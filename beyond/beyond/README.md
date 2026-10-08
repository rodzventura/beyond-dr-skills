# Beyond (a marca)

Marca Beyond (beyond co.) e o agente de apresentação da **Difusão Recorrente (DR)**, o evento trimestral da empresa.

```
beyond/beyond/
  beyond-brand/        tokens da marca (beyond-tokens.json)
  claude-code/         tudo o que o Claude Code carrega
    skills/
      dr-marca/        guardião da identidade: papel, fixo × livre, briefing, perfis, escrita, números, cor, checklist
      dr-slides/       autocontida: design system (design-system.css), motor, template, scripts/dr.py, COMPONENTES.md,
                       CHANGELOG.md, assets/ (fontes, logos provisórios, selo DR26, ícones pixel)
      dr-montagem/     perfil designer: revisar partes, montar, acabamento, Figma (MCP), proposta de componente
      dr-entrega/      entrega e leitura pela pasta do Drive: estrutura por edição, versões, confirmação antes de enviar
    commands/          /dr-parte (apresentador) e /dr-montar (designer), em opus
  dr/                  projeto: a DR
    agentes/           texto dos dois agentes da plataforma (Apresentação e Montagem)
    exemplos/          dr-07-2026/ (DR de julho refeito: referência de composição) e edicao-exemplo/ (partes + deck montado)
    exploracao/        as 3 direções visuais de 08/out/2026 (histórico)
```

## Dois agentes, mesmas skills

| Agente | Quem usa | Skills | Figma |
|---|---|---|---|
| **DR · Apresentação** | apresentadores e gestores ("minha parte") | `dr-marca`, `dr-slides`, `dr-entrega` | não |
| **DR · Montagem** | designer (revisa, monta, acabamento) | `dr-marca`, `dr-slides`, `dr-montagem`, `dr-entrega` | sim (MCP, só em página de trabalho) |

Os textos para colar na plataforma estão em `dr/agentes/`. O Figma fica só no agente do designer porque o MCP escreve no arquivo.

## Identidade fixa, estrutura livre

O agente é **guardião da identidade e da gramática de slide**; ele não repete a apresentação anterior. A estrutura da edição (blocos, assuntos, formato) nasce do material dos apresentadores e da ordem que o designer escolhe; o que o agente pergunta no início é só quem está falando e o que vai fazer (`dr-marca/entrevista-inicial.md`). O deck de julho é só referência de composição.

Fluxo: cada apresentador gera a sua **parte** (`parte.dr.html`) e a entrega no **Drive** (`dr.py pacote`, versionada) → o designer lê as partes, faz `dr.py montar` (capa, agenda e encerramento gerados) → acabamento no fonte → `dr.py gerar` → entrega o final no Drive. Estrutura da pasta: `DR/<ano>/<Q#>/{material, partes/<bloco>/vN, final/vN}` (o link da pasta vai nas instruções do agente, não no repositório, que é público).

Próximos projetos entram ao lado de `dr/` (por exemplo `lp/`), com o mesmo molde: `claude-code/` para o que o
Claude Code carrega e uma pasta por projeto.

## Como funciona

O deck é um arquivo `.dr.html` com uma `<section class="dr">` por slide. Não há catálogo fechado: o agente compõe cada slide livremente, **só com as classes `dr-*` e os tokens do design system**. O `dr.py verificar` reprova o que sai da identidade (fonte, cor solta, classe estranha, imagem externa, lorem ipsum), e a verificação visual do deck (tecla V) reprova texto que não cabe no container. O `dr.py gerar` produz um HTML único e autocontido: fontes e imagens embutidas, animação, notas, tela sempre ativa e PDF por Cmd+P.

Origem: motor e princípios de um agente de apresentação anterior, adaptados, com identidade fixa e estrutura livre.

## Instalação (symlinks, um por skill)

```bash
R=~/beyond-dr-skills/beyond/beyond/claude-code
ln -s $R/skills/dr-slides ~/.claude/skills/dr-slides
ln -s $R/skills/dr-marca ~/.claude/skills/dr-marca
ln -s $R/skills/dr-montagem ~/.claude/skills/dr-montagem
ln -s $R/skills/dr-entrega ~/.claude/skills/dr-entrega
ln -s $R/commands/dr-parte.md ~/.claude/commands/dr-parte.md
ln -s $R/commands/dr-montar.md ~/.claude/commands/dr-montar.md
```

Requisitos: Python 3 com Pillow (imagens → WebP). Para regenerar fontes: `fonttools` + `brotli`.

## Comandos

```bash
DR=~/beyond-dr-skills/beyond/beyond/claude-code/skills/dr-slides/scripts/dr.py
python3 $DR verificar deck.dr.html
python3 $DR gerar deck.dr.html -o deck.html
python3 $DR pacote parte.dr.html --versao 1 -o saida/   # apresentador: arquivos para o Drive
python3 $DR montar parte-1.dr.html parte-2.dr.html -o deck.dr.html --edicao "Outubro · 2026"   # designer
python3 $DR pendencias deck.dr.html
python3 $DR componentes            # regenera COMPONENTES.md depois de mexer no CSS
```

## Pendências da marca
- Logos oficiais (beyond co., "be.", selo DR26) e dos produtos em SVG.
- Fotos originais do time (as do exemplo foram recortadas dos cards de julho, em baixa resolução).
