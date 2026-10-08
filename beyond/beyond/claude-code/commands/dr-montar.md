---
description: Monta o deck final da Difusão Recorrente (DR) a partir das partes dos apresentadores (perfil designer)
model: opus
argument-hint: "[edição, ex.: outubro 2026]"
---

Você vai **montar o deck final** da **Difusão Recorrente (DR)** com o designer. Leia antes as skills `dr-marca`, `dr-slides` e `dr-montagem` (fluxo completo, regras do Figma e proposta de componente).

Edição: $ARGUMENTS

1. **Conversa inicial** (`dr-marca/entrevista-inicial.md`) e **leia as partes no Drive** (`partes/<bloco>/`, versão mais alta). A ordem dos blocos é do designer; nada vem de edições anteriores.
2. **Revise cada parte:** `dr.py verificar`, tecla V no HTML da parte e o checklist de `dr-marca`. Dê um parecer por parte (pronta · acabamento do design · volta para o apresentador) e liste as inconsistências entre partes.
3. **Monte:** `dr.py montar parte-1.dr.html parte-2.dr.html … -o deck.dr.html --edicao "<mês · ano>"`, depois `dr.py gerar deck.dr.html -o DR-<AAAA-MM>.html`.
4. **Acabamento no arquivo-fonte** (`deck.dr.html`, nunca no HTML gerado), conforme os pedidos do designer. Para telas no Figma, siga as regras de segurança de `dr-montagem` (página de trabalho `DR · <AAAA-MM>`, só estilos do Guide, nunca editar as páginas existentes).
5. **Componente novo** só por proposta (`dr-montagem/propostas/_modelo.md`), nunca CSS solto.
6. **Entregue** no Drive (`final/v<N>/`, skill `dr-entrega`, depois de confirmar) o HTML final, o fonte com `img/` e o relatório (slides, pendências, propostas abertas, versão do design system, frames do Figma).
