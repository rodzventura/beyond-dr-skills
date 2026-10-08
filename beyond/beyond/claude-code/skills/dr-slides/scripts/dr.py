#!/usr/bin/env python3
"""DR · ferramenta do deck da Difusão Recorrente.

O deck é um arquivo-fonte `.dr.html`: um comentário de cabeçalho e uma sequência de
<section class="dr" ...> compostas só com as classes dr-* e os tokens do design system.

  <!-- dr:deck titulo="DR · Julho 2026" rodape="DR Beyond 2026" -->
  <section class="dr" data-secao="receita" data-fundo="grade"> ... <aside class="dr-notas">…</aside></section>

Comandos
  dr.py verificar  DECK.dr.html            regras do design system (fontes, cores, classes, imagens, estrutura)
  dr.py gerar      DECK.dr.html -o SAIDA   HTML único, autocontido (fontes, imagens WebP, motor); roda `verificar` antes
  dr.py pendencias DECK.dr.html            lista PENDENTE:, PARA O DESIGN: e imagens pedidas
  dr.py montar     PARTES... -o DECK.dr.html --edicao "Outubro · 2026"
                                           junta as partes dos apresentadores no deck final (capa, agenda e encerramento geradas)
  dr.py pacote     PARTE.dr.html --versao N -o PASTA
                                           gera o que vai para o Drive: zip do fonte com img/, pré-visualização, pendências e entrega.json
  dr.py componentes                        regenera COMPONENTES.md a partir dos comentários @componente do CSS
  dr.py construir  FONTE.html -o SAIDA     (legado) substitui marcadores /*DR:...*/ e {{SVG:}} {{IMG:}} numa página livre

A verificação visual (texto cabendo no container, nada embaixo do rodapé) roda no navegador:
tecla V no deck gerado, ou DR.verificar() no console.
"""
import argparse, base64, hashlib, html, io, os, re, sys
from html.parser import HTMLParser

SLIDES = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MARCA = os.path.abspath(os.path.join(SLIDES, '..', '..', '..'))  # beyond/beyond (raiz da marca)
FONTES = os.path.join(SLIDES, 'assets', 'fontes')  # a skill é autocontida: fontes e logos moram em assets/
CSS = os.path.join(SLIDES, 'design-system.css')
PESOS = {'regular': 400, 'italic': 400, 'medium': 500, 'semibold': 600, 'bold': 700, 'extrabold': 800, 'black': 900}
FAMILIAS = {'rethinksans': 'Rethink Sans', 'sofiasansextracondensed': 'Sofia Sans Extra Condensed'}

SECOES = {'marca', 'cerimonia', 'institucional', 'receita', 'pessoas', 'premio', 'roxo', 'verde', 'laranja', 'rosa'}
GENERICAS = {'roxo', 'verde', 'laranja', 'rosa'}
ESCURAS = {'roxo', 'rosa', 'institucional', 'cerimonia', 'premio'}  # cor viva escura: texto branco
# limites de texto (avisos, não erros): empurram o conteúdo para o que cabe no telão
LIMITE_TITULO = {'g': 28, 'frase': 70, 'm': 70, '': 70}
LIMITES = {'dr-sub': 90, 'dr-texto': 300, 'dr-legenda': 160, 'dr-pilula': 40, 'dr-item': 90, 'dr-aba': 24}
VOID = {'img', 'br', 'hr', 'meta', 'link', 'input', 'source', 'wbr'}
FUNDOS = {'branco', 'grade', 'nevoa', 'lilas', 'lilas-grade', 'hachura', 'cor', 'clara', 'escuro'}
MODIFICADORES = {'g', 'frase', 'm', 'p', 'centro', 'meio', 'coluna', 'base', 'esticar', 'cor', 'viva', 'cheia',
                 'sem-sombra', 'escura', 'inversa', 'numerada', 'contida', 'sem-borda', 'recorte', 'q', 'gira', 'sec'}
