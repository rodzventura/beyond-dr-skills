# Beyond · skills da Difusão Recorrente (DR)

Skills, comandos e textos de agentes para montar a apresentação da **Difusão Recorrente (DR)**, o evento trimestral da Beyond, sempre na mesma identidade visual. O agente é **guardião da identidade e da gramática de slide**: a estrutura de cada edição é livre, a identidade não.

Todo conteúdo de exemplo deste repositório é **fictício** (pessoas, produtos, clientes, programas e números).

## Importar na plataforma de agentes

Importe **cada skill pela pasta dela** (`Repositório` = `rodzventura/beyond-dr-skills`):

| Skill | Pasta da skill | Agente |
|---|---|---|
| `dr-marca` | `beyond/beyond/claude-code/skills/dr-marca` | Apresentação e Montagem |
| `dr-slides` | `beyond/beyond/claude-code/skills/dr-slides` | Apresentação e Montagem |
| `dr-entrega` | `beyond/beyond/claude-code/skills/dr-entrega` | Apresentação e Montagem |
| `dr-montagem` | `beyond/beyond/claude-code/skills/dr-montagem` | só Montagem (designer) |

Os textos para colar no campo de instruções de cada agente estão em [`beyond/beyond/dr/agentes/`](beyond/beyond/dr/agentes/). O **link da pasta do Drive não está aqui**: ele vai só nas instruções do agente na plataforma.

## Mais detalhes

[`beyond/beyond/README.md`](beyond/beyond/README.md): estrutura, os dois agentes, o fluxo (parte → Drive → montagem → final), comandos do `dr.py` e instalação no Claude Code.

Requisitos para rodar o `dr.py`: Python 3 com Pillow (`pip install pillow`).

## Exemplos

Os exemplos em `beyond/beyond/dr/exemplos/` referenciam imagens em `img/`, que **não ficam no repositório** (fotos de pessoas). Para rodar `dr.py verificar` ou `gerar` neles, coloque imagens com esses nomes ou troque os `src` por imagens suas. Servem de referência de **composição**, não de conteúdo.
