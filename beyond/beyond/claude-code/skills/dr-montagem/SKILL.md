---
name: "dr-montagem"
description: "Use esta skill quando quem fala é o designer da Difusão Recorrente (DR): receber as partes dos apresentadores, montar o deck final, revisar a consistência, fazer o acabamento no arquivo-fonte, pedir telas ao Figma via MCP e propor componentes novos ao design system sem sair da identidade."
---

# DR · montagem (perfil designer)

Você apoia o designer que fecha a apresentação da DR. Valem as regras de `dr-marca` (guardião da identidade; estrutura livre) e a ferramenta de `dr-slides`. Aqui está o que é específico do designer.

## 1. Receber e revisar as partes

Faça antes a **conversa inicial** (`dr-marca/entrevista-inicial.md`). As partes chegam **pelo Drive** (skill `dr-entrega`): leia `partes/<bloco>/` da pasta da edição e use a **versão mais alta** de cada bloco. Cada pacote traz o fonte com `img/` (zip), a pré-visualização e as pendências. Descompacte e, para cada parte:

1. `dr.py verificar parte.dr.html`. Erros voltam ao apresentador com a lista exata do que mudar; avisos de texto longo você resolve ou devolve.
2. Abra o HTML da parte e rode a tecla **V**.
3. Revise com o checklist de `dr-marca` e procure **inconsistências entre partes**: o mesmo número com formatos diferentes, o mesmo assunto com nomes diferentes, cores repetidas em blocos vizinhos, densidade muito diferente entre blocos, tom de escrita destoando.
4. Responda com um parecer por parte: **pronta** · **acabamento do design** · **volta para o apresentador** (com a lista do que pedir). Não corrija o conteúdo do apresentador por conta própria: dado, nome e número são dele.

## 2. Montar o deck final

A ordem dos blocos é **do designer**: proponha pela ordem de entrega e ajuste ao que ele pedir. Os nomes vêm do cabeçalho de cada parte; nada vem de edições anteriores.

```bash
python3 $DR montar parte-1.dr.html parte-2.dr.html parte-3.dr.html -o deck.dr.html --edicao "Outubro · 2026"
# opções: --sem-capa  --sem-agenda  --sem-encerramento  --titulo "…"  --rodape "…"
python3 $DR gerar deck.dr.html -o DR-<AAAA-MM>.html
```

O `montar` gera capa, agenda (a partir de `data-agenda` e do cabeçalho `dr:parte` de cada parte) e encerramento, e acerta o caminho das imagens. Com mais de 4 blocos a agenda não é gerada: componha à mão com `dr-pasta` e registre `PARA O DESIGN:`. Se o formato da edição pedir outra moldura (sem agenda, abertura diferente), use as flags ou componha no `deck.dr.html`.

## 3. Acabamento: sempre no arquivo-fonte

Edite `deck.dr.html`, **nunca o HTML gerado** (ele é refeito a cada `gerar` e perderia a mudança). Pedidos típicos, em linguagem natural:

- trocar um `data-pedido="…"` pela imagem final (`<img src="img/…" alt="…">`);
- enquadrar uma foto: `style="--foco:50% 20%"` no `.dr-foto` ou `.dr-preenche`;
- reordenar slides, dividir ou juntar, trocar a composição, ajustar `data-fundo`;
- mudar a cor de um bloco (`data-secao`) respeitando "sem repetir em blocos vizinhos";
- levantar o que falta: `dr.py pendencias deck.dr.html`.

Depois de cada rodada: `verificar`, `gerar` e tecla **V**. Mostre o que mudou.

## 4. Figma (via MCP)

O arquivo **[Beyond | DR 2026] Guide** (`tgkSKkqoyGphOVFNLuCfLK`) é a fonte da identidade. Tokens, estilos e páginas em `figma-estilos.md`. Antes de qualquer escrita, carregue a skill `figma-use` do plugin do Figma (ela é pré-requisito do `use_figma`).

**Regras de segurança (valem sempre):**
- **Nunca edite as páginas existentes** do Guide (`● Cover`, `◆ Style guide`, `✦ Apresentação assets e templates`, `▲ Posts`, `■ Interno`). Elas são a referência.
- **Escreva só numa página de trabalho nova**, com o nome `DR · <AAAA-MM>` (crie-a se não existir). Antes de escrever, confirme com o designer o arquivo e a página.
- Use **só os estilos do Guide** (cores por estilo, não hex; Rethink Sans e Sofia Sans Extra Condensed; efeito "Sombra"; contorno 1,8px). Frames de **1920×1080**.

**Do deck para o Figma** ("crie no Figma o slide X"): leia a `<section>` do slide, monte o frame de 1920×1080 na página de trabalho, com as mesmas peças do slide (rodapé como no template "Rodapé Light"/"Rodapé Dark" da página de assets), e devolva o link do frame.

**Do Figma para o deck** ("traga esta tela para o deck"): leia o frame (`get_design_context`, `get_screenshot`) e **recomponha com os componentes `dr-*`**; não copie o CSS gerado pelo Figma. Se os componentes não alcançarem o que o frame mostra, abra uma proposta (seção 5).

## 5. Componente novo: proposta, nunca CSS solto

Quando um conteúdo não cabe nos componentes:

1. Componha com o que existe e registre `PARA O DESIGN: <o que faltou>`.
2. Se o designer quiser resolver, escreva a proposta em `propostas/<nome>.md` seguindo `propostas/_modelo.md` (descrição, onde apareceu, frame do Figma, HTML de uso com classes `dr-*`, CSS só com tokens, limites de texto).
3. O designer aprova ou recusa. Aprovada, a proposta é **entregue ao responsável pelo repositório** para entrar no `design-system.css` (com comentário `@componente`, versão nova e entrada no `CHANGELOG.md`). Até lá, a edição segue com a composição provisória.
4. Você **não altera o design system** por conta própria nem põe CSS no deck.

## 6. Entrega final

- `DR-<AAAA-MM>.html` (autocontido) e o pacote do fonte (`deck.dr.html` + `img/`), **entregues no Drive** em `final/v<N>/` pela skill `dr-entrega`.
- Relatório: total de slides, blocos e responsáveis, pendências (`dr.py pendencias`), propostas de componente abertas, versão do design system (`<meta name="dr-design-system">`), links dos frames criados no Figma.
- PDF de reserva: Cmd+P no navegador do computador do evento (1 slide por página); confirme que o computador do evento abre o HTML offline.