PROPS_LIVRES = {'grid-column', 'grid-row', 'align-self', 'justify-self', 'order', 'flex', 'width', 'max-width',
                'height', 'min-height', 'text-align', 'gap', 'margin-top', 'align-items', 'justify-content'}
PROIBIDO_VALOR = re.compile(r'#|rgb|hsl|url\(|font|!important|expression', re.I)
TAGS_PROIBIDAS = {'script', 'style', 'link', 'iframe', 'object', 'embed', 'font', 'meta', 'base'}


def tokens():
    return set(re.findall(r'--([a-z0-9-]+)\s*:', open(CSS, encoding='utf-8').read()))


def versao_css():
    m = re.search(r'design system v(\d+\.\d+\.\d+)', open(CSS, encoding='utf-8').read())
    return m.group(1) if m else '0.0.0'


def classes_css():
    return set(re.findall(r'\.(dr-[a-z0-9-]+)', open(CSS, encoding='utf-8').read()))


# ---------------------------------------------------------------- leitura do deck
def ler(caminho):
    fonte = open(caminho, encoding='utf-8').read()
    m = re.search(r'<!--\s*dr:deck(.*?)-->', fonte, re.S)
    meta = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1))) if m else {}
    return fonte, meta


class Leitor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.erros, self.avisos, self.imgs, self.secoes = [], [], [], []
        self.slide = 0
        self.pilha = []  # elementos abertos com limite de texto: [tag, limite, nome, texto]
        self.contexto = []  # classes dos elementos abertos (para p/li dentro de card, pasta e lista)
        self.agenda = []

    def onde(self):
        return 'slide %d (linha %d)' % (self.slide, self.getpos()[0])

    def limite_de(self, tag, cls):
        if 'dr-titulo' in cls:
            mod = next((m for m in ('g', 'frase', 'm') if m in cls), '')
            return LIMITE_TITULO[mod], 'título' + (' (%s)' % mod if mod else '')
        for c in LIMITES:
            if c in cls:
                return LIMITES[c], c
        anc = [c for lista in self.contexto for c in lista]
        if tag == 'p' and ('dr-card' in anc or 'dr-pasta' in anc):
            return 90, 'texto de card/pasta'
        if tag == 'li' and 'dr-lista' in anc:
            return 70, 'item de lista'
        return None, None

    def handle_data(self, data):
        for e in self.pilha:
            e[3] += data

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.contexto:
            self.contexto.pop()
        for i in range(len(self.pilha) - 1, -1, -1):
            if self.pilha[i][0] == tag:
                _, lim, nome, texto = self.pilha.pop(i)
                n = len(' '.join(texto.split()))
                if n > lim:
                    self.avisos.append('slide %d: texto longo (%d > %d) em %s: «%s…»' % (self.slide, n, lim, nome, ' '.join(texto.split())[:40]))
                break

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get('class') or '').split()
        if tag not in VOID:
            self.contexto.append(cls)
            lim, nome = self.limite_de(tag, cls)
            if lim:
                self.pilha.append([tag, lim, nome, ''])
        if tag == 'section':
            self.slide += 1
            cls = (a.get('class') or '').split()
            if 'dr' not in cls:
                self.erros.append('%s: <section> precisa de class="dr"' % self.onde())
            sec = a.get('data-secao')
            if sec not in SECOES:
                self.erros.append('%s: data-secao="%s" inválido (use %s)' % (self.onde(), sec, ', '.join(sorted(SECOES))))
            if a.get('data-fundo') and a['data-fundo'] not in FUNDOS:
                self.erros.append('%s: data-fundo="%s" inválido (use %s)' % (self.onde(), a['data-fundo'], ', '.join(sorted(FUNDOS))))
            self.secoes.append({'slide': self.slide, 'secao': sec, 'notas': False})
            if sec in GENERICAS and not a.get('data-rotulo') and a.get('data-rodape') != 'nenhum':
                self.avisos.append('%s: seção genérica "%s" sem data-rotulo: o rodapé ficará sem o nome do bloco' % (self.onde(), sec))
            if a.get('data-agenda'):
                self.agenda.append((self.slide, a['data-agenda']))
        if tag in TAGS_PROIBIDAS:
            self.erros.append('%s: <%s> não é permitido no conteúdo' % (self.onde(), tag))
        for k, v in attrs:
            if k.startswith('on'):
                self.erros.append('%s: atributo %s não é permitido' % (self.onde(), k))
            if k == 'class':
                for c in (v or '').split():
                    if c == 'dr' and tag == 'section':
                        continue
                    if c.startswith('dr-'):
                        if c not in self.validas:
                            self.erros.append('%s: classe "%s" não existe no design system' % (self.onde(), c))
                    elif c not in MODIFICADORES:
                        self.erros.append('%s: classe "%s" fora do design system (use dr-* ou modificadores documentados)' % (self.onde(), c))
                    if c == 'dr-notas' and self.secoes:
                        self.secoes[-1]['notas'] = True
            if k == 'style' and v:
                for decl in [d.strip() for d in v.split(';') if d.strip()]:
                    if ':' not in decl:
                        continue
                    p, val = [x.strip() for x in decl.split(':', 1)]
                    if PROIBIDO_VALOR.search(val):
                        self.erros.append('%s: style "%s" — cor/fonte só por token (var(--...))' % (self.onde(), decl))
                    elif p.startswith('--'):
                        for t in re.findall(r'var\(--([a-z0-9-]+)\)', val):
                            if t not in self.toks:
                                self.erros.append('%s: token --%s não existe' % (self.onde(), t))
                        if not re.fullmatch(r'(var\(--[a-z0-9-]+\)|-?[\d.]+(px|%|em)?|\s)+', val):
                            self.erros.append('%s: valor "%s" em %s — use token ou número' % (self.onde(), val, p))
                    elif p not in PROPS_LIVRES:
                        self.erros.append('%s: propriedade "%s" não é permitida em style (só layout: %s)' % (self.onde(), p, ', '.join(sorted(PROPS_LIVRES))))
            if k == 'data-cores':
                for t in (v or '').split(','):
                    if t.strip() not in self.toks:
                        self.erros.append('%s: data-cores usa "%s", que não é token' % (self.onde(), t))
        if tag == 'img':
            src = a.get('src', '')
            if not src:
                self.erros.append('%s: <img> sem src (para imagem que falta, use <div data-pedido="...">)' % self.onde())
            elif re.match(r'https?:', src):
                self.erros.append('%s: imagem externa (%s) — salve o arquivo junto do deck' % (self.onde(), src))
            else:
                self.imgs.append((self.slide, src))
            if 'alt' not in a:
                self.avisos.append('%s: <img> sem alt' % self.onde())


