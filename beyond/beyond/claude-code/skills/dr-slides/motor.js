/* DR · motor do deck (v1)
   Monta cada <section class="dr">: fundo, rodapé, formas concêntricas, ícones, logos, imagens embutidas.
   Animação de entrada (CSS padrão = estado final) · navegação · visão geral · notas · tela ativa · verificação · PDF.
   Teclas: ← → espaço clique navegam · F tela cheia · G visão geral · N notas · R repete · V verifica · Home/End */
(function () {
  const ICONES = window.DR_ICONES || {};
  const IMAGENS = JSON.parse((document.getElementById('dr-imagens') || {}).textContent || '{}');
  /* nomes padrão do rodapé; nas famílias genéricas (roxo, verde, laranja, rosa) o nome vem de data-rotulo */
  const ROTULOS = { marca: 'Difusão Recorrente', cerimonia: 'Cerimônia', institucional: 'Institucional', receita: 'Receita', pessoas: 'Pessoas e Cultura', premio: 'Beyond The Best' };
  const RODAPE = document.body.dataset.rodape || 'DR Beyond 2026';
  const COR = n => n.startsWith('var(') ? n : `var(--${n})`;
  const palco = document.getElementById('palco'), fit = document.getElementById('fit');
  const slides = [...palco.querySelectorAll('section.dr')];

  /* ---------- formas concêntricas ---------- */
  function raio(tipo, R, t) {
    if (tipo === 'flor') return R * (1 + .11 * Math.cos(4 * (t - Math.PI / 4)));
    if (tipo === 'estrela') { const p = .78, c = Math.abs(Math.cos(t)), q = Math.abs(Math.sin(t)); return R / Math.pow(Math.pow(c, p) + Math.pow(q, p), 1 / p); }
    if (tipo === 'octogono') { const s = Math.PI / 8, ro = R / Math.cos(((t + s) % (2 * s)) - s); return .78 * ro + .22 * R * 1.04; }
    return R;
  }
  function caminho(tipo, cx, cy, R) {
    let d = '';
    for (let k = 0, N = 240; k <= N; k++) { const t = k / N * 2 * Math.PI, r = raio(tipo, R, t); d += (k ? 'L' : 'M') + (cx + r * Math.cos(t)).toFixed(1) + ' ' + (cy + r * Math.sin(t)).toFixed(1); }
    return d + 'Z';
  }
  function forma(svg) {
    const pai = svg.parentElement, W = pai.offsetWidth || 1920, H = pai.offsetHeight || 1080;
    const tipo = svg.dataset.forma || 'circulo', cx = +(svg.dataset.cx || W / 2), cy = +(svg.dataset.cy || H / 2),
      R = +(svg.dataset.r || Math.hypot(W, H) / 2), n = +(svg.dataset.n || 1), rmin = +(svg.dataset.rmin || .3),
      cores = (svg.dataset.cores || 'p300,p600,p400,p300,n100').split(',');
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    let h = '';
    for (let i = 0; i < n; i++) {
      const r = n === 1 ? R : R * (1 - i * (1 - rmin) / (n - 1));
      const st = `style="fill:${COR(cores[i % cores.length])};--i:${i};transform-origin:${cx}px ${cy}px"`;
      h += tipo === 'circulo' ? `<circle class="cam" cx="${cx}" cy="${cy}" r="${r}" ${st}/>` : `<path class="cam" d="${caminho(tipo, cx, cy, r)}" ${st}/>`;
    }
    svg.innerHTML = h;
  }

  /* ---------- montagem de cada slide ---------- */
  function monta(s, i) {
    const f = document.createElement('div'); f.className = 'dr-fundo'; s.prepend(f);
    if (/lilas-grade|escuro/.test(s.dataset.fundo || '')) { const g = document.createElement('div'); g.className = 'dr-grao'; s.append(g); }
    if (s.dataset.rodape !== 'nenhum') {
      const r = document.createElement('div'); r.className = 'dr-rodape';
      r.innerHTML = `<span>${RODAPE}</span><span class="sec">${s.dataset.rotulo || ROTULOS[s.dataset.secao] || ''}</span><span class="fim">›</span>`;
      s.append(r);
    }
    s.querySelectorAll('img[data-src]').forEach(im => { im.src = IMAGENS[im.dataset.src] || ''; });
    s.querySelectorAll('[data-ic]').forEach(el => { el.classList.add('dr-icone'); el.innerHTML = `<svg viewBox="0 0 24 24" shape-rendering="crispEdges"><path fill="currentColor" d="${ICONES[el.dataset.ic] || ''}"/></svg>`; });
    s.querySelectorAll('.dr-selo,.dr-aba-be,.dr-logo').forEach(el => { const t = el.classList.contains('dr-selo') ? 'selo' : el.classList.contains('dr-aba-be') ? 'aba' : 'co'; el.innerHTML = document.getElementById('tpl-' + t).innerHTML; });
    s.querySelectorAll('[data-pedido]').forEach(el => { el.classList.add('dr-pedido'); if (!el.textContent.trim()) el.textContent = 'Imagem pendente · ' + el.dataset.pedido; });
    s.querySelectorAll('.dr-barra').forEach((b, k) => b.style.setProperty('--k', k));
    palavras(s);
    let k = 0; s.querySelectorAll('[data-a]').forEach(el => el.style.setProperty('--d', (120 + k++ * 90) + 'ms'));
    s.id = 's' + (i + 1);
  }
  function palavras(raiz) {
    raiz.querySelectorAll('[data-a=palavras]').forEach(el => {
      let w = 0;
      const anda = n => [...n.childNodes].forEach(c => {
        if (c.nodeType === 3) {
          const fr = document.createDocumentFragment();
          c.textContent.split(/(\s+)/).forEach(p => { if (!p) return; if (/^\s+$/.test(p)) fr.append(p); else { const sp = document.createElement('span'); sp.className = 'pal'; sp.style.setProperty('--w', w++); sp.textContent = p; fr.append(sp); } });
          c.replaceWith(fr);
        } else if (c.nodeType === 1 && c.tagName !== 'BR' && !c.classList.contains('dr-destaque')) anda(c);
      });
      anda(el);
    });
  }
  function conta(s) {
    s.querySelectorAll('[data-conta]').forEach(el => {
      const txt = el.dataset.conta, alvo = parseFloat(txt.replace(/\./g, '').replace(',', '.')), dec = (txt.split(',')[1] || '').length, t0 = performance.now();
      const fmt = v => v.toLocaleString('pt-BR', { minimumFractionDigits: dec, maximumFractionDigits: dec });
      const passo = t => { const p = Math.min(1, (t - t0) / 1400); el.textContent = fmt(alvo * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(passo); else el.textContent = txt; };
      requestAnimationFrame(passo);
    });
  }
  const tocar = s => { s.classList.remove('run'); void s.offsetWidth; s.classList.add('run'); conta(s); };
  const desenha = () => slides.forEach(s => { s.classList.add('on'); s.querySelectorAll('svg.dr-forma').forEach(forma); s.classList.remove('on'); });

  slides.forEach(monta);

  /* ---------- navegação ---------- */
  let atual = -1;
  function ajusta() {
    const k = Math.min(innerWidth / 1920, innerHeight / 1080);
    fit.style.transform = `translate(-50%,-50%) scale(${k})`;
    document.documentElement.style.setProperty('--kg', (Math.min(innerWidth - 80, 1760) / 4 - 24) / 1920);
  }
  function mostra(i, animar = true) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, j) => s.classList.toggle('on', j === i));
    if (i !== atual && animar) tocar(slides[i]);
    atual = i;
    history.replaceState(null, '', '#' + (i + 1));
    document.getElementById('pg').textContent = `${i + 1} / ${slides.length}`;
    const n = slides[i].querySelector('.dr-notas'); document.getElementById('notas').innerHTML = n ? n.innerHTML : '<em>Sem notas neste slide.</em>';
  }
  const visao = on => document.body.classList.toggle('geral', on);
  addEventListener('keydown', e => {
    const k = e.key.toLowerCase();
    if (k === 'arrowright' || k === 'pagedown' || k === ' ') { e.preventDefault(); mostra(atual + 1); }
    else if (k === 'arrowleft' || k === 'pageup') mostra(atual - 1);
    else if (k === 'home') mostra(0);
    else if (k === 'end') mostra(slides.length - 1);
    else if (k === 'f') document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
    else if (k === 'g' || k === 'escape') visao(k !== 'escape' && !document.body.classList.contains('geral'));
    else if (k === 'n') document.body.classList.toggle('com-notas');
    else if (k === 'r') tocar(slides[atual]);
    else if (k === 'v') { const p = verificar(); console.table(p); alert(p.length ? p.map(x => `Slide ${x.slide}: ${x.erro} — "${x.txt}"`).join('\n') : 'Tudo cabe: nenhum texto fora do container, da área ou embaixo do rodapé.'); }
  });
  fit.addEventListener('click', e => {
    if (document.body.classList.contains('geral')) { const s = e.target.closest('section.dr'); if (s) { visao(false); atual = -1; mostra(slides.indexOf(s)); } return; }
    mostra(e.clientX < innerWidth / 5 ? atual - 1 : atual + 1);
  });
  addEventListener('resize', ajusta);

  /* ---------- verificação: todo texto dentro do seu container, da área e acima do rodapé ---------- */
  const CONTAINERS = '.dr-aba,.dr-area,.dr-topo,.dr-caixa,.dr-card,.dr-pasta,.dr-item,.dr-pilula,.dr-nota,.dr-grafico,.dr-placa,.dr-tabela,.dr-moldura,.dr-tag,.dr-figura,.dr-barra';
  const folhas = raiz => [...raiz.querySelectorAll('*')].filter(el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && !el.closest('.dr-rodape,svg,.dr-notas,.dr-pedido'));
  function verificar() {
    const probs = [], geral = document.body.classList.contains('geral');
    if (geral) visao(false);
    slides.forEach((s, i) => {
      const on = s.classList.contains('on'), run = s.classList.contains('run');
      s.classList.add('on'); s.classList.remove('run');
      const R = s.getBoundingClientRect(), rod = s.querySelector('.dr-rodape'), lim = rod ? rod.getBoundingClientRect().top : R.bottom;
      /* tolerância vertical: a caixa de uma palavra é mais alta que a linha em títulos de entrelinha justa */
      const fora = (a, b, tv = 1) => a.left < b.left - 1 || a.right > b.right + 1 || a.top < b.top - tv || a.bottom > b.bottom + tv;
      const add = (el, erro) => probs.push({ slide: i + 1, txt: el.textContent.trim().replace(/\s+/g, ' ').slice(0, 40), erro });
      folhas(s).forEach(el => {
        const r = el.getBoundingClientRect(); if (!r.width) return;
        const tv = Math.max(2, parseFloat(getComputedStyle(el).fontSize) * 0.22 * (R.width / 1920));
        if (fora(r, R, tv)) return add(el, 'fora do slide');
        if (r.bottom > lim + tv) return add(el, 'invade o rodapé');
        const c = el.matches(CONTAINERS) ? el.parentElement.closest(CONTAINERS + ',.dr-area') : el.parentElement.closest(CONTAINERS);
        if (!c) return add(el, 'texto solto (fora de dr-area/container)');
        if (el.matches('.dr-aba')) return; /* a aba fica acima da pasta de propósito; o texto dela é checado abaixo */
        const alvo = el.matches('.dr-nota') ? el.closest('.dr-area') : c;
        if (alvo && fora(r, alvo.getBoundingClientRect(), tv)) add(el, 'fora do container ' + [...alvo.classList].find(x => x.startsWith('dr-')));
      });
      s.querySelectorAll('.dr-aba').forEach(ab => { if (ab.scrollWidth > ab.clientWidth + 1) add(ab, 'texto maior que a aba da pasta'); });
      s.querySelectorAll('.dr-nota').forEach(n => { const a = n.closest('.dr-area'); if (a && fora(n.getBoundingClientRect(), a.getBoundingClientRect())) add(n, 'nota sai da dr-area'); });
      s.querySelectorAll('.dr-area').forEach(a => { if (a.scrollHeight > a.clientHeight + 2 || a.scrollWidth > a.clientWidth + 2) add(a, 'conteúdo maior que a dr-area'); });
      s.classList.toggle('on', on); if (run) s.classList.add('run');
    });
    if (geral) visao(true);
    return probs;
  }

  /* ---------- tela sempre ativa ---------- */
  let trava = null;
  const acorda = async () => { try { if ('wakeLock' in navigator && !trava) { trava = await navigator.wakeLock.request('screen'); trava.addEventListener('release', () => trava = null); } } catch (_) {} };
  addEventListener('click', acorda); addEventListener('keydown', acorda);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') acorda(); });

  /* PDF: tudo no estado final */
  addEventListener('beforeprint', () => slides.forEach(s => s.classList.remove('run')));

  document.fonts.ready.then(() => { desenha(); ajusta(); mostra((parseInt(location.hash.slice(1)) || 1) - 1); acorda(); });
  window.DR = { mostra, tocar, slides, visao, verificar };
})();
