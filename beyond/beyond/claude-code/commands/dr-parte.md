---
description: Monta a parte de um apresentador da Difusão Recorrente (DR) da Beyond, na identidade da DR
model: opus
argument-hint: "[bloco e edição, ex.: Receita · outubro 2026]"
---

Você vai montar **a parte de um apresentador** da **Difusão Recorrente (DR)**, o evento trimestral da Beyond. Leia antes as skills `dr-marca` (você é guardião da identidade; a estrutura é livre) e `dr-slides` (formato, design system, seção "Parte do apresentador").

Pedido: $ARGUMENTS

1. **Conversa inicial** (`dr-marca/entrevista-inicial.md`): quem é a pessoa, qual sessão vai preencher e como traz o conteúdo (arquivos, chat ou Drive). Pergunte só o que faltar, numa mensagem curta.
2. **Pergunte de forma aberta** o que a pessoa quer apresentar neste trimestre e peça o material (textos, planilhas, prints, fotos). A estrutura de slides **não é fixa**: não liste assuntos de edições passadas.
3. **Derive os slides do material** e proponha a lista (título e composição de cada slide). Espere o ok.
4. **Componha** `parte.dr.html` com o cabeçalho `dr:parte`, só com classes `dr-*` e tokens, `data-agenda` nos slides que entram na agenda, notas em todos. Imagens em `img/`. Nunca invente dado: `PENDENTE:` e `data-pedido`.
5. **Verifique e gere:** `python3 ~/beyond-dr-skills/beyond/beyond/claude-code/skills/dr-slides/scripts/dr.py verificar parte.dr.html` e `… gerar parte.dr.html -o parte.html`. Abra o HTML, tecla V até dar "Tudo cabe", passe pelos slides.
6. **Entregue** pela skill `dr-entrega`: `dr.py pacote` e envio à pasta do Drive da edição, depois de confirmar com a pessoa.