def verificar(caminho, silencioso=False):
    fonte, meta = ler(caminho)
    base = os.path.dirname(os.path.abspath(caminho))
    L = Leitor()
    L.toks, L.validas = tokens(), classes_css()
    L.feed(fonte)
    for slide, src in L.imgs:
        if not src.startswith('data:') and not os.path.exists(os.path.join(base, src)):
            L.erros.append('slide %d: imagem não encontrada: %s' % (slide, src))
    for s in L.secoes:
        if not s['notas']:
            L.avisos.append('slide %d: sem notas do apresentador (<aside class="dr-notas">)' % s['slide'])
    if re.search(r'lorem ipsum', fonte, re.I):
        L.erros.append('o deck contém "lorem ipsum" — troque por conteúdo real ou PENDENTE:')
    if not silencioso:
        for e in L.erros:
            print('ERRO  ', e)
        for w in L.avisos:
            print('aviso ', w)
        print('%d slide(s) · %d erro(s) · %d aviso(s) · design system v%s' % (len(L.secoes), len(L.erros), len(L.avisos), versao_css()))
    return L


# ---------------------------------------------------------------- geração
def fontes():
    css = []
    for f in sorted(os.listdir(FONTES)):
        if not f.endswith('.woff2'):
            continue
        fam, peso = f[:-6].split('-')
        b64 = base64.b64encode(open(os.path.join(FONTES, f), 'rb').read()).decode()
        css.append("@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2');font-weight:%d;font-style:%s;font-display:block}"
                   % (FAMILIAS[fam], b64, PESOS[peso], 'italic' if peso == 'italic' else 'normal'))
    return '\n'.join(css)


