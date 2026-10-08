---
name: "dr-slides"
description: "Use esta skill para montar, editar ou gerar slides da Difusão Recorrente (DR), o evento trimestral da Beyond. Traz o formato do deck (.dr.html), o design system (classes dr-*), as composições de referência e a ferramenta dr.py (verificar, gerar, montar, pendências)."
---

# DR · slides

O deck da DR é um arquivo-fonte `.dr.html` com uma `<section class="dr">` por slide. **Não existe catálogo fechado de layouts**: cada slide é composto livremente, a partir do conteúdo, **só com as peças do design system** (`design-system.css`). O `dr.py` verifica as regras e gera um HTML único, animado, com notas, tela sempre ativa e PDF.

Leia junto: `COMPONENTES.md` (lista gerada de classes) e a skill `dr-marca` (roteiro, escrita, números).

## Fluxo

```bash
DR=<pasta desta skill>/scripts/dr.py   # ex.: ~/beyond-dr-skills/beyond/beyond/claude-code/skills/dr-slides/scripts/dr.py
python3 $DR verificar deck.dr.html          # regras do design system + avisos de texto longo
python3 $DR gerar deck.dr.html -o deck.html # HTML final (roda a verificação antes)
python3 $DR pendencias deck.dr.html         # PENDENTE:, PARA O DESIGN:, imagens pedidas
python3 $DR pacote parte.dr.html --versao 1 -o saida/   # apresentador: zip do fonte, pré-visualização, pendências (vai para o Drive)
python3 $DR montar parte1.dr.html parte2.dr.html -o deck.dr.html --edicao "Outubro · 2026"   # designer: junta as partes
```

Depois de gerar, **abra o HTML e rode a verificação visual**: tecla **V** (ou `DR.verificar()` no console). Ela acusa texto fora do container, fora da `dr-area`, fora do slide ou embaixo do rodapé. **Tudo tem de caber no seu container**: se acusar, reescreva mais curto ou recomponha; nunca diminua fonte fora da escala.

Teclas do deck: ← → espaço/clique navegam · F tela cheia · G visão geral · N notas · R repete animação · V verifica.

## Parte do apresentador (perfil "minha parte")

O apresentador traz o material do bloco dele; você devolve **uma parte**, que o designer junta às outras. Siga a skill `dr-marca` (identidade fixa, estrutura livre, conversa inicial, roteiro).

1. Faça a **conversa inicial** (`dr-marca/entrevista-inicial.md`): quem é a pessoa, qual sessão vai preencher e como traz o conteúdo.
2. Pergunte de forma aberta o que a pessoa quer apresentar; leia o material e proponha a lista de slides. Espere o ok.
3. Escreva `parte.dr.html` com o cabeçalho abaixo e as `<section class="dr">`. Marque com `data-agenda="Nome curto"` os 1 a 4 slides que devem aparecer na agenda do evento. Notas em todo slide.
4. `verificar`, `gerar -o parte.html` (a pré-visualização dessa parte), tecla V no navegador, `pendencias`.
5. Entregue pela skill `dr-entrega` (pasta do Drive, com versão): `dr.py pacote` gera o pacote da parte. As imagens ficam em `img/`, com caminho relativo no `src`.

```html
<!-- dr:parte bloco="Receita" apresentador="Nome Sobrenome" cargo="CRO" secao="verde" -->
<section class="dr" data-secao="verde" data-rotulo="Receita" data-fundo="grade" data-agenda="Resultados do trimestre">
  …
</section>
```

`bloco` é o nome no rodapé e na agenda; `secao` é a família de cor (`roxo`, `verde`, `laranja`, `rosa`) e deve ser a mesma em todos os slides da parte, com `data-rotulo` igual ao `bloco` nas famílias genéricas. O apresentador não precisa escolher a cor: o designer ajusta na montagem.

## Formato

```html
<!-- dr:deck titulo="DR · Outubro 2026" rodape="DR Beyond 2026" -->
<section class="dr" data-secao="receita" data-fundo="grade">
  <div class="dr-area">
    <div class="dr-cab"><span class="dr-pilula"><i class="dr-ponto"></i>Receita</span><h2 class="dr-titulo">Resultados obtidos</h2></div>
    <div class="dr-corpo">…</div>
  </div>
  <aside class="dr-notas">O que o apresentador fala aqui.</aside>
</section>
```

- `data-secao`: família de cor do bloco: `roxo` · `verde` · `laranja` · `rosa` (genéricas, para qualquer bloco; o nome vai em `data-rotulo`). Equivalentes nomeados: `institucional`=roxo, `receita`=verde, `pessoas`=laranja, `cerimonia`=rosa; `marca` (capa e agenda) e `premio` (roxo com destaque rosa). Define pílula, destaque, rodapé e sombras.
- `data-fundo`: `branco` · `grade` · `nevoa` · `lilas` · `lilas-grade` · `hachura` · `cor` · `clara` · `escuro`.
- Rodapé: o motor gera sozinho (`DR Beyond 2026 | BLOCO | ›`). `data-rotulo` dá o nome do bloco (obrigatório nas famílias genéricas); `data-rodape="nenhum"` tira (capa, aberturas, slides de imagem cheia).
- Imagens: `<img src="img/arquivo.jpg" alt="…">`, caminho relativo ao `.dr.html`. Imagem que ainda não existe: `<div data-pedido="Foto do time no evento"></div>`.
- Animação: `data-a="sobe"` · `"surge"` · `"escala"` · `"palavras"` (título palavra a palavra). Números com `data-conta="4,0"` contam até o valor.
- Notas: `<aside class="dr-notas">` em todo slide.

