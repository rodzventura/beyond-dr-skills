# Figma ↔ design system DR

Arquivo: **[Beyond | DR 2026] Guide** · fileKey `tgkSKkqoyGphOVFNLuCfLK` · status Concluído.

## Páginas (somente leitura)
| Página | Nó | Conteúdo |
|---|---|---|
| ● Cover | `0:1` | capa do guia |
| ◆ Style guide | `1:22` | paleta, tipografia, padrões concêntricos (estrela, pinçado, círculos, octógono) |
| ✦ Apresentação assets e templates | `80:24` | slides de referência (capas, vencedor, cards, rodapés Light/Dark), logos, ícones |
| ▲ Posts, ■ Interno | `24:914`, `206:71` | outros materiais |

Página de trabalho (a única em que se escreve): `DR · <AAAA-MM>`.

## Cores: estilos do Figma → tokens do CSS
| Estilo no Figma | Token | Hex |
|---|---|---|
| Purple variation/100 … 1050 | `--p100 … --p1050` | `#FCFAFF #F6EFFF #F0E9FF #CBB7F7 #A880FF #834AFF #6937D7 #6334C9 #3B1099 #311371 #1A0743` |
| Pink variations/100 … 400 | `--pk100 … --pk400` | `#FEF8FF #DB9BE8 #C418E8 #600C72` |
| Orange variations/100 … 400 | `--or100 … --or400` | `#FFFBF7 #FFE7D0 #FF8C22 #2F1B09` |
| Green variations/100 … 400 | `--gr100 … --gr400` | `#FDFFFC #E0FFD2 #75DB42 #163A0C` |
| Neutral colors/100 … 600 | `--n100 … --n600` | `#FFFFFF #E6E6E6 #CFCFCF #B5B5B5 #696969 #000000` |
| Gym Rats/Red · Yellow · Dark | `--gym-red · --gym-yellow` | `#FF0004 #FDC00E` |

Famílias de bloco: `roxo` = Purple (forte 900, viva 600, clara 400, fundo 300) · `verde` = Green · `laranja` = Orange · `rosa` = Pink.

## Tipografia e traço
- **Rethink Sans** (Regular, Medium, SemiBold, Bold, ExtraBold): títulos 600, corpo 500. **Sofia Sans Extra Condensed**: só números de lista numerada. Nenhuma outra fonte.
- Contorno **1,8px** preto. Efeito de sombra: estilo **"Sombra"** (y 11,8; blur 23,7; preto 50%).
- Palco **1920×1080**; margens 120; rodapé 46px.

## Componentes ↔ o que desenhar
| Componente `dr-*` | No Figma |
|---|---|
| `dr-pasta` | card com aba e sombra dura (12px) na cor viva do bloco |
| `dr-card` | card reto creme (`Orange variations/100`), contorno 1,8px, sombra 16px |
| `dr-caixa`, `dr-grafico` | caixa reta branca, contorno 1,8px em `Purple variation/1050`, sombra deslocada |
| `dr-forma` | camadas concêntricas (círculo, flor, estrela, octógono) com contorno preto |
| `dr-rodape` | "Rodapé Light" / "Rodapé Dark" da página `✦ Apresentação assets e templates` |
| `dr-selo`, `dr-aba-be`, logos | componentes da página de assets |