def webp(caminho, maximo=1920):
    try:
        from PIL import Image, ImageOps
    except ImportError:
        sys.exit('Falta a biblioteca Pillow (converte as imagens para WebP). Instale com: pip install pillow')
    im = ImageOps.exif_transpose(Image.open(caminho))
    if im.mode not in ('RGB', 'RGBA'):
        im = im.convert('RGBA')
    im.thumbnail((maximo, maximo))
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=82, method=5)
    return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()


def svg(rel):
    base = SLIDES if os.path.exists(os.path.join(SLIDES, rel)) else MARCA  # rel é relativo à skill (ou, nas páginas de exploração, à raiz da marca)
    return re.sub(r'<!--.*?-->', '', open(os.path.join(base, rel), encoding='utf-8').read())


def gerar(caminho, saida):
    L = verificar(caminho)
    if L.erros:
        sys.exit('não gerado: corrija os erros acima.')
    fonte, meta = ler(caminho)
    base = os.path.dirname(os.path.abspath(caminho))
    imagens = {}

    def troca(m):
        src = m.group(2)
        if src.startswith('data:'):
            return m.group(0)
        p = os.path.join(base, src)
        k = hashlib.sha1(open(p, 'rb').read()).hexdigest()[:12]
        if k not in imagens:
            imagens[k] = webp(p)
        return '<img%sdata-src="%s"' % (m.group(1), k)

    slides = re.sub(r'<!--\s*dr:deck.*?-->', '', fonte, flags=re.S)
    slides = re.sub(r'<img\b([^>]*?)src="([^"]+)"', troca, slides)
    icones = open(os.path.join(SLIDES, 'assets', 'icones', '_icones.json')).read()
    import json
    t = open(os.path.join(SLIDES, 'template.html'), encoding='utf-8').read()
    rep = {
        '/*DR:TITULO*/': html.escape(meta.get('titulo', 'Difusão Recorrente')),
        '/*DR:RODAPE*/': html.escape(meta.get('rodape', 'DR Beyond 2026')),
        '/*DR:VERSAO*/': versao_css(),
        '/*DR:FONTES*/': fontes(),
        '/*DR:CSS*/': open(CSS, encoding='utf-8').read(),
        '/*DR:SLIDES*/': slides,
        '/*DR:SELO*/': svg('assets/selo-dr26.svg'),
        '/*DR:LOGO*/': svg('assets/logos/beyond-co.svg'),
        '/*DR:ABA*/': svg('assets/logos/beyond-be-aba.svg'),
        '/*DR:IMAGENS*/': json.dumps(imagens),
        '/*DR:MOTOR*/': 'window.DR_ICONES=' + icones + ';\n' + open(os.path.join(SLIDES, 'motor.js'), encoding='utf-8').read(),
    }
    for k, v in rep.items():
        t = t.replace(k, v)
    open(saida, 'w', encoding='utf-8').write(t)
    print('ok %s · %d slide(s) · %d imagem(ns) · %.1f MB' % (saida, len(L.secoes), len(imagens), os.path.getsize(saida) / 1048576))