## Regras (o `dr.py verificar` reprova)

- Só classes `dr-*` existentes e os modificadores documentados (`g`, `frase`, `m`, `p`, `centro`, `meio`, `coluna`, `base`, `esticar`, `cor`, `viva`, `cheia`, `sem-sombra`, `escura`, `inversa`, `numerada`, `contida`, `sem-borda`, `recorte`).
- Nada de `<style>`, `<script>`, `font-family`, cor em hex/rgb, imagem externa.
- `style` só aceita **tokens** (`--cor:var(--gr300)`, `--fundo:var(--or300)`, `--v:83.3`, `--n:300px`, `--div:58%`, `--foco:50% 20%` para enquadrar foto) e propriedades de **layout** (width, max-width, height, flex, gap, align-self, text-align…).
- Texto acima dos limites gera **aviso** (títulos ~70 caracteres, `g` 28, cards 90, itens de lista 70, pílulas 40): encurte em vez de ignorar.
- Sem "lorem ipsum". O que falta vira `PENDENTE:` (dado) ou `PARA O DESIGN:` (visual), nas notas ou no texto.
- Fontes: só Rethink Sans (tudo) e Sofia Sans Extra Condensed (só nos números do `dr-item`). Contorno 1,8px. Títulos em Rethink Sans 600.

## Composições de referência (não são limites)

**Atenção:** o exemplo é o DR de julho/2026 e serve só para ver *como compor*. Os assuntos dele (ofensores, programas e parcerias daquele semestre…) não são estrutura de edição nenhuma: não os proponha nem os pergunte ao apresentador. O conteúdo e a estrutura de cada deck vêm do material dos apresentadores e da ordem escolhida pelo designer (veja `dr-marca`).

O deck `~/beyond-dr-skills/beyond/beyond/dr/exemplos/dr-07-2026/deck.dr.html` é o DR de julho inteiro refeito. Use os slides dele como ponto de partida e crie composições novas quando o conteúdo pedir, sempre com as mesmas peças.

| Composição | Slide no exemplo | Peças |
|---|---|---|
| Capa / encerramento | 1, 56 | `dr-forma` octógono + `dr-selo` + `dr-topo` com pílulas + `dr-aba-be` |
| Quem apresenta | 2, 6, 15, 22 | `dr-split` (grade + `dr-lado cor` com `dr-forma`), `dr-titulo g`, pílulas de cargo |
| Frase / abertura de bloco | 3, 7, 8, 14 | `dr-titulo frase` + `dr-destaque`, `dr-forma` flor saindo da borda |
| Agenda | 4 | `dr-grid-3` de `dr-pasta` com `dr-lista` |
| Cards de pasta | 11, 40 | `dr-grid-4` de `dr-pasta` (`--fundo`) com ícone |
| Cards retos | 12, 25, 39 | `dr-caixa` de título + `dr-grid-*` de `dr-card` em `lilas-grade` |
| Gráfico de barras | 16, 18 | `dr-grafico` + `dr-barra` (`--v`, `--cor`) + `dr-valores` |
| Número central | 17, 19 | `dr-caixa centro` + `dr-numero` + `dr-nota`, fundo `hachura` |
| Métricas | 47 | `dr-metrica` lado a lado (mesmo tamanho) |
| Fotos com legenda | 23, 26, 43 | `dr-grid-* esticar` de `dr-figura` |
| Texto + imagem | 13, 27, 38, 44 | `dr-corpo` com `dr-texto` + `dr-foto`, ou `dr-split` |
| Comparativo | 34 | `dr-grid-2` de `dr-pasta` com `dr-lista p` |
| Tabela | 35 | `dr-tabela` |
| Lista numerada | 41, 45 | `dr-itens` + `dr-item`, opcional `dr-moldura` com forma e ícone |
| Imagem cheia + caixa | 32, 36 | `dr-preenche` + `dr-caixa` centralizada |
| Abertura de categoria | 48, 50… | `dr-forma` círculo + `dr-area centro inversa`, sem rodapé |
| Vencedor | 49, 51… | `dr-split --div:1128px`, `dr-tag`, `dr-placa`, retrato em `dr-preenche` |

Quando nenhuma peça resolver, **não invente CSS**: componha com o que existe e registre `PARA O DESIGN: …` nas notas. Componente novo entra no `design-system.css` (com comentário `@componente`) e depois `python3 $DR componentes`.

## Erros comuns

- Grid de cards com `esticar`: os cards ficam altos e vazios. `esticar` é para fotos.
- Texto longo em `dr-titulo g`/`frase`: use até ~3 linhas; acima disso, `dr-titulo` normal ou `m`.
- Nome em `dr-aba` muito longo: a aba cresce, mas a pasta precisa ter largura para ela.
- Esquecer o `<div class="dr-fundo"></div>` dentro de um `dr-lado` com `data-fundo` próprio.
