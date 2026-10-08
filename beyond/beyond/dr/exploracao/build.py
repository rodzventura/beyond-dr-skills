#!/usr/bin/env python3
"""Gera exploracao/direcoes.html (autocontido) a partir de direcoes.fonte.html.

Marcadores na fonte:
  /*DR:FONTES*/   -> @font-face das woff2 de claude-code/skills/dr-slides/assets/fontes (base64)
  /*DR:ICONES*/{} -> JSON {nome: path-d} dos ícones pixel (dr-slides/assets/icones/_icones.json)
  {{SVG:caminho}} -> conteúdo do SVG (caminho relativo a beyond/)
  {{IMG:caminho}} -> data URI WebP (caminho relativo a beyond/)
"""
import base64, io, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BEYOND = os.path.abspath(os.path.join(AQUI, '..', '..'))  # beyond/beyond (raiz da marca)
FONTES = os.path.join(BEYOND, 'claude-code', 'skills', 'dr-slides', 'assets', 'fontes')

PESOS = {'regular': 400, 'italic': 400, 'medium': 500, 'semibold': 600, 'bold': 700, 'extrabold': 800, 'black': 900}
FAMILIAS = {'rethinksans': 'Rethink Sans', 'sofiasansextracondensed': 'Sofia Sans Extra Condensed'}


def fontes():
    css = []
    for f in sorted(os.listdir(FONTES)):
        if not f.endswith('.woff2'):
            continue
        fam, peso = f[:-6].split('-')
        b64 = base64.b64encode(open(os.path.join(FONTES, f), 'rb').read()).decode()
        estilo = 'italic' if peso == 'italic' else 'normal'
        css.append("@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2');font-weight:%d;font-style:%s;font-display:block}"
                   % (FAMILIAS[fam], b64, PESOS[peso], estilo))
    return '\n'.join(css)


def imagem(caminho):
    from PIL import Image
    im = Image.open(os.path.join(BEYOND, caminho))
    im.thumbnail((1920, 1920))
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=82)
    return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()


def main():
    fonte = os.path.join(AQUI, 'direcoes.fonte.html')
    saida = os.path.join(AQUI, 'direcoes.html')
    html = open(fonte, encoding='utf-8').read()
    html = html.replace('/*DR:FONTES*/', fontes())
    icones = open(os.path.join(BEYOND, 'claude-code', 'skills', 'dr-slides', 'assets', 'icones', '_icones.json')).read()
    html = html.replace('/*DR:ICONES*/{}', icones)
    html = re.sub(r'\{\{SVG:([^}]+)\}\}', lambda m: re.sub(r'<!--.*?-->', '', open(os.path.join(BEYOND, m.group(1))).read()), html)
    html = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: imagem(m.group(1)), html)
    open(saida, 'w', encoding='utf-8').write(html)
    print('ok', saida, '%.0f KB' % (os.path.getsize(saida) / 1024))


if __name__ == '__main__':
    main()