def listar_pendencias(caminho):
    fonte, _ = ler(caminho)
    saida, n = [], 0
    for p in re.split(r'(?=<section\b)', fonte):
        if not p.startswith('<section'):
            continue
        n += 1
        texto = re.sub(r'<[^>]+>', ' ', p)
        for m in re.finditer(r'(PENDENTE|PARA O DESIGN):\s*([^\n<]+)', texto):
            saida.append((n, m.group(1), m.group(2).strip()))
        for m in re.finditer(r'data-pedido="([^"]+)"', p):
            saida.append((n, 'IMAGEM', html.unescape(m.group(1))))
    return saida


def pendencias(caminho):
    itens = listar_pendencias(caminho)
    for n, tipo, txt in itens:
        print('slide %2d · %s: %s' % (n, tipo, txt))
    print('%d pendência(s)' % len(itens))


# ---------------------------------------------------------------- montagem (designer)
CAPA = """<section class="dr" data-secao="marca" data-rodape="nenhum">
  <svg class="dr-forma" data-forma="octogono" data-cores="p300,p700,p600,p400,p300" data-cy="560" data-r="1500" data-rmin=".36" data-n="5"></svg>
  <div class="dr-selo" data-a="escala"></div>
  <div class="dr-topo"><span class="dr-pilula" data-a="sobe">Difusão Recorrente</span><span class="dr-pilula" data-a="sobe">%(edicao)s</span></div>
  <div class="dr-aba-be" data-a="sobe"></div>
  <aside class="dr-notas">Tela de abertura. Fica no ar enquanto todos se acomodam.</aside>
</section>
"""
ENCERRAMENTO = """<section class="dr" data-secao="marca" data-rodape="nenhum">
  <svg class="dr-forma" data-forma="octogono" data-cores="p300,p700,p600,p400,p300" data-cy="560" data-r="1500" data-rmin=".36" data-n="5"></svg>
  <div class="dr-selo" data-a="escala"></div>
  <div class="dr-topo"><span class="dr-pilula" data-a="sobe">Obrigado!</span><span class="dr-pilula" data-a="sobe">Até o próximo DR</span></div>
  <div class="dr-aba-be" data-a="sobe"></div>
  <aside class="dr-notas">Encerramento.</aside>
</section>
"""


def ler_parte(caminho):
    """Uma parte = um arquivo .dr.html de um apresentador, com o cabeçalho
    <!-- dr:parte bloco="Receita" apresentador="Nome" cargo="Cargo" secao="verde" -->"""
    fonte = open(caminho, encoding='utf-8').read()
    m = re.search(r'<!--\s*dr:parte(.*?)-->', fonte, re.S)
    if not m:
        sys.exit('%s: falta o cabeçalho <!-- dr:parte bloco="…" apresentador="…" cargo="…" secao="…" -->' % caminho)
    meta = {k: html.unescape(v) for k, v in re.findall(r'(\w+)="([^"]*)"', m.group(1))}
    for k in ('bloco', 'secao'):
        if not meta.get(k):
            sys.exit('%s: o cabeçalho dr:parte precisa de %s=' % (caminho, k))
    if meta['secao'] not in SECOES:
        sys.exit('%s: secao="%s" inválida (use %s)' % (caminho, meta['secao'], ', '.join(sorted(SECOES))))
    corpo = re.sub(r'<!--\s*dr:parte.*?-->', '', fonte, flags=re.S).strip()
    # imagens: reescreve para caminho relativo ao arquivo de saída (feito em montar)
    return meta, corpo, os.path.dirname(os.path.abspath(caminho))


