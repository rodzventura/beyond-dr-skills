# Componentes do design system DR

Gerado por `dr.py componentes` a partir de `design-system.css`. Não editar à mão.

## Slide

`<section class="dr" data-secao="…" data-fundo="…">` · seções: cerimonia, institucional, laranja, marca, pessoas, premio, receita, rosa, roxo, verde · fundos: branco, clara, cor, escuro, grade, hachura, lilas, lilas-grade, nevoa.

Modificadores aceitos (sem prefixo): `base`, `centro`, `cheia`, `coluna`, `contida`, `cor`, `escura`, `esticar`, `frase`, `g`, `gira`, `inversa`, `m`, `meio`, `numerada`, `p`, `q`, `recorte`, `sec`, `sem-borda`, `sem-sombra`, `viva`.

Em `style` só entram tokens (`--cor:var(--gr300)`, `--v:92.4`, `--fundo:var(--or300)`, `--n:300px`) e propriedades de layout: align-items, align-self, flex, gap, grid-column, grid-row, height, justify-content, justify-self, margin-top, max-width, min-height, order, text-align, width.

## Componentes

- seção (data-secao no <section>) · família de cor do slide. Genéricas: roxo | verde | laranja | rosa (para qualquer bloco; dê o nome no rodapé com data-rotulo). Nomeadas (equivalentes): institucional=roxo, receita=verde, pessoas=laranja, cerimonia=rosa, premio=roxo com destaque rosa, marca=capas e agenda.
- fundo · data-fundo no <section>: branco | grade | nevoa | lilas | lilas-grade | hachura | cor | clara | escuro
- rodapé · gerado pelo motor; data-rodape="nenhum" no <section> desliga, data-rotulo troca o nome da seção
- dr-area · a caixa de conteúdo do slide (margens 120, topo 96, acima do rodapé). Tudo que é texto mora aqui dentro.
- dr-corpo · ocupa o espaço que sobra abaixo do cabeçalho
- dr-grid-2/3/4/5 · colunas iguais
- dr-split · tela dividida em dois lados (--div = largura do 1º lado, padrão 55%). O lado com .cor usa o fundo claro da seção.
- dr-topo · faixa no alto do slide com itens nas pontas (ex.: pílulas da capa)
- dr-cab · cabeçalho: pílula/kicker + título
- dr-titulo · título do slide (Rethink 600, 96px). Variações: .g (gigante 168) · .frase (150, para frases de impacto) · .m (64)
- dr-destaque · trecho realçado dentro de título (caixa com contorno na cor de destaque da seção)
- dr-valores · lista curta de valores ao lado de um gráfico (produto + valor por linha)
- dr-sub · subtítulo (44px) · dr-texto · corpo (32px) · dr-legenda · apoio (24px) · dr-kicker · rótulo curto na cor da seção
- dr-pilula · etiqueta com contorno. Com <i class="dr-ponto"></i> mostra a bolinha da seção. .cheia = fundo da cor viva
- dr-numero · número grande com unidades menores: <div class="dr-numero"><span class="dr-u">R$</span><span data-conta="4,0">4,0</span><span class="dr-u">mi</span></div>. Tamanho por --n (padrão 400px).
- dr-metrica · número médio + legenda, para 2–4 números lado a lado (mesmo tamanho)
- dr-caixa · caixa reta com contorno e sombra deslocada (estilo editorial). .sem-sombra · .escura
- dr-nota · caixinha de observação colada no canto de outra caixa
- dr-card · card reto, fundo creme, ícone + texto
- dr-pasta · card em forma de pasta com aba e sombra dura. Cor por --fundo (padrão: cor viva da seção). .inversa = texto branco
- dr-item · linha em caixa arredondada com número e sombra dura na cor da seção
- dr-moldura · moldura arredondada com sombra da seção, para formas/ícone/imagem
- dr-lista · lista com fios entre itens (3–7 itens). .numerada mostra 01, 02…
- dr-tabela · tabela reta com cabeçalho escuro
- dr-grafico · painel reto com barras verticais. Cada barra: <div class="dr-barra" style="--v:83.3;--cor:var(--p400)"><b>25,0%</b><span>Beta</span></div> (--v = altura relativa à maior, 0–100)
- dr-foto · imagem com contorno, recortada para preencher (object-fit). Enquadramento: style="--foco:50% 20%" no .dr-foto ou .dr-preenche (ponto da imagem que fica no centro). .contida = sem cortar · .sem-borda · .recorte = pessoa recortada apoiada na base
- dr-figura · foto + legenda abaixo
- dr-preenche · imagem que cobre todo o slide ou todo o lado
- dr-pedido · imagem que ainda falta: o design substitui. data-pedido="descrição"
- dr-forma · formas concêntricas (svg). data-forma: circulo | flor | estrela | octogono; data-cores (fora→dentro); data-n camadas; data-r raio; data-cx/cy (padrão: centro do pai); data-rmin
- dr-selo · selo DR26 · dr-aba-be · aba "be." na base · dr-logo · wordmark beyond co. · dr-icone · ícone pixel (data-ic)
- dr-tag-quadro · ícone dentro de quadrado na cor forte (ex.: Beyond The Best)
- dr-placa · fundo branco atrás de texto que fica sobre grade/forma
- dr-area.inversa · texto branco (sobre forma ou fundo escuro)

## Tokens de cor

`gr100`, `gr200`, `gr300`, `gr400`, `gym-red`, `gym-yellow`, `n100`, `n200`, `n300`, `n400`, `n500`, `n600`, `or100`, `or200`, `or300`, `or400`, `p100`, `p1000`, `p1050`, `p200`, `p300`, `p400`, `p500`, `p600`, `p700`, `p800`, `p900`, `pk100`, `pk200`, `pk300`, `pk400`
