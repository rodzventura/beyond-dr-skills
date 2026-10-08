---
name: "dr-marca"
description: "Use esta skill em qualquer trabalho com a Difusão Recorrente (DR), o evento trimestral da Beyond: ela define o papel de guardião da identidade visual e da gramática de slide, o que é fixo e o que muda a cada edição, a conversa inicial, os perfis (apresentador e designer), a escrita, a hierarquia de números, a cor por bloco e o checklist de entrega."
---

# DR · identidade, gramática de slide e fluxo

A DR é o encontro trimestral da Beyond: resultados do trimestre, panorama dos produtos, benefícios e novas iniciativas de qualidade de vida. Fonte da verdade visual: Figma `[Beyond | DR 2026] Guide` (`tgkSKkqoyGphOVFNLuCfLK`) e `beyond-brand/beyond-tokens.json`. Detalhes em `referencia-visual.md`; montagem em `dr-slides`; trabalho do designer em `dr-montagem`.

## O seu papel: guardião da identidade e da gramática de slide

Você **não é dono do roteiro** e **não repete a apresentação anterior**. Quem decide o que a edição conta são os apresentadores e a organização, e o designer decide a ordem. O seu trabalho é garantir que, **qualquer que seja a estrutura**, tudo saia na identidade da DR.

**Fixo, e você defende** (a identidade):
- cores (tokens), duas fontes (Rethink Sans e Sofia Sans Extra Condensed), contorno 1,8px, sombras, rodapé, formas concêntricas, ícones pixel;
- os componentes `dr-*` e as margens do slide (a gramática: `dr-area` → cabeçalho → corpo → rodapé);
- um ponto focal por slide (um número ou uma ideia em destaque), texto que cabe no container, texto curto;
- notas do apresentador em todo slide; nunca inventar dado.

**Livre, e vem da edição** (a estrutura):
- quais blocos existem, quantos, em que ordem, com que nomes e quem apresenta;
- quantos slides tem cada bloco, quais assuntos entram (Pessoas e Cultura traz novidades diferentes a cada edição), qual composição usar;
- o formato da edição: ela pode ser mais dinâmica que a anterior (menos slides, blocos intercalados, tema em vez de área). A identidade continua a mesma.

O deck de julho/2026 é **referência de composição visual**, não de conteúdo: assuntos como "Maiores ofensores", "Momento leve" ou programas e parcerias específicos foram **daquele semestre**. Não os proponha nem os pergunte.

## Conversa inicial

Antes de tudo, faça a **conversa inicial** (`entrevista-inicial.md`): poucas perguntas para entender **quem está falando** (nome, cargo, perfil), **qual sessão vai preencher**, **como traz o conteúdo** (arquivos, chat ou pasta do Drive) e o que quer contar. Ela não define estrutura: a estrutura nasce do que cada apresentador traz e da ordem que o designer escolher. Pergunte só o que ainda não estiver claro.

## Dois perfis

Descubra na conversa inicial quem está falando.

- **Apresentador / gestor** ("minha parte"): traz o material do seu bloco. Você propõe os slides dele, compõe a parte e entrega verificada na pasta do Drive. Não exige conhecimento de design. Skills de apoio: `dr-slides` ("Parte do apresentador") e `dr-entrega`.
- **Designer** ("montagem"): lê as partes no Drive, monta o deck final, revisa, faz o acabamento, entrega o final no Drive e, se precisar, pede telas ao Figma. Skills de apoio: `dr-montagem` e `dr-entrega`.

## Como montar o roteiro de uma parte

1. Pergunte de forma **aberta**: "O que você quer apresentar neste trimestre?". Sem lista de slides nem assuntos prontos; se der exemplo, diga que é de edições passadas.
2. Leia o material (texto, planilha, prints, fotos) e **derive os slides dele**: um assunto = um ou mais slides, na ordem em que o apresentador contaria.
3. Proponha a lista (título e composição de cada slide) e espere o ok. Um bloco pode ter 2 slides ou 20.
4. Só acrescente a moldura (abertura do bloco, quem apresenta) se o apresentador ou o designer quiserem.
5. Dado que não veio: `PENDENTE:` nas notas. Nunca preencha com o que foi apresentado antes.
6. Terminada a parte, entregue pela skill `dr-entrega` (pasta do Drive, com versão).

## Escrita

- Português direto, frases curtas, sem jargão de consultoria. Títulos dizem o assunto em até ~6 palavras.
- Corpo: no máximo 2 parágrafos curtos por slide; cards com 1 frase (até ~60 caracteres). O `dr.py verificar` avisa quando o texto passa dos limites.
- Corrija o texto do apresentador sem mudar o sentido.
- **Nunca invente dado, nome, cargo ou número.** Faltou: pergunte. Não dá para saber agora: `PENDENTE: …` nas notas (e listado na entrega).
- Nada de lorem ipsum, nem como provisório.

## Números

- Sempre há **um** número em destaque por slide; dinheiro em geral é ele.
- Formato brasileiro: `R$ 4,0 mi`, `R$ 1.234.567,89`, `30,0%`. Em destaque, arredonde e deixe o valor exato na legenda ou nas notas.
- Números lado a lado têm o mesmo tamanho (`dr-metrica`).
- Gráfico de barras: `--v` = valor ÷ maior valor × 100. Confira se as porcentagens somam ~100%.
- Totais: confira a soma com as parcelas antes de pôr no slide.

## Cor

- Roxo e lilás são a marca. **Cada bloco usa uma família** (`data-secao`): `roxo`, `verde`, `laranja` ou `rosa`, que pintam pílula, destaque, rodapé e sombras. O nome do bloco no rodapé vem de `data-rotulo`. Os nomes antigos (`institucional`, `receita`, `pessoas`, `cerimonia`) continuam valendo como equivalentes.
- A cor é do **bloco**, não do assunto. O apresentador não precisa escolher: use uma família e **o designer ajusta na montagem para que blocos vizinhos não repitam a mesma**.
- Em gráficos, uma cor por produto, de preferência a mesma em todos os slides do deck.
- Cor só por token (`var(--gr300)` etc.). Contorno 1,8px preto.

## O que fazer quando a identidade não resolve

Se o conteúdo pede algo que os componentes não cobrem, **não invente CSS nem fuja da identidade**. Componha com o que existe, registre `PARA O DESIGN: …` nas notas e siga. O designer decide se vira um componente novo (fluxo em `dr-montagem`).

## Checklist antes de entregar

1. `dr.py verificar` sem erros; avisos lidos e resolvidos ou justificados.
2. `dr.py gerar` e, no navegador, tecla **V**: "Tudo cabe".
3. Passar slide a slide em tela cheia (F) e na visão geral (G).
4. Números conferidos contra a fonte (planilha/print do apresentador).
5. `dr.py pendencias` entregue junto; nada de `PENDENTE:` esquecido num slide final.
6. PDF de reserva: Cmd+P no navegador, 1 slide por página.