def agenda_html(partes):
    n = len(partes)
    cols = {1: 'dr-grid-2', 2: 'dr-grid-2', 3: 'dr-grid-3', 4: 'dr-grid-4'}[n]
    pastas = []
    for i, (meta, corpo, _) in enumerate(partes, 1):
        itens = [html.escape(x) for x in re.findall(r'<section[^>]*?data-agenda="([^"]*)"', corpo)][:5]
        quem = ' · '.join(x for x in (meta.get('apresentador'), meta.get('cargo')) if x)
        if len(quem) > 38:  # cargo longo não cabe na pílula da pasta: fica só o nome (o cargo vai para as notas)
            quem = meta.get('apresentador', '')
        inversa = ' inversa' if meta['secao'] in ESCURAS else ''
        lista = '<ul class="dr-lista">' + ''.join('<li>%s</li>' % t for t in itens) + '</ul>' if itens else ''
        pastas.append('      <div class="dr-pasta%s" data-secao="%s" data-a="sobe"><span class="dr-aba">%02d</span><h3>%s</h3>%s%s</div>'
                      % (inversa, meta['secao'], i, html.escape(meta['bloco']),
                         '<span class="dr-pilula">%s</span>' % html.escape(quem) if quem else '', lista))
    return ('<section class="dr" data-secao="marca" data-fundo="nevoa" data-rotulo="Agenda">\n  <div class="dr-area">\n'
            '    <div class="dr-cab"><h2 class="dr-titulo" data-a="palavras">A agenda de hoje</h2></div>\n'
            '    <div class="%s">\n%s\n    </div>\n  </div>\n  <aside class="dr-notas">Agenda gerada a partir dos blocos do deck.</aside>\n</section>\n' % (cols, '\n'.join(pastas)))


def montar(arquivos, saida, edicao, titulo, rodape, capa=True, agenda=True, encerramento=True):
    partes = [ler_parte(a) for a in arquivos]
    pasta_saida = os.path.dirname(os.path.abspath(saida))
    blocos = []
    for meta, corpo, base in partes:
        def reescreve(m):
            src = m.group(2)
            if re.match(r'(https?:|data:)', src):
                return m.group(0)
            return '<img%ssrc="%s"' % (m.group(1), os.path.relpath(os.path.join(base, src), pasta_saida))
        blocos.append(re.sub(r'<img\b([^>]*?)src="([^"]+)"', reescreve, corpo))
    out = ['<!-- dr:deck titulo="%s" rodape="%s" -->' % (html.escape(titulo, quote=True), html.escape(rodape, quote=True)),
           '<!-- Deck montado por dr.py montar a partir de: %s -->' % ', '.join(os.path.basename(a) for a in arquivos), '']
    if capa:
        out.append(CAPA % {'edicao': html.escape(edicao)})
    if agenda:
        if len(partes) > 4:
            print('aviso  mais de 4 blocos: agenda não gerada. Monte à mão (PARA O DESIGN).')
        else:
            out.append(agenda_html(partes))
    for (meta, _, _), b in zip(partes, blocos):
        out.append('<!-- ===== %s%s ===== -->' % (meta['bloco'], ' · ' + meta['apresentador'] if meta.get('apresentador') else ''))
        out.append(b + '\n')
    if encerramento:
        out.append(ENCERRAMENTO)
    open(saida, 'w', encoding='utf-8').write('\n'.join(out))
    print('ok %s · %d bloco(s) · %d slide(s) de conteúdo' % (saida, len(partes), sum(b.count('<section') for b in blocos)))
    verificar(saida)


# ---------------------------------------------------------------- pacote para o Drive
def slug(txt):
    import unicodedata
    t = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-') or 'bloco'


