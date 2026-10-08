---
name: "dr-entrega"
description: "Use esta skill para entregar e para ler material da Difusão Recorrente (DR) na pasta do Google Drive da edição: estrutura de pastas, versões, confirmação antes de enviar, o que subir (pacote da parte, pré-visualização, pendências) e plano B quando o Drive não responde."
---

# DR · entrega pelo Drive

Tudo da DR trafega por **uma pasta do Google Drive**, organizada por edição (trimestre). Esta skill vale para os dois perfis: o apresentador **entrega a parte** e o designer **lê as partes e entrega o final**.

## A pasta

O link/ID da pasta **raiz `DR`** vem das **instruções do agente** (campo "Pasta de entrega"). Ele não está no repositório de propósito: o repositório é público. Se você não tiver o link, peça ao usuário; **nunca invente nem procure pastas parecidas**.

Dentro da raiz há **uma subpasta por ano** (`2026`) e, dentro dela, **uma por edição, com o nome do trimestre** (`Q1`, `Q3`…). Ache a da edição pelo nome. Se não existir, **peça confirmação para criá-la**.

```
DR/                              ← raiz (link nas instruções do agente)
  2026/                          ← ano
    Q3/                          ← edição = trimestre
      material/<bloco>/          ← opcional: arquivos que o apresentador sobe para você ler
      partes/<bloco>/v1/ v2/ …   ← entrega do apresentador (uma pasta por versão)
      final/v1/ v2/ …            ← entrega do designer
```

`<bloco>` é o nome do bloco em minúsculas, sem acento e com hífen (o `dr.py pacote` usa o mesmo, ex.: `conquistas-do-ano`).

## Entregar a parte (apresentador)

Só entregue quando a pessoa disser **"pode enviar"** (ou equivalente) e depois de **confirmar o resumo**.

1. Rode `dr.py verificar`, `gerar` e a tecla V; resolva os erros. Avisos e pendências vão no relatório.
2. Descubra a próxima versão: olhe `partes/<bloco>/` na pasta da edição; a versão nova é `v<maior+1>` (ou `v1`).
3. `python3 dr.py pacote parte.dr.html --versao N -o saida/` gera quatro arquivos: o zip do fonte com `img/`, a pré-visualização `.html`, as pendências `.md` e o `entrega.json`.
4. **Mostre o resumo e peça o ok**: bloco, quem apresenta, edição, versão, nº de slides, pendências e a pasta de destino. Só depois envie.
5. Crie `partes/<bloco>/v<N>/` (e as pastas que faltarem) e suba os quatro arquivos. **Nunca sobrescreva nem apague** arquivos existentes: cada envio é uma versão nova.
6. Responda com o **link da pasta da versão** e a lista de pendências. Avise que o designer vai encontrar a parte nessa pasta.
7. Se o apresentador subiu arquivos em `material/<bloco>/`, não mexa neles.

## Ler as partes (designer)

1. Na pasta da edição, liste `partes/`. Para cada bloco, use **a versão mais alta** e baixe o zip, o `.md` de pendências e o `entrega.json`.
2. Descompacte cada zip numa pasta própria (o fonte `parte.dr.html` já vem com `img/`).
3. Se faltar bloco que o designer esperava, avise; se houver `v` mais antiga e mais nova, diga qual está usando.

## Entregar o final (designer)

Mesmo cuidado: **resumo, ok, depois envio**. Em `final/v<N>/` suba:
- `DR-<AAAA-MM>.html` (o deck autocontido, `dr.py gerar`);
- `deck-fonte-vN.zip` (`deck.dr.html` + `img/`) para continuar editando;
- `relatorio-vN.md`: slides, blocos e responsáveis, versões das partes usadas, pendências, propostas de componente abertas, versão do design system, links dos frames do Figma.

## Regras

- **Só escreva dentro da pasta `DR` da edição**; nunca em outro lugar do Drive. Não mude permissões nem compartilhamento.
- **Nunca apague** nada, nem versões antigas.
- Dado de receita e fotos de pessoas são **internos**: não cole conteúdo da pasta em outros lugares nem peça para compartilhar o link.
- **Plano B:** se o Drive falhar (sem acesso, erro), diga o motivo e **entregue os arquivos na própria conversa**; o usuário sobe depois.
- Não crie Notion, Slack nem outros avisos sem o usuário pedir.
