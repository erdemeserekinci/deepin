(function(){
'use strict';
const Q = new URLSearchParams(location.search);
if (Q.get('tur') !== '1') return;
const KARE = Q.get('kare') === '1';
const TEMIZ = Q.get('temiz') === '1';
const TURLAR = window.__TURLAR || {};
const SENARYO_AD = Q.get('senaryo') || 'urun_turu';
const SENARYO = TURLAR[SENARYO_AD];
if (!SENARYO) {
  window.__tur = {durum:'hata', hazir:false, hatalar:['senaryo yok: ' + SENARYO_AD + ' (var olanlar: ' + Object.keys(TURLAR).join(', ') + ')']};
  return;
}
document.documentElement.classList.add('tur');
if (TEMIZ) document.documentElement.classList.add('temiz');

const bekleyen = [];
let simdi = 0, sira = 0;
const saat = {
  kur(f, ms){ const id = ++sira; bekleyen.push({id, t:simdi + Math.max(0, +ms || 0), f}); return id; },
  sil(id){ const i = bekleyen.findIndex(x => x.id === id); if (i >= 0) bekleyen.splice(i, 1); },
  ilerle(t){
    for (;;) {
      let en = null;
      for (const x of bekleyen) if (x.t <= t && (!en || x.t < en.t || (x.t === en.t && x.id < en.id))) en = x;
      if (!en) break;
      bekleyen.splice(bekleyen.indexOf(en), 1);
      simdi = en.t;
      try { en.f(); } catch (e) { hata('zamanlayici: ' + e.message); }
    }
    simdi = t;
  }
};
window.__turSaat = saat;

const $ = s => document.querySelector(s);
const kel = (a, b, u) => a + (b - a) * u;
const yumusak = u => (u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2);
const cik = u => 1 - Math.pow(1 - u, 3);
const hatalar = [];
function hata(m){ if (hatalar.indexOf(m) < 0) hatalar.push(m); }

const SURE = {imlec:850, tikla:380, bekle:500, kaydir:1000, yaz:1100, gonder:0, git:0, sec:0, panel:900, kapanis:4500, kontrol:0};
const adimlar = [];
const sahneler = [];
let t0 = 0;
const BILINEN = new Set(['tik', 'imlec', 'tikla', 'bekle', 'kaydir', 'yaz', 'gonder', 'git', 'sec', 'panel', 'kapanis', 'kontrol']);
SENARYO.sahneler.forEach(s => s.adimlar.forEach(a => { if (!BILINEN.has(a[0])) hata('bilinmeyen adim tipi: ' + a[0] + ' (sahne ' + s.ad + ')'); }));
SENARYO.sahneler.forEach((s, si) => {
  if (TEMIZ && s.adimlar.some(a => a[0] === 'kapanis')) s = {ad:s.ad, altyazi:'', adimlar:[['bekle', 1000]]};
  const bas = t0;
  s.adimlar.forEach(a => {
    const [tip, hedef, ms, ek] = a;
    if (tip === 'tik') {
      const m1 = typeof ms === 'number' ? ms : SURE.imlec;
      adimlar.push({tip:'imlec', hedef, ek:ek || {}, bas:t0, ms:m1, sahne:si}); t0 += m1;
      adimlar.push({tip:'tikla', hedef, ek:ek || {}, bas:t0, ms:SURE.tikla, sahne:si}); t0 += SURE.tikla;
      return;
    }
    const sure = tip === 'bekle' ? hedef : (typeof ms === 'number' ? ms : SURE[tip]);
    adimlar.push({tip, hedef, ms:sure, ek:(tip === 'bekle' ? {} : ek) || {}, bas:t0, sahne:si});
    t0 += sure;
  });
  sahneler.push({bas, bit:t0, ad:s.ad, metin:s.altyazi || '', kapanis:s.adimlar.some(a => a[0] === 'kapanis')});
});
const TOPLAM = t0;

const IMLEC_SVG = '<svg viewBox="0 0 28 32" width="28" height="32" aria-hidden="true"><path d="M4 2.5v22.6l5.6-5.3 3.7 8.6 3.7-1.6-3.6-8.4h7.9z" fill="#fff" stroke="#143037" stroke-width="1.7" stroke-linejoin="round"/></svg>';
let imEl, halkaEl, ayEl, ayIc, kapEl;
function katmanKur(){
  imEl = document.createElement('div'); imEl.id = 'imlec'; imEl.innerHTML = IMLEC_SVG;
  halkaEl = document.createElement('div'); halkaEl.id = 'tikhalka';
  ayEl = document.createElement('div'); ayEl.id = 'altyazi'; ayIc = document.createElement('span'); ayEl.appendChild(ayIc);
  kapEl = document.createElement('div'); kapEl.id = 'kapanis';
  const k = SENARYO.kapanis || {};
  const A = window.__ASSET || 'assets/';
  kapEl.innerHTML = `<div class="kp-ic"><div class="kp-logo"><img src="${A}deepin-logo-platform.png" alt="deepin"><span class="sep"></span><span class="prod">security</span></div><p class="kp-slogan">${k.slogan || ''}</p></div><p class="kp-not">${k.not || ''}</p>`;
  [halkaEl, imEl, ayEl, kapEl].forEach(e => document.body.appendChild(e));
}

const im = {x:0, y:0, bas:null, hedef:null, basla:0};
let tikAn = -1e9;
let aktif = 0;

function nokta(a){
  const el = typeof a.hedef === 'string' ? $(a.hedef) : null;
  if (!el) return null;
  const ek = a.ek || {};
  if (ek.svg && el.ownerSVGElement !== undefined) {
    const svg = el.ownerSVGElement || el;
    const p = svg.createSVGPoint(); p.x = ek.svg[0]; p.y = ek.svg[1];
    const q = p.matrixTransform(svg.getScreenCTM());
    return {x:q.x, y:q.y};
  }
  const r = el.getBoundingClientRect();
  if (!r.width && !r.height) return null;
  return {x:r.left + r.width * (ek.fx == null ? .5 : ek.fx) + (ek.dx || 0), y:r.top + r.height * (ek.fy == null ? .5 : ek.fy) + (ek.dy || 0)};
}
function tikla(a){
  let el = typeof a.hedef === 'string' ? $(a.hedef) : null;
  if (!el) el = document.elementFromPoint(im.x, im.y);
  if (!el) { hata('tiklanacak oge yok: ' + a.hedef); return; }
  if (typeof el.click === 'function' && el instanceof HTMLElement) { if (el.focus && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA')) el.focus(); el.click(); }
  else el.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, clientX:im.x, clientY:im.y}));
}
function kaydirHedef(a, kap){
  const h = a.ek.hedef;
  if (h === 'son') return kap.scrollHeight - kap.clientHeight;
  if (typeof h === 'number') return h;
  const el = $(h);
  if (!el) { hata('kaydirma hedefi yok: ' + h); return kap.scrollTop; }
  const y = el.getBoundingClientRect().top - kap.getBoundingClientRect().top + kap.scrollTop - (a.ek.ust == null ? 24 : a.ek.ust);
  return Math.max(0, Math.min(kap.scrollHeight - kap.clientHeight, y));
}

function baslat(a){
  if (a.tip === 'imlec') {
    a.p0 = {x:im.x, y:im.y};
    a.p1 = nokta(a);
    if (!a.p1) { a.eksik = true; }
  } else if (a.tip === 'tikla') {
    a.yapildi = false;
  } else if (a.tip === 'kaydir') {
    const kap = $(a.hedef || '#card');
    if (!kap) { hata('kaydirma kabi yok: ' + a.hedef); return; }
    a.kap = kap; a.y0 = kap.scrollTop; a.y1 = kaydirHedef(a, kap);
  } else if (a.tip === 'yaz') {
    const el = $(a.hedef);
    if (!el) { hata('yazi kutusu yok: ' + a.hedef); return; }
    el.focus(); a.metin = a.ek.metin || ''; a.n = -1;
  } else if (a.tip === 'git') {
    location.hash = a.hedef;
  } else if (a.tip === 'gonder') {
    const f = $(a.hedef);
    if (!f) { hata('form yok: ' + a.hedef); return; }
    if (f.requestSubmit) f.requestSubmit(); else f.dispatchEvent(new Event('submit', {bubbles:true, cancelable:true}));
  } else if (a.tip === 'sec') {
    const el = $(a.hedef);
    if (!el) { hata('secim kutusu yok: ' + a.hedef); return; }
    el.value = a.ek.deger; el.dispatchEvent(new Event('change', {bubbles:true}));
  } else if (a.tip === 'kontrol') {
    if (a.hedef && !$(a.hedef)) hata('kontrol: ekranda yok: ' + a.hedef);
    if (a.ek.cevap && window.__sonCevap !== a.ek.cevap) hata('kontrol: asistan beklenen soruyu cevaplamadi: beklenen ' + a.ek.cevap + ', gelen ' + (window.__sonCevap || 'yok'));
    if (a.ek.metin && !(document.body.innerText || '').includes(a.ek.metin)) hata('kontrol: ekranda metin yok: ' + a.ek.metin);
  } else if (a.tip === 'panel') {
    const cs = getComputedStyle(document.documentElement).getPropertyValue('--panel');
    a.w0 = parseFloat(cs) || 300; a.w1 = a.ek.genislik;
    const h = $('#handle');
    if (h) { const r = h.getBoundingClientRect(); a.hx0 = r.left + r.width / 2; a.hy = r.top + r.height / 2; }
  }
}
function ara(a, u){
  if (a.tip === 'imlec') {
    if (a.eksik) { a.p1 = nokta(a); if (a.p1) { a.eksik = false; a.p0 = {x:im.x, y:im.y}; } else return; }
    const e = yumusak(u);
    const dx = a.p1.x - a.p0.x, dy = a.p1.y - a.p0.y;
    const kv = Math.min(60, Math.hypot(dx, dy) * .12);
    const L = Math.hypot(dx, dy) || 1;
    const ox = -dy / L * kv, oy = dx / L * kv;
    const b = 4 * e * (1 - e);
    im.x = a.p0.x + dx * e + ox * b * .5;
    im.y = a.p0.y + dy * e + oy * b * .5;
  } else if (a.tip === 'tikla') {
    if (!a.yapildi && u >= .4) { a.yapildi = true; tikAn = a.bas + a.ms * .4; tikla(a); }
  } else if (a.tip === 'kaydir' && a.kap) {
    a.kap.scrollTop = kel(a.y0, a.y1, yumusak(u));
  } else if (a.tip === 'yaz' && a.metin != null) {
    const n = Math.min(a.metin.length, Math.floor(yumusak(Math.min(1, u * 1.08)) * (a.metin.length + .999)));
    if (n !== a.n) {
      a.n = n;
      const el = $(a.hedef);
      if (el) { el.value = a.metin.slice(0, n); el.dispatchEvent(new Event('input', {bubbles:true})); }
    }
  } else if (a.tip === 'panel' && a.w1) {
    const w = kel(a.w0, a.w1, yumusak(u));
    document.documentElement.style.setProperty('--panel', w.toFixed(1) + 'px');
    if (a.hx0 != null) { im.x = a.hx0 + (w - a.w0); im.y = a.hy; }
  }
}
function bitir(a){
  if (a.tip === 'imlec' && a.eksik) hata('imlec hedefi bulunamadi: ' + a.hedef);
  if (a.tip === 'tikla' && !a.yapildi) { a.yapildi = true; tikla(a); }
}

const izlenen = new WeakMap();
function animasyonlar(t){
  if (!KARE || !document.getAnimations) return;
  document.getAnimations().forEach(an => {
    let b = izlenen.get(an);
    if (b == null) { b = t; izlenen.set(an, b); try { an.pause(); } catch (e) {} }
    const zm = an.effect && an.effect.getComputedTiming ? an.effect.getComputedTiming() : null;
    const ic = t - b;
    try {
      if (zm && isFinite(zm.endTime) && ic >= zm.endTime) an.finish();
      else an.currentTime = ic;
    } catch (e) {}
  });
}

const kacis = x => String(x).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const vurgula = m => kacis(m).replace(/\d+(?:[.,]\d+)*/g, '<b>$&</b>');
function katmanCiz(t){
  imEl.style.transform = `translate(${im.x.toFixed(1)}px,${im.y.toFixed(1)}px)`;
  const dt = t - tikAn;
  const bas = dt >= 0 && dt < 520;
  const bs = bas ? cik(dt / 520) : 1;
  halkaEl.style.opacity = bas ? (.55 * (1 - bs)).toFixed(3) : '0';
  halkaEl.style.transform = `translate(${im.x.toFixed(1)}px,${im.y.toFixed(1)}px) scale(${(.35 + bs * .9).toFixed(3)})`;
  const basma = dt >= 0 && dt < 220 ? Math.sin(dt / 220 * Math.PI) : 0;
  imEl.firstChild.style.transform = `scale(${(1 - basma * .14).toFixed(3)})`;
  let s = sahneler.findIndex(x => t >= x.bas && t < x.bit);
  if (s < 0) s = sahneler.length - 1;
  const sh = sahneler[s];
  const onceki = sahneler[s - 1], sonraki = sahneler[s + 1];
  let op = 0;
  if (sh.metin && !sh.kapanis && !TEMIZ) {
    const giris = onceki && onceki.metin === sh.metin ? 1 : Math.min(1, (t - sh.bas) / 320);
    const cikis = sonraki && sonraki.metin === sh.metin ? 1 : Math.min(1, (sh.bit - t) / 260);
    op = Math.max(0, Math.min(giris, cikis));
    if (ayIc.dataset.m !== sh.metin) { ayIc.dataset.m = sh.metin; ayIc.innerHTML = vurgula(sh.metin); }
  }
  ayEl.style.opacity = op.toFixed(3);
  ayEl.style.transform = `translate(-50%, ${((1 - op) * 8).toFixed(1)}px)`;
  const kp = sahneler.find(x => x.kapanis);
  const kop = kp && t >= kp.bas ? yumusak(Math.min(1, (t - kp.bas) / 700)) : 0;
  kapEl.style.opacity = kop.toFixed(3);
  kapEl.style.visibility = kop > 0 ? 'visible' : 'hidden';
  imEl.style.opacity = (1 - kop).toFixed(3);
}

function kare(t){
  t = Math.max(0, Math.min(TOPLAM, t));
  saat.ilerle(t);
  while (aktif < adimlar.length && adimlar[aktif].bas <= t) {
    const a = adimlar[aktif];
    if (!a.basladi) { a.basladi = true; baslat(a); }
    const u = a.ms ? Math.min(1, (t - a.bas) / a.ms) : 1;
    ara(a, u);
    if (t >= a.bas + a.ms) { bitir(a); aktif++; } else break;
  }
  animasyonlar(t);
  katmanCiz(t);
  const bitti = t >= TOPLAM && aktif >= adimlar.length;
  if (bitti) window.__tur.durum = 'bitti';
  return {x:+im.x.toFixed(2), y:+im.y.toFixed(2), bitti};
}

window.__tur = {durum:'yukleniyor', hazir:false, senaryo:SENARYO_AD, sure:TOPLAM, kare, hatalar, sahneler:sahneler.map(s => ({bas:s.bas, bit:s.bit, ad:s.ad, metin:s.metin})), temiz:TEMIZ};

function basla(){
  katmanKur();
  const b = SENARYO.imlec_bas || [0.62, 0.72];
  im.x = innerWidth * b[0]; im.y = innerHeight * b[1];
  kare(0);
  window.__tur.hazir = true;
  window.__tur.durum = 'hazir';
  if (!KARE) {
    const bas = performance.now() + 400;
    const dongu = () => { const r = kare(performance.now() - bas); if (!r.bitti) requestAnimationFrame(dongu); };
    requestAnimationFrame(dongu);
  }
}
const hazirlan = () => {
  const yazi = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
  const resimler = Promise.all(Array.from(document.images).map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
  Promise.all([yazi, resimler]).then(() => setTimeout(basla, 60));
};
if (document.readyState === 'complete') hazirlan(); else window.addEventListener('load', hazirlan);
})();