def pacote(caminho, versao, saida):
    """Gera os arquivos de uma entrega no Drive:
       DR-parte-<bloco>-vN.zip   fonte (parte.dr.html) + img/ com só as imagens usadas
       DR-parte-<bloco>-vN.html  pré-visualização autocontida da parte
       pendencias-<bloco>-vN.md  lista de PENDENTE / PARA O DESIGN / imagens pedidas
       entrega.json              manifesto (bloco, apresentador, versão, slides, design system)"""
    import json, shutil, tempfile, zipfile, datetime
    L = verificar(caminho)
    if L.erros:
        sys.exit('não empacotado: corrija os erros acima.')
    fonte = open(caminho, encoding='utf-8').read()
    m = re.search(r'<!--\s*dr:parte(.*?)-->', fonte, re.S)
    if not m:
        sys.exit('falta o cabeçalho <!-- dr:parte bloco="…" apresentador="…" cargo="…" secao="…" -->')
    meta = {k: html.unescape(v) for k, v in re.findall(r'(\w+)="([^"]*)"', m.group(1))}
    base = os.path.dirname(os.path.abspath(caminho))
    sl = slug(meta.get('bloco', 'bloco'))
    nome = 'DR-parte-%s-v%d' % (sl, versao)
    os.makedirs(saida, exist_ok=True)

    # imagens: tudo vai para img/ dentro do pacote (caminhos relativos ao fonte)
    usados, mapa = {}, {}
    def troca(mm):
        src = mm.group(2)
        if re.match(r'(https?:|data:)', src):
            return mm.group(0)
        origem = os.path.normpath(os.path.join(base, src))
        if origem not in mapa:
            arc = 'img/' + os.path.basename(origem)
            if arc in usados and usados[arc] != origem:
                arc = 'img/%s-%s' % (hashlib.sha1(origem.encode()).hexdigest()[:6], os.path.basename(origem))
            usados[arc] = origem
            mapa[origem] = arc
        return '<img%ssrc="%s"' % (mm.group(1), mapa[origem])
    fonte_pkg = re.sub(r'<img\b([^>]*?)src="([^"]+)"', troca, fonte)

    with zipfile.ZipFile(os.path.join(saida, nome + '.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('parte.dr.html', fonte_pkg)
        for arc, origem in usados.items():
            z.write(origem, arc)

    # pré-visualização: gera a partir de uma cópia temporária com o cabeçalho de deck
    tmp = tempfile.mkdtemp()
    try:
        for arc, origem in usados.items():
            os.makedirs(os.path.join(tmp, os.path.dirname(arc)), exist_ok=True)
            shutil.copy(origem, os.path.join(tmp, arc))
        t = os.path.join(tmp, 'parte.dr.html')
        open(t, 'w', encoding='utf-8').write('<!-- dr:deck titulo="DR · %s (parte v%d)" rodape="DR Beyond 2026" -->\n' % (html.escape(meta.get('bloco', ''), quote=True), versao) + fonte_pkg)
        gerar(t, os.path.join(saida, nome + '.html'))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    itens = listar_pendencias(caminho)
    linhas = ['# Pendências · %s · v%d' % (meta.get('bloco', ''), versao), '']
    linhas += ['- slide %d · %s: %s' % i for i in itens] or ['Nenhuma pendência.']
    open(os.path.join(saida, 'pendencias-%s-v%d.md' % (sl, versao)), 'w', encoding='utf-8').write('\n'.join(linhas) + '\n')
    manifesto = {'bloco': meta.get('bloco'), 'apresentador': meta.get('apresentador'), 'cargo': meta.get('cargo'), 'secao': meta.get('secao'),
                 'versao': versao, 'slides': len(L.secoes), 'imagens': len(usados), 'pendencias': len(itens),
                 'design_system': versao_css(), 'gerado_em': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                 'arquivos': [nome + '.zip', nome + '.html', 'pendencias-%s-v%d.md' % (sl, versao)]}
    json.dump(manifesto, open(os.path.join(saida, 'entrega.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('ok pacote %s · v%d · %d slide(s) · %d imagem(ns) · %d pendência(s) → %s' % (meta.get('bloco'), versao, len(L.secoes), len(usados), len(itens), saida))


def componentes():
    css = open(CSS, encoding='utf-8').read()
    linhas = ['# Componentes do design system DR', '',
              'Gerado por `dr.py componentes` a partir de `design-system.css`. Não editar à mão.', '',
              '## Slide', '', '`<section class="dr" data-secao="…" data-fundo="…">` · seções: ' + ', '.join(sorted(SECOES)) +
              ' · fundos: ' + ', '.join(sorted(FUNDOS)) + '.', '',
              'Modificadores aceitos (sem prefixo): ' + ', '.join('`%s`' % m for m in sorted(MODIFICADORES)) + '.', '',
              'Em `style` só entram tokens (`--cor:var(--gr300)`, `--v:92.4`, `--fundo:var(--or300)`, `--n:300px`) e propriedades de layout: ' +
              ', '.join(sorted(PROPS_LIVRES)) + '.', '', '## Componentes', '']
    for m in re.finditer(r'/\*\s*@componente\s+(.*?)\*/', css, re.S):
        linhas.append('- ' + ' '.join(m.group(1).split()))
    toks = sorted(t for t in tokens() if re.match(r'(p|pk|or|gr|n)\d+$|gym-', t))
    linhas += ['', '## Tokens de cor', '', ', '.join('`%s`' % t for t in toks), '']
    open(os.path.join(SLIDES, 'COMPONENTES.md'), 'w', encoding='utf-8').write('\n'.join(linhas))
    print('ok COMPONENTES.md')


def construir(fonte, saida):
    """Legado: páginas livres (exploração) com marcadores."""
    h = open(fonte, encoding='utf-8').read()
    icones = open(os.path.join(SLIDES, 'assets', 'icones', '_icones.json')).read()
    h = h.replace('/*DR:FONTES*/', fontes()).replace('/*DR:CSS*/', open(CSS, encoding='utf-8').read())
    h = h.replace('/*DR:MOTOR*/', 'window.DR_ICONES=' + icones + ';\n' + open(os.path.join(SLIDES, 'motor.js'), encoding='utf-8').read())
    h = h.replace('/*DR:ICONES*/{}', icones)
    h = re.sub(r'\{\{SVG:([^}]+)\}\}', lambda m: svg(m.group(1)), h)
    cache = {}
    h = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: cache.setdefault(m.group(1), webp(m.group(1) if os.path.isabs(m.group(1)) else os.path.join(MARCA, m.group(1)))), h)
    open(saida, 'w', encoding='utf-8').write(h)
    print('ok %s · %.0f KB' % (saida, os.path.getsize(saida) / 1024))


def main():
    ap = argparse.ArgumentParser(description='DR · ferramenta do deck da Difusão Recorrente')
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('verificar'); v.add_argument('deck')
    g = sub.add_parser('gerar'); g.add_argument('deck'); g.add_argument('-o', '--saida', required=True)
    p = sub.add_parser('pendencias'); p.add_argument('deck')
    m = sub.add_parser('montar'); m.add_argument('partes', nargs='+'); m.add_argument('-o', '--saida', required=True)
    m.add_argument('--edicao', required=True, help='ex.: "Outubro · 2026"'); m.add_argument('--titulo'); m.add_argument('--rodape', default='DR Beyond 2026')
    m.add_argument('--sem-capa', action='store_true'); m.add_argument('--sem-agenda', action='store_true'); m.add_argument('--sem-encerramento', action='store_true')
    k = sub.add_parser('pacote'); k.add_argument('parte'); k.add_argument('--versao', type=int, required=True); k.add_argument('-o', '--saida', required=True)
    sub.add_parser('componentes')
    c = sub.add_parser('construir'); c.add_argument('fonte'); c.add_argument('-o', '--saida', required=True)
    a = ap.parse_args()
    if a.cmd == 'verificar':
        sys.exit(1 if verificar(a.deck).erros else 0)
    elif a.cmd == 'gerar':
        gerar(a.deck, a.saida)
    elif a.cmd == 'pendencias':
        pendencias(a.deck)
    elif a.cmd == 'montar':
        montar(a.partes, a.saida, a.edicao, a.titulo or 'DR · ' + a.edicao, a.rodape, not a.sem_capa, not a.sem_agenda, not a.sem_encerramento)
    elif a.cmd == 'pacote':
        pacote(a.parte, a.versao, a.saida)
    elif a.cmd == 'componentes':
        componentes()
    elif a.cmd == 'construir':
        construir(a.fonte, a.saida)


if __name__ == '__main__':
    main()
