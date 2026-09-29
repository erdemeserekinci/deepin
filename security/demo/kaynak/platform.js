(function(){
'use strict';
const D = window.__VERI;
const $ = (s, e) => (e || document).querySelector(s);
const $$ = (s, e) => Array.from((e || document).querySelectorAll(s));
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const DIL = window.__DIL || 'tr';
const TXT = window.__TXT || {};
const ASSET = window.__ASSET || 'assets/';
const zamanla = (f, ms) => (window.__turSaat ? window.__turSaat.kur(f, ms) : setTimeout(f, ms));
const zamanIptal = z => (window.__turSaat ? window.__turSaat.sil(z) : clearTimeout(z));
const tt = (s, ...a) => {
  let v = TXT[s];
  if (v == null) v = s;
  else if (typeof v === 'object') v = (a.length && Number(a[0]) === 1 && v['1'] != null) ? v['1'] : v['*'];
  return a.length ? v.replace(/\{(\d)\}/g, (m, i) => (a[i] == null ? m : a[i])) : v;
};
const sayi = n => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, DIL === 'en' ? ',' : '.');
const dizin = (arr, k) => Object.fromEntries(arr.map(x => [x[k], x]));
const INC = dizin(D.incelemeler, 'id');
const UY = dizin(D.uyarilar, 'id');
const GUN = dizin(D.gunler, 'tarih');
const gunEt = t => (GUN[t] ? GUN[t].et : t);
const SON_GUN = D.gunler[D.gunler.length - 1].tarih;
const ONC = {yuksek:{ad:tt('Yüksek'), c:'var(--hi)'}, orta:{ad:tt('Orta'), c:'var(--md)'}, dusuk:{ad:tt('Düşük'), c:'var(--lo)'}};
const KAYNAK_AD = k => (D.kaynaklar[k] ? D.kaynaklar[k].ad : k);
const DONEMLER = [
  {k:'tum', ad:tt('Tüm dönem'), alt:D.donem.kisa, bas:D.gunler[0].tarih},
  {k:'son3', ad:tt('Son 3 gün'), alt:D.donem.son3, bas:'2026-05-01'},
  {k:'bugun', ad:tt('Bugün'), alt:D.gunler[D.gunler.length - 1].et, bas:SON_GUN}
];
const SIRALAR = [{k:'oncelik', ad:tt('Önceliğe göre')}, {k:'uyari', ad:tt('Uyarı sayısına göre')}, {k:'son', ad:tt('Son uyarıya göre')}];
const TIP_IC = {kisi:'user', bilgisayar:'laptop', servis:'server', adres:'globe'};
const TIP_AD = {kisi:tt('Kişi'), bilgisayar:tt('Bilgisayar'), servis:tt('Servis'), adres:tt('Dış adres bloğu')};

/* ---------------------------------------------------------------- ikonlar */
const IC = {
  home:'<path d="M12 2.6 2.8 10.4c-.5.4-.2 1.2.5 1.2H5V20a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1v-8.4h1.7c.7 0 1-.8.5-1.2z"/>',
  bell:'<path d="M12 2.5a1.5 1.5 0 0 1 1.5 1.5v.6A6.5 6.5 0 0 1 18.5 11v4.2l1.7 2.5c.4.6 0 1.3-.7 1.3h-15c-.7 0-1.1-.7-.7-1.3l1.7-2.5V11a6.5 6.5 0 0 1 5-6.4V4A1.5 1.5 0 0 1 12 2.5zM9.5 20.5h5a2.5 2.5 0 0 1-5 0z"/>',
  graph:'<path d="M9.5 3h5A1.5 1.5 0 0 1 16 4.5v3A1.5 1.5 0 0 1 14.5 9H13v2h5.5a1.5 1.5 0 0 1 1.5 1.5V15h1a1.5 1.5 0 0 1 1.5 1.5v3A1.5 1.5 0 0 1 21 21h-4a1.5 1.5 0 0 1-1.5-1.5v-3A1.5 1.5 0 0 1 17 15h.5v-2h-11v2H7a1.5 1.5 0 0 1 1.5 1.5v3A1.5 1.5 0 0 1 7 21H3a1.5 1.5 0 0 1-1.5-1.5v-3A1.5 1.5 0 0 1 3 15h1v-2.5A1.5 1.5 0 0 1 5.5 11H11V9H9.5A1.5 1.5 0 0 1 8 7.5v-3A1.5 1.5 0 0 1 9.5 3z"/>',
  shield:'<path fill-rule="evenodd" d="M12 2 4 5.2v6c0 4.9 3.3 9.4 8 10.8 4.7-1.4 8-5.9 8-10.8v-6zm-1.1 12.9-3-3 1.4-1.4 1.6 1.6 4.2-4.2 1.4 1.4z"/>',
  route:'<path d="M7 7h11.2l-2.6-2.6L17 3l5 5-5 5-1.4-1.4L18.2 9H7zM17 17H5.8l2.6 2.6L7 21l-5-5 5-5 1.4 1.4L5.8 15H17z"/>',
  usersearch:'<circle cx="10" cy="7.5" r="4"/><path d="M2 20c0-3.6 3.6-6 8-6 1 0 2 .1 2.9.4A5.5 5.5 0 0 0 15 19.5c0 .5.1 1 .2 1.5H2z"/><circle cx="17.2" cy="17.2" r="3.3" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="m19.6 19.6 2.4 2.4" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>',
  db:'<path d="M12 2C7 2 3 3.6 3 5.5v13C3 20.4 7 22 12 22s9-1.6 9-3.5v-13C21 3.6 17 2 12 2zm0 2c4.4 0 7 1.2 7 1.5S16.4 7 12 7 5 5.8 5 5.5 7.6 4 12 4zM5 8.6c1.8 1 4.5 1.6 7 1.6s5.2-.6 7-1.6v3c0 .3-2.6 1.6-7 1.6s-7-1.3-7-1.6zm0 6c1.8 1 4.5 1.6 7 1.6s5.2-.6 7-1.6v3.9c0 .3-2.6 1.5-7 1.5s-7-1.2-7-1.5z"/>',
  cube:'<path d="M12 2 3 6.5v11L12 22l9-4.5v-11zM12 4.3l6.2 3.1L12 10.5 5.8 7.4zM5 9.2l6 3v7.4l-6-3zM13 19.6v-7.4l6-3v7.4z"/>',
  pin:'<circle cx="12" cy="8" r="5"/><path d="M10.9 12h2.2v9.5h-2.2z"/>',
  news:'<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3h11A1.5 1.5 0 0 1 18 4.5V19a1 1 0 0 0 1 1H6a2 2 0 0 1-2-2zM7 7v3.5h8V7zm0 5.5V14h8v-1.5zm0 3V17h8v-1.5zM19.5 8H21v11a2 2 0 0 1-2 2v-1.6a.6.6 0 0 0 .6-.6z"/>',
  send:'<path d="M2.5 3.2 22 12 2.5 20.8l2-6.7L14 12 4.5 9.9z"/>',
  user:'<circle cx="12" cy="7.5" r="4.5"/><path d="M3.5 21c0-4.4 3.8-7 8.5-7s8.5 2.6 8.5 7z"/>',
  laptop:'<path d="M5 5.5A1.5 1.5 0 0 1 6.5 4h11A1.5 1.5 0 0 1 19 5.5V15H5zM2 16.5h20v.7A2.8 2.8 0 0 1 19.2 20H4.8A2.8 2.8 0 0 1 2 17.2z"/>',
  server:'<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3h13A1.5 1.5 0 0 1 20 4.5v4A1.5 1.5 0 0 1 18.5 10h-13A1.5 1.5 0 0 1 4 8.5zm0 11A1.5 1.5 0 0 1 5.5 14h13a1.5 1.5 0 0 1 1.5 1.5v4a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 19.5zM7 6v2h2V6zm0 11v2h2v-2z"/>',
  globe:'<path fill-rule="evenodd" d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm-1.1 2.1v3H8.3A8 8 0 0 1 10.9 4.1zM4.3 11h3.6c.1-1 .3-1.9.5-2.7H5.6A8 8 0 0 0 4.3 11zm0 2a8 8 0 0 0 1.3 2.7h2.8a15 15 0 0 1-.5-2.7zm4 4.7A8 8 0 0 0 10.900 19.900V16.700zM13.100 19.900A8 8 0 0 0 15.700 17.700h-2.600zm3.100-4.200h2.800a8 8 0 0 0 1.300-2.700h-3.600c-.1 1-.3 1.900-.5 2.700zm.7-4.700h3.600a8 8 0 0 0-1.300-2.700h-2.800c.2.800.4 1.700.5 2.700zM15.700 6.300A8 8 0 0 0 13.100 4.100v2.200zM13.100 8.300v2.700h2.800a13 13 0 0 0-.5-2.700zM10.900 8.300H8.600c-.2.800-.4 1.700-.5 2.700h2.800zm0 4.700H8.100c.1 1 .3 1.900.5 2.700h2.300zm2.200 0v2.700h2.300c.2-.8.4-1.700.5-2.700z"/>',
  menu:'<path d="M3 6h18v2H3zM3 11h18v2H3zM3 16h18v2H3z"/>',
  chev:'<path d="m6 9 6 6 6-6"/>',
  chevl:'<path d="m15 6-6 6 6 6"/>',
  chevr:'<path d="m9 6 6 6-6 6"/>',
  x:'<path d="M6 6l12 12M18 6 6 18"/>',
  arrows:'<path d="M3 12h18M7 8l-4 4 4 4M17 8l4 4-4 4"/>',
  search:'<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
  ext:'<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'
};
const FA = window.__IKON || {};
const FA_AD = {home:'house', bell:'bell', graph:'diagram-project', shield:'shield-halved', route:'network-wired', usersearch:'user-clock',
  db:'database', cube:'cube', pin:'map-pin', news:'newspaper', send:'paper-plane', user:'user', users:'users', laptop:'laptop',
  server:'server', globe:'globe', arrows:'arrows-left-right-to-line', search:'magnifying-glass', xcircle:'circle-xmark', check:'check'};
const LINE = new Set(['chev','chevl','chevr','x','ext']);
function svgIkon(n, sinif){
  const f = FA[FA_AD[n]];
  if (f) return `<svg class="${sinif}" viewBox="0 ${f.y} ${f.w} 512" aria-hidden="true"><path d="${f.d}"/></svg>`;
  return `<svg class="${sinif} ic-line" viewBox="0 0 24 24" aria-hidden="true">${IC[n] || ''}</svg>`;
}
const ico = (n, c) => svgIkon(n, c || 'ic');
const icoS = n => svgIkon(n, 'ic-s');

/* ---------------------------------------------------------------- durum */
const S = {
  rota:'home', incId:null, tab:'genel', risk:'tum', sirala:'oncelik', donem:'tum',
  acik:new Set(), gkisi:{}, gdugum:null, adim:{}, sabit:new Set(),
  mtSec:new Set(), agTab:'akis', agMod:'ulasan', kisi:'ktuncer', uyAra:'', uyOnc:'', uyKay:'', uySira:'onem',
  drawer:null, drAra:''
};
try {
  const kayit = JSON.parse(localStorage.getItem('dsec_sabit') || '[]');
  kayit.forEach(x => { if (INC[x]) S.sabit.add(x); });
} catch (e) {}
const kaydetSabit = () => { try { localStorage.setItem('dsec_sabit', JSON.stringify(Array.from(S.sabit))); } catch (e) {} };

/* ---------------------------------------------------------------- veri yardimcilari */
function gorunen(){
  const bas = DONEMLER.find(d => d.k === S.donem).bas;
  const l = D.incelemeler.map(inc => ({inc, u:inc.uyarilar.map(x => UY[x]).filter(x => x.gun >= bas)})).filter(x => x.u.length);
  const son = x => x.u.reduce((m, y) => (y.gun > m ? y.gun : m), '');
  if (S.sirala === 'uyari') l.sort((a, b) => b.u.length - a.u.length || b.inc.puan - a.inc.puan);
  else if (S.sirala === 'son') l.sort((a, b) => (son(b) > son(a) ? 1 : son(b) < son(a) ? -1 : b.inc.puan - a.inc.puan));
  else l.sort((a, b) => b.inc.puan - a.inc.puan);
  return l;
}
function turSay(u){
  const m = {};
  u.forEach(x => { m[x.tur] = (m[x.tur] || 0) + 1; });
  return Object.entries(m).sort((a, b) => b[1] - a[1]);
}
const kisiVar = ad => !!D.kisiler[ad];
const yuzde = v => DIL === 'en' ? Math.round(v * 100) + '%' : '%' + Math.round(v * 100);
const varlikHtml = (ad, tip) => (tip === 'kisi' && D.haftalar[ad]) ? `<a href="#/kisi/${esc(ad)}" class="who" style="text-decoration:none;border-bottom:1px dotted var(--faint)">${esc(ad)}</a>` : `<span class="who">${esc(ad)}</span>`;
const norm = s => String(s).toLocaleLowerCase(DIL).replace(/ı/g,'i').replace(/ş/g,'s').replace(/ğ/g,'g').replace(/ü/g,'u').replace(/ö/g,'o').replace(/ç/g,'c').replace(/[^a-z0-9 ]/g,' ');
const oncBadge = k => `<span class="risk ${k}">${ONC[k].ad}</span>`;

/* ---------------------------------------------------------------- yonlendirme */
function rotaOku(){
  const h = (location.hash || '#/').replace(/^#\/?/, '').split('/');
  const a = h[0] || 'home';
  S.rota = a; S.incId = null;
  if (a === 'inc') {
    if (INC[h[1]]) { S.incId = h[1]; S.tab = h[2] || 'genel'; }
    else { S.rota = 'home'; }
  }
  if (a === 'kisi' && h[1] && D.haftalar[h[1]]) S.kisi = h[1];
  if (a === 'graf') {
    const g = D.incelemeler.find(i => i.graf);
    if (g) { location.replace('#/inc/' + g.id + '/graf'); return false; }
  }
  return true;
}
function git(p){ location.hash = '#/' + p; }
const geri = () => { if (history.length > 1) history.back(); else git(''); };

/* ---------------------------------------------------------------- iskelet */
function iskelet(){
  const railItems = [
    ['', 'home', tt('Ana sayfa')], ['uyarilar', 'bell', tt('Tüm uyarılar')], ['graf', 'graph', tt('Graf')], ['mitre', 'shield', 'MITRE'],
    ['ag', 'route', tt('Ağ geçişleri')], ['kisi', 'usersearch', tt('Kişi sorgusu')], ['kaynaklar', 'db', tt('Veri kaynakları')]
  ];
  const rail = railItems.map(([p, i, ad]) => `<button class="rb" data-a="nav" data-p="${p}" data-r="${p || 'home'}" aria-label="${ad}">${ico(i)}<span class="tip">${ad}</span>${p === 'uyarilar' ? `<span class="n">${D.uyarilar.length}</span>` : ''}</button>`).join('');
  const en = DIL === 'en';
  $('#kok').innerHTML = `
  <div class="app">
    <header class="head">
      <a class="brand" href="#/" aria-label="deepin security"><img src="${ASSET}deepin-logo-platform.png" alt="deepin" width="108" height="32"><span class="sep" aria-hidden="true"></span><span class="prod">security</span></a>
      <div class="head-r">
        <button class="menu-btn" data-a="chat-ac" aria-label="${tt('Asistan')}">${ico('news')}</button>
        <div class="lang" role="group" aria-label="${tt('Dil')}"><button class="${en ? '' : 'on'}" data-a="dil" data-p="tr">TR</button><button class="${en ? 'on' : ''}" data-a="dil" data-p="en">EN</button></div>
      </div>
    </header>
    <nav class="rail" aria-label="${tt('Ana menü')}">${rail}<span class="grow"></span><button class="rb avatar" aria-label="${esc(D.kurum)}">${ico('user')}<span class="tip">${esc(D.kurum)} · ${esc(D.kurum_alt)}</span></button></nav>
    <aside class="chat" id="chat" aria-label="${tt('Asistan')}">
      <div class="chat-in">
        <button class="back" data-a="geri" id="geri" hidden>${ico('chevl')}<span>${tt('Geri')}</span></button>
        <div class="wm" aria-hidden="true"><img src="${ASSET}deepin-logo-platform.png" alt=""><span class="sep"></span><span>security</span></div>
        <div class="feed" id="feed" aria-live="polite"></div>
        <div class="chat-foot">
          <div class="cf-top"><button class="news" data-a="brifing" aria-label="${tt('Günlük özet')}" title="${tt('Günlük özet')}">${ico('news')}</button></div>
          <form class="ask" id="ask" autocomplete="off"><input id="askin" type="text" placeholder="${tt('Deepin Security size nasıl yardımcı olabilir?')}" aria-label="${tt('Soru')}"><button type="submit" aria-label="${tt('Gönder')}">${ico('send')}</button></form>
          <p class="disc">${tt('Yapay zekâ hata yapabilir. Lütfen cevapları doğrulayın.')}</p>
        </div>
      </div>
      <button class="handle" id="handle" aria-label="${tt('Paneli yeniden boyutlandır')}" title="${tt('Sürükleyerek boyutlandırın')}">${ico('arrows')}</button>
    </aside>
    <main class="main"><div class="card" id="card" tabindex="-1"></div></main>
    <aside class="rrail" aria-label="${tt('Yardımcı paneller')}">
      <button class="rb" data-a="cekmece" data-p="varlik" aria-label="${tt('Varlıklar')}">${ico('cube')}<span class="tip">${tt('Varlıklar')}</span></button>
      <button class="rb" data-a="cekmece" data-p="sabit" aria-label="${tt('Sabitlenenler')}">${ico('pin')}<span class="tip">${tt('Sabitlenenler')}</span></button>
    </aside>
    <aside class="drawer" id="drawer" aria-label="Panel"></aside>
    <div class="toast" id="toast" role="status"></div>
  </div>`;
}

/* ---------------------------------------------------------------- ana sayfa */
function viewHome(){
  const l = gorunen();
  const say = {yuksek:0, orta:0, dusuk:0};
  l.forEach(x => { say[x.inc.oncelik]++; });
  const bosMetin = tt('Bu dönemde kayıt yok');
  const sub = {yuksek:[tt('Hemen bakın'), bosMetin], orta:[tt('Yakından izleyin'), bosMetin], dusuk:[tt('Rutin takip'), bosMetin]};
  const tabs = ['yuksek', 'orta', 'dusuk'].map(k => `<button class="t4 ${S.risk === k ? 'on' : ''} ${say[k] ? 'dolu' : 'bos'}" style="--c:${ONC[k].c}" data-a="risk" data-p="${k}"><span class="top4"><span class="num">${say[k]}</span><span class="lab">${ONC[k].ad}</span></span><span class="sb">${sub[k][say[k] ? 0 : 1]}</span></button>`).join('')
    + `<button class="t4 ${S.risk === 'tum' ? 'on' : ''} dolu" style="--c:var(--ink)" data-a="risk" data-p="tum"><span class="top4"><span class="num">${l.length}</span><span class="lab">${tt('Tümü')}</span></span><span class="sb">${S.sirala === 'oncelik' ? tt('Yüksekten düşüğe sıralı') : SIRALAR.find(x => x.k === S.sirala).ad}</span></button>`;
  const sec = S.risk === 'tum' ? l : l.filter(x => x.inc.oncelik === S.risk);
  const uSay = sec.reduce((a, x) => a + x.u.length, 0);
  const bas = S.risk === 'tum' ? tt('Tüm incelemeler') : tt('{0} öncelik', ONC[S.risk].ad);
  const donem = DONEMLER.find(d => d.k === S.donem);
  const satirlar = sec.map(x => satir(x)).join('') || `<div class="bos-liste"><b>${tt('Bu seçimde inceleme yok')}</b>${tt('Dönemi ya da öncelik sekmesini değiştirin.')}</div>`;
  return `
  <div class="top">
    <div><h1>${tt('Güncel Uyarılar')}</h1><p class="sub">${tt('Takip ettiğiniz kayıt kaynaklarındaki son değişiklikler')}</p></div>
    <div class="top-r">${S.donem !== 'tum' ? `<button class="xbtn" data-a="donem" data-p="tum" aria-label="${tt('Dönem seçimini kaldır')}" title="${tt('Dönem seçimini kaldır')}">${ico('xcircle')}</button>` : '<span class="xyer"></span>'}<div class="donem" id="donem"><button data-a="donem-menu" aria-haspopup="true"><span>${esc(donem.ad)}</span>${icoS('chev')}</button>
      <ul>${DONEMLER.map(d => `<li><button class="${d.k === S.donem ? 'on' : ''}" data-a="donem" data-p="${d.k}"><span>${d.ad}</span><span style="color:var(--muted);font-weight:400">${d.alt}</span></button></li>`).join('')}</ul></div></div>
  </div>
  <div class="tabs4" role="tablist">${tabs}</div>
  <div class="listbar"><h2>${bas} <span>· ${tt('{0} inceleme', sec.length)}, ${tt('{0} uyarı', uSay)}</span></h2>
    <div class="sort" id="sort"><button data-a="sort-menu" aria-haspopup="true">${tt('Sıralama:')} <b>${SIRALAR.find(x => x.k === S.sirala).ad}</b> ${icoS('chev')}</button>
      <ul>${SIRALAR.map(s => `<li><button class="${s.k === S.sirala ? 'on' : ''}" data-a="sirala" data-p="${s.k}">${s.ad}</button></li>`).join('')}</ul></div></div>
  <div class="rows">${satirlar}</div>
  <p class="note">${tt('Kurgusal kurumla hazırlanmış demo verisi. Dönem: {0}, son güncelleme {1}.', esc(D.donem.etiket), esc(D.donem.son_kosu))}</p>`;
}
function satir(x){
  const inc = x.inc;
  const chips = turSay(x.u).map(([ad, n]) => `<span class="rchip">${esc(ad)} <b>${n}</b></span>`).join('');
  const bugun = x.u.some(y => y.gun === SON_GUN);
  const kaynaklar = inc.kaynaklar.map(KAYNAK_AD).join(', ');
  const acik = S.acik.has(inc.id);
  const alt = x.u.slice(0, 4).map(y => `<div><b>${esc(y.varlik)}</b><span>${esc(y.ne)}</span><small>${esc(KAYNAK_AD(y.kaynak))}</small><small>${gunEt(y.gun)}</small></div>`).join('')
    + (x.u.length > 4 ? `<div><b>${tt('+{0} uyarı daha', x.u.length - 4)}</b><span>${tt('İnceleme dosyasında listelenir')}</span><small></small><small></small></div>` : '');
  return `<div class="row ${inc.oncelik} ${acik ? 'acik' : ''}" data-id="${inc.id}">
    <div class="row-h" role="link" tabindex="0" data-a="ac-inc" data-p="${inc.id}" aria-label="${tt('{0} incelemesini aç', esc(inc.baslik))}">
      <div><div class="rt">${esc(inc.baslik)}${bugun ? `<span class="yeni">${tt('bugün')}</span>` : ''}</div>
        <div class="rchips">${chips}</div></div>
      <div class="rsag"><span class="pill">${tt('{0} uyarı', x.u.length)}</span><button class="chev" data-a="satir-ac" data-p="${inc.id}" aria-label="${acik ? tt('Ayrıntıyı kapat') : tt('Ayrıntıyı aç')}" aria-expanded="${acik}">${ico('chev')}</button></div>
    </div>
    <div class="rdet"><p class="ozt">${esc(inc.kart_ozet)} <span style="color:var(--muted)">· ${esc(kaynaklar)}</span></p><div class="sub-u">${alt}</div>
      <button class="btn p s go" data-a="ac-inc" data-p="${inc.id}">${tt('İncelemeyi aç')} ${icoS('chevr')}</button></div>
  </div>`;
}

/* ---------------------------------------------------------------- inceleme dosyasi */
const TAB_AD = {genel:tt('Genel bakış'), uyarilar:tt('Uyarılar'), kanit:tt('Kanıt'), zaman:tt('Zaman'), graf:tt('Graf'), eksik:tt('Eksik bilgi')};
function viewInc(){
  const inc = INC[S.incId];
  const tabs = ['genel', 'uyarilar', 'kanit', 'zaman'].concat(inc.graf ? ['graf'] : [], ['eksik']);
  if (tabs.indexOf(S.tab) < 0) S.tab = 'genel';
  const say = {uyarilar:inc.uyarilar.length, eksik:inc.eksik.length};
  const pinli = S.sabit.has(inc.id);
  const govde = {genel:tabGenel, uyarilar:tabUyarilar, kanit:tabKanit, zaman:tabZaman, graf:tabGraf, eksik:tabEksik}[S.tab](inc);
  return `
  <div class="dhead"><button class="geri" data-a="geri" aria-label="${tt('Geri')}">${ico('chevl')}</button><span class="crumb">${tt('Güncel Uyarılar')} / ${tt('İnceleme')}</span></div>
  <div class="dtitle"><div><h1>${esc(inc.baslik)}</h1><p class="alt">${esc(inc.alt)}</p>
    <div class="dbadges">${oncBadge(inc.oncelik)}<span class="tag">${esc(inc.tur_ad)}</span><span class="mtl">${tt('{0} uyarı', inc.uyarilar.length)} · ${inc.kaynaklar.map(KAYNAK_AD).join(', ')}</span></div></div>
    <div class="dact"><button class="btn s" data-a="sabit" data-p="${inc.id}">${icoS('pin')} ${pinli ? tt('Sabitlendi') : tt('Sabitle')}</button>${inc.graf && S.tab !== 'graf' ? `<button class="btn s p" data-a="tab" data-p="graf">${icoS('graph')} ${tt('Grafı aç')}</button>` : ''}</div></div>
  <div class="dtabs" role="tablist">${tabs.map(ad => `<button class="${S.tab === ad ? 'on' : ''}" data-a="tab" data-p="${ad}" role="tab">${TAB_AD[ad]}${say[ad] != null ? `<em>${say[ad]}</em>` : ''}</button>`).join('')}</div>
  ${govde}`;
}
function tablo(k, satirlar, opts){
  opts = opts || {};
  const sayisal = new Set(k.sayisal || []);
  const th = k.kolon.map((c, i) => `<th class="${sayisal.has(i) ? 'n' : ''}">${esc(c)}</th>`).join('');
  const tr = (satirlar || k.satir).map(r => `<tr>${r.map((c, i) => `<td class="${sayisal.has(i) ? 'n' : ''}">${i === 0 && k.kolon[0] === tt('Kullanıcı') ? varlikHtml(c, 'kisi') : esc(c)}</td>`).join('')}</tr>`).join('');
  return `<div class="tw"><table class="t"><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table></div>`;
}
function tabGenel(inc){
  const mit = inc.mitre.length ? `<div class="mitrow"><span class="lab">MITRE</span>${inc.mitre.map(c => `<span class="mtl"><span class="mt">${c}</span>${esc(D.mitre[c].ad)}</span>`).join('')}${inc.asama ? `<span class="mtl" style="margin-left:auto">${tt('Aşama')} <b>${esc(inc.asama)}</b></span>` : ''}</div>` : '';
  const varl = inc.varliklar.slice(0, 8).map(v => `<tr><td><span style="display:inline-flex;align-items:center;gap:10px"><span style="color:var(--muted)">${ico(TIP_IC[v.tip])}</span>${varlikHtml(v.ad, v.tip)}</span></td><td>${TIP_AD[v.tip]}</td><td>${esc(v.alt)}</td></tr>`).join('')
    + (inc.varliklar.length > 8 ? `<tr><td colspan="3" style="color:var(--muted)">${tt('+{0} varlık daha, Uyarılar sekmesinde', inc.varliklar.length - 8)}</td></tr>` : '');
  const adimlar = inc.adimlar.map((a, i) => {
    const ok = !!S.adim[inc.id + i];
    return `<div class="step ${ok ? 'ok' : ''}"><i data-a="adim" data-p="${inc.id}|${i}" role="checkbox" aria-checked="${ok}" tabindex="0"></i><div><b>${esc(a[0])}</b><small>${esc(a[1])}</small></div><span class="own">${esc(a[2])}</span></div>`;
  }).join('');
  return `
  <div class="verdict ${inc.oncelik}">${esc(inc.ozet)}</div>
  ${inc.nedenler.length ? `<div class="neden">${inc.nedenler.map(n => `<span>${esc(n)}</span>`).join('')}</div>` : ''}
  ${mit}
  <div class="mets">${inc.metrikler.map((m, i) => `<div class="met ${i === 0 && inc.oncelik === 'yuksek' ? 'w' : ''}"><b>${esc(m[0])}</b><span>${esc(m[1])}</span></div>`).join('')}</div>
  <div class="fg">${inc.alan.map(a => `<div><span>${esc(a[0])}</span><b>${esc(a[1])}</b></div>`).join('')}</div>
  <h3 class="sec">${tt('Varlıklar')}</h3>
  <div class="tw"><table class="t"><thead><tr><th>${tt('Varlık')}</th><th>${tt('Tür')}</th><th>${tt('Ayrıntı')}</th></tr></thead><tbody>${varl}</tbody></table></div>
  <h3 class="sec">${tt('Adımlar')}</h3><div class="steps">${adimlar}</div>`;
}
function tabUyarilar(inc){
  const satirlar = inc.uyarilar.map(id => UY[id]).map(u => `<tr><td>${varlikHtml(u.varlik, u.tip)}</td><td>${esc(u.tur)}</td><td style="min-width:230px">${esc(u.ne)}</td><td>${esc(KAYNAK_AD(u.kaynak))}</td><td class="nw">${gunEt(u.gun)}</td><td class="nw"><span class="barw"><span class="bar" style="width:${Math.round(u.onem * .6)}px;--c:${u.onem >= 84 ? 'var(--hi)' : u.onem >= 60 ? 'var(--md)' : 'var(--lo)'}"></span><span>${u.onem}</span></span></td></tr>`).join('');
  return `<p class="lead">${tt('Bu incelemeyi oluşturan {0} uyarı. Her uyarı tek bir kayıt kaynağından ve tek bir davranıştan gelir; inceleme, bunları aynı hikâyede toplar.', inc.uyarilar.length)}</p>
  <div class="tw" style="margin-top:18px"><table class="t"><thead><tr><th>${tt('Varlık')}</th><th>${tt('Uyarı türü')}</th><th>${tt('Ne oldu')}</th><th>${tt('Kaynak')}</th><th>${tt('Gün')}</th><th>${tt('Önem')}</th></tr></thead><tbody>${satirlar}</tbody></table></div>`;
}
function hamHtml(inc){
  const h = inc.ham;
  const satir = h.satirlar.map((s, i) => `<div><span class="ln">${String(i + 1).padStart(2, '0')}</span>${esc(s).replace(/(\b\d{1,3}(?:\.\d{1,3}){3}\b)/g, '<em>$1</em>').replace(/(MERIDYEN\\[a-z0-9]+)/g, '<em>$1</em>')}</div>`).join('');
  return `<h3 class="sec">${tt('Ham kayıt')}</h3>
  <div class="logh"><span>${tt('{0} / {1} satır gösteriliyor', h.satirlar.length, sayi(h.toplam))} · ${esc(KAYNAK_AD(h.kaynak === 'waf' ? 'citrix' : h.kaynak))}</span><span>${tt('Dosya')} <code>ham_kanit/${esc(h.dosya)}</code></span></div>
  <div class="log" role="region" aria-label="${tt('Ham kayıt satırları')}" tabindex="0">${satir}</div>`;
}
function tabKanit(inc){
  return inc.kanit.map(k => `<h3 class="sec">${esc(k.baslik)}</h3>${tablo(k)}`).join('') + hamHtml(inc);
}
function tabZaman(inc){
  const say = {};
  inc.uyarilar.forEach(id => { const g = UY[id].gun; say[g] = (say[g] || 0) + 1; });
  const mx = Math.max.apply(null, Object.values(say).concat([1]));
  const cubuk = D.gunler.map(g => `<div class="${say[g.tarih] ? '' : 'b'}"><b>${say[g.tarih] || ''}</b><i style="height:${say[g.tarih] ? Math.max(14, Math.round(say[g.tarih] / mx * 70)) : 4}px"></i><small>${g.et}</small></div>`).join('');
  const liste = inc.zaman.slice().sort((a, b) => (a.gun + a.saat) < (b.gun + b.saat) ? -1 : 1).map(z => `<li class="${z.ton}"><span class="tm">${gunEt(z.gun)}${z.saat ? ' · ' + z.saat : ''}</span><b>${esc(z.baslik)}</b><p>${esc(z.ayrinti)}</p><span class="ks">${esc(KAYNAK_AD(z.kaynak))}</span></li>`).join('');
  return `<p class="lead">${tt('Uyarıların günlere dağılımı ve kayıtlardaki olayların sırası.')}</p><div class="spark">${cubuk}</div><ol class="tl">${liste}</ol>`;
}
function tabEksik(inc){
  return `<p class="lead">${tt('Bu incelemeyi sonuçlandırmak için eksik olan {0} bilgi. Bilgi geldiğinde inceleme yeniden değerlendirilir.', inc.eksik.length)}</p>
  <div class="eks" style="margin-top:18px">${inc.eksik.map(e => `<div><b>${esc(e[0])}</b><dl><dt>${tt('Kayıtlarda olmayan')}</dt><dd>${esc(e[1])}</dd><dt>${tt('Cevabı kimde')}</dt><dd>${esc(e[2])}</dd></dl></div>`).join('')}</div>`;
}

/* ---------------------------------------------------------------- graf */
const SINIF = {
  normal:{ad:tt('Grubun da gittiği ağ'), c:'#158867', bg:'#eaf6f1', dash:''},
  yalniz:{ad:tt('Yalnız bu kişinin ulaştığı ağ'), c:'#ca8505', bg:'#fbf1df', dash:''},
  engel:{ad:tt('Denedi, engellendi'), c:'#e2725f', bg:'#fbe4df', dash:'6 5'},
  grup_engel:{ad:tt('Grubun da engellendiği ağ'), c:'#9aa3ad', bg:'#f3f5f8', dash:'6 5'}
};
const SINIF_DUR = {
  normal:tt('Ulaşıldı; grubun başka üyeleri de gidiyor'),
  yalniz:tt('Ulaşıldı; yalnız bu kişi gidiyor'),
  engel:tt('Engellendi; hiçbir istek geçmedi'),
  grup_engel:tt('Engellendi; grubun başka üyeleri de aynı ağı deniyor')
};
function kalinlik(n){ return Math.min(11, 1.4 + Math.log10(n + 1) * 2.6); }
function grafKur(inc, kisi){
  const ag = kisi.ag;
  const sinifDizisi = ['normal', 'yalniz', 'engel', 'grup_engel'];
  const tavan = {normal:4, yalniz:4, engel:6, grup_engel:1};
  const gruplar = sinifDizisi.map(s => {
    const hepsi = ag.filter(x => x.sinif === s).sort((a, b) => b.istek - a.istek);
    const toplam = s === 'engel' ? Math.max(kisi.ozet.engel, hepsi.length) : hepsi.length;
    let goster = hepsi.slice(0, tavan[s]);
    let ekle = null;
    if (s === 'grup_engel' && hepsi.length) { goster = []; ekle = {kume:true, sinif:s, adet:hepsi.length, istek:hepsi.reduce((a, x) => a + x.istek, 0), grup_pay:hepsi[0].grup_pay}; }
    else if (toplam > goster.length) ekle = {kume:true, sinif:s, adet:toplam - goster.length, istek:(s === 'engel' && kisi.engel_istek != null) ? kisi.engel_istek - goster.reduce((a, x) => a + x.istek, 0) : hepsi.slice(goster.length).reduce((a, x) => a + x.istek, 0), grup_pay:0};
    return {s, goster, ekle, toplam};
  }).filter(g => g.goster.length || g.ekle);
  const W = 1000, NX = 590, NW = 360, NH = 44, GAP = 10, BAND = 32;
  let y = 24;
  const dugumler = [];
  const basliklar = [];
  gruplar.forEach(g => {
    basliklar.push({y, s:g.s, toplam:g.toplam});
    y += BAND;
    g.goster.forEach(x => { dugumler.push(Object.assign({}, x, {y, id:'d' + dugumler.length})); y += NH + GAP; });
    if (g.ekle) { dugumler.push(Object.assign({}, g.ekle, {y, id:'d' + dugumler.length})); y += NH + GAP; }
    y += 10;
  });
  const H = Math.max(y + 10, 480);
  const gx = 140, gy = 120, px = 140, py = Math.max(H - 120, 330);
  const kenar = dugumler.map(d => {
    const c = SINIF[d.sinif];
    const cy = d.y + NH / 2;
    const w = kalinlik(d.istek);
    const dash = c.dash ? ` stroke-dasharray="${c.dash}"` : '';
    const y0 = py;
    let s = `<path d="M ${px + 64} ${y0} C ${px + 230} ${y0}, ${NX - 170} ${cy}, ${NX} ${cy}" fill="none" stroke="${c.c}" stroke-width="${w.toFixed(1)}" stroke-opacity=".78"${dash} stroke-linecap="round"/>`;
    if ((d.sinif === 'normal' || d.sinif === 'grup_engel') && inc.graf.tur !== 'x') {
      const gw = Math.max(1.2, (d.grup_pay || .3) * 5.5);
      s += `<path d="M ${gx + 60} ${gy} C ${gx + 230} ${gy}, ${NX - 170} ${cy}, ${NX} ${cy}" fill="none" stroke="#b6bec7" stroke-width="${gw.toFixed(1)}" stroke-opacity=".55"${dash} stroke-linecap="round"/>`;
    }
    return s;
  }).join('');
  const nodeSvg = dugumler.map(d => {
    const c = SINIF[d.sinif];
    const sel = S.gdugum === d.id ? ' sel' : '';
    const dash = c.dash ? ` stroke-dasharray="${c.dash}"` : '';
    if (d.kume) {
      const bas = d.sinif === 'grup_engel' ? tt('{0} ağ', d.adet) : tt('+{0} ağ daha', d.adet);
      const alt = d.sinif === 'grup_engel' ? tt('Grubun da engellendiği ağlar') : tt('engellendi, tabloda');
      return `<g class="gnode${sel}" data-a="dugum" data-p="${d.id}" tabindex="0"><rect x="${NX}" y="${d.y}" width="${NW}" height="${NH}" rx="12" fill="${c.bg}" stroke="${c.c}" stroke-width="1.25"${dash}/><text x="${NX + 16}" y="${d.y + 20}" font-size="13" font-weight="600" fill="#143037">${bas}</text><text x="${NX + 16}" y="${d.y + 37}" font-size="12" fill="#727c8a">${alt}</text><text x="${NX + NW - 14}" y="${d.y + 28}" font-size="12" text-anchor="end" fill="#4a5d64">${tt('{0} istek', sayi(d.istek))}</text></g>`;
    }
    const ad = d.ad ? d.ad : tt('kayıtlarda tanımlı değil');
    return `<g class="gnode${sel}" data-a="dugum" data-p="${d.id}" data-c="${esc(d.cidr)}" tabindex="0"><rect x="${NX}" y="${d.y}" width="${NW}" height="${NH}" rx="12" fill="${c.bg}" stroke="${c.c}" stroke-width="1.25"${dash}/><text x="${NX + 16}" y="${d.y + 20}" font-size="13" font-weight="600" fill="#143037" font-family="JetBrains Mono, ui-monospace, Menlo, monospace">${esc(d.cidr)}</text><text x="${NX + 16}" y="${d.y + 37}" font-size="12" fill="#727c8a"${d.ad ? '' : ' font-style="italic"'}>${esc(ad)}</text><text x="${NX + NW - 14}" y="${d.y + 28}" font-size="12" text-anchor="end" fill="#4a5d64">${tt('{0} istek', sayi(d.istek))}</text></g>`;
  }).join('');
  const bas = basliklar.map(b => `<text x="${NX}" y="${b.y + 18}" font-size="12" font-weight="600" letter-spacing=".06em" fill="${SINIF[b.s].c}" style="text-transform:uppercase">${SINIF[b.s].ad.toLocaleUpperCase(DIL)}${b.toplam ? ' · ' + b.toplam : ''}</text>`).join('');
  const nuye = inc.graf.grup.uye;
  const noktalar = [];
  for (let i = 0; i < 16; i++) {
    const a = i / 16 * Math.PI * 2;
    noktalar.push(`<circle cx="${gx + Math.cos(a) * 58}" cy="${gy + Math.sin(a) * 58}" r="5" fill="#c9d3da"/>`);
  }
  const grupSvg = `<g>${noktalar.join('')}<circle cx="${gx}" cy="${gy}" r="44" fill="#f3f5f8" stroke="#dbe1e6" stroke-width="1.5"/><text x="${gx}" y="${gy - 2}" text-anchor="middle" font-size="24" font-weight="700" fill="#143037">${nuye}</text><text x="${gx}" y="${gy + 17}" text-anchor="middle" font-size="11.5" fill="#727c8a">${tt('kişi')}</text></g>
    <text x="${gx}" y="${gy + 84}" text-anchor="middle" font-size="12.5" font-weight="600" fill="#143037">${esc(inc.graf.grup.ad)}</text><text x="${gx}" y="${gy + 101}" text-anchor="middle" font-size="12" fill="#727c8a">${tt('benzer görevdekiler')}</text>`;
  const kisiSvg = `<g><rect x="${px - 64}" y="${py - 30}" width="128" height="60" rx="16" fill="#143037"/><text x="${px}" y="${py - 4}" text-anchor="middle" font-size="14" font-weight="600" fill="#fff" font-family="JetBrains Mono, ui-monospace, Menlo, monospace">${esc(kisi.ad)}</text><text x="${px}" y="${py + 14}" text-anchor="middle" font-size="11.5" fill="#9fb3ba">${esc(kisi.ad_soyad)}</text></g>`;
  return {svg:`<svg class="gsvg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${tt('{0} için ağ rotaları', esc(kisi.ad_soyad))}">${kenar}${grupSvg}${kisiSvg}${bas}${nodeSvg}</svg>`, dugumler};
}
function tabGraf(inc){
  const g = inc.graf;
  const ad = S.gkisi[inc.id] || g.kisiler[0].ad;
  const kisi = g.kisiler.find(k => k.ad === ad) || g.kisiler[0];
  const {svg, dugumler} = grafKur(inc, kisi);
  const oz = kisi.ozet;
  const secili = dugumler.find(d => d.id === S.gdugum);
  let yan;
  if (secili) {
    const c = SINIF[secili.sinif];
    yan = secili.kume
      ? `<h4>${secili.sinif === 'grup_engel' ? tt('Grubun da engellendiği ağlar') : tt('Diğer engellenen ağlar')}</h4><dl><dt>${tt('Ağ sayısı')}</dt><dd>${secili.adet}</dd><dt>${tt('İstek')}</dt><dd>${sayi(secili.istek)}</dd><dt>${tt('Durum')}</dt><dd>${SINIF_DUR[secili.sinif]}</dd></dl>`
      : `<h4 style="font-family:var(--mono);font-size:14px">${esc(secili.cidr)}</h4><dl><dt>${tt('Ağ tanımı')}</dt><dd>${secili.ad ? esc(secili.ad) : `<span style="color:var(--muted);font-style:italic;font-weight:400">${tt('kayıtlarda tanımlı değil')}</span>`}</dd><dt>${tt('Durum')}</dt><dd style="color:${c.c}">${SINIF_DUR[secili.sinif]}</dd><dt>${tt('İstek')}</dt><dd>${sayi(secili.istek)}</dd><dt>${tt('Geçen istek')}</dt><dd>${sayi(secili.gecen)}</dd><dt>${tt('İlk görülme')}</dt><dd>${gunEt(secili.gun)}</dd><dt>${tt('Benzer görevdekilerden giden')}</dt><dd>${secili.grup_pay ? tt('{0} ({1} / {2})', yuzde(secili.grup_pay), Math.round(secili.grup_pay * g.grup.uye), g.grup.uye) : tt('hiçbiri')}</dd></dl>`;
  } else {
    yan = `<h4>${esc(kisi.ad_soyad)}</h4><dl><dt>${tt('Birim')}</dt><dd>${esc(kisi.alt)}</dd><dt>${tt('Grubun da gittiği')}</dt><dd>${tt('{0} ağ', oz.normal)}</dd><dt>${tt('Yalnız bu kişinin ulaştığı')}</dt><dd>${tt('{0} ağ', oz.yalniz)}</dd><dt>${tt('Engellenen ağ, toplam')}</dt><dd>${tt('{0} ağ', sayi(oz.engel + oz.grup_engel))}</dd><dt>${tt('Yalnız bu kişinin denediği')}</dt><dd>${tt('{0} ağ', sayi(oz.engel))}</dd><dt>${tt('Grubun da engellendiği')}</dt><dd>${tt('{0} ağ', oz.grup_engel)}</dd></dl><p class="bos" style="margin-top:14px">${tt('Bir ağa tıklayın, ayrıntısı burada görünür.')}</p>`;
  }
  const secim = g.kisiler.length > 1 ? `<span class="lab">${tt('Kişi')}</span><div class="gsel">${g.kisiler.map(k => `<button class="${k.ad === kisi.ad ? 'on' : ''}" data-a="gkisi" data-p="${inc.id}|${k.ad}">${esc(k.ad)}</button>`).join('')}</div>` : `<span class="lab">${esc(kisi.ad_soyad)} · ${esc(kisi.alt)}</span>`;
  return `<div class="gwrap"><div class="gbar">${secim}<div class="gleg"><span><i style="--c:#158867"></i>${tt('Grubun da gittiği')}</span><span><i style="--c:#ca8505"></i>${tt('Yalnız bu kişi')}</span><span><i class="k" style="--c:#e2725f"></i>${tt('Engellendi')}</span><span><i style="--c:#b6bec7"></i>${tt('Grubun yolu')}</span></div></div>
  <div class="gbody"><div>${svg}</div><div class="gside">${yan}</div></div>
  <div class="gcap">${tt('Çizgi kalınlığı istek sayısını gösterir (logaritmik ölçek). Gri çizgi, benzer görevdekilerin o ağa gönderdiği isteği temsil eder.')}</div></div>`;
}

/* ---------------------------------------------------------------- tum uyarilar */
function viewUyarilar(){
  let l = D.uyarilar.slice();
  const q = norm(S.uyAra);
  if (q) l = l.filter(u => norm(u.varlik + ' ' + u.ne + ' ' + u.tur).indexOf(q) >= 0);
  if (S.uyOnc) l = l.filter(u => INC[u.inc].oncelik === S.uyOnc);
  if (S.uyKay) l = l.filter(u => u.kaynak === S.uyKay);
  l.sort((a, b) => S.uySira === 'gun' ? (a.gun < b.gun ? 1 : -1) : S.uySira === 'varlik' ? a.varlik.localeCompare(b.varlik, DIL) : b.onem - a.onem);
  const satir = l.map(u => { const inc = INC[u.inc]; return `<tr class="lnk" data-a="ac-inc" data-p="${inc.id}"><td>${esc(u.varlik)}</td><td>${esc(u.tur)}</td><td style="min-width:230px">${esc(u.ne)}</td><td>${esc(KAYNAK_AD(u.kaynak))}</td><td class="nw">${gunEt(u.gun)}</td><td class="nw"><span class="barw"><span class="bar" style="width:${Math.round(u.onem * .5)}px;--c:${u.onem >= 84 ? 'var(--hi)' : u.onem >= 60 ? 'var(--md)' : 'var(--lo)'}"></span><span>${u.onem}</span></span></td><td class="nw">${oncBadge(inc.oncelik)}</td></tr>`; }).join('');
  return `<div class="top"><div><h1>${tt('Tüm uyarılar')}</h1><p class="sub">${tt('{0} / {1} uyarı', l.length, D.uyarilar.length)} · ${esc(D.donem.etiket)}</p></div></div>
  <div class="filters"><label class="search">${icoS('search')}<input id="uyara" type="search" placeholder="${tt('Varlık, tür veya açıklama ara')}" value="${esc(S.uyAra)}" aria-label="${tt('Uyarılarda ara')}"></label>
    <select class="sel" data-a="uyonc" aria-label="${tt('Öncelik')}"><option value="">${tt('Tüm öncelikler')}</option>${Object.keys(ONC).map(k => `<option value="${k}" ${S.uyOnc === k ? 'selected' : ''}>${ONC[k].ad}</option>`).join('')}</select>
    <select class="sel" data-a="uykay" aria-label="${tt('Kaynak')}"><option value="">${tt('Tüm kaynaklar')}</option>${Object.keys(D.kaynaklar).map(k => `<option value="${k}" ${S.uyKay === k ? 'selected' : ''}>${D.kaynaklar[k].ad}</option>`).join('')}</select>
    <select class="sel" data-a="uysira" aria-label="${tt('Sıralama')}"><option value="onem" ${S.uySira === 'onem' ? 'selected' : ''}>${tt('Önem sırasına göre')}</option><option value="gun" ${S.uySira === 'gun' ? 'selected' : ''}>${tt('Yeniden eskiye')}</option><option value="varlik" ${S.uySira === 'varlik' ? 'selected' : ''}>${tt('Varlık adına göre')}</option></select></div>
  <div class="tw" style="margin-top:18px"><table class="t"><thead><tr><th>${tt('Varlık')}</th><th>${tt('Uyarı türü')}</th><th>${tt('Ne oldu')}</th><th>${tt('Kaynak')}</th><th>${tt('Gün')}</th><th>${tt('Önem')}</th><th>${tt('İnceleme')}</th></tr></thead><tbody>${satir || `<tr><td colspan="7" style="text-align:center;color:var(--muted);padding:34px">${tt('Eşleşen uyarı yok')}</td></tr>`}</tbody></table></div>`;
}

/* ---------------------------------------------------------------- mitre */
function viewMitre(){
  const uy = {};
  D.uyarilar.forEach(u => u.mitre.forEach(k => { (uy[k] = uy[k] || []).push(u); }));
  const teknikSay = Object.keys(D.mitre).length;
  const uyarili = Object.keys(uy).length;
  const uyarisayisi = D.uyarilar.filter(u => u.mitre.length).length;
  const cols = D.taktik_sirasi.map(tk => {
    const teknikler = Object.keys(D.mitre).filter(k => D.mitre[k].taktik === tk);
    return `<div class="mcol"><h4>${esc(tk)}<span>${teknikler.length}</span></h4><div class="tiles">${teknikler.map(k => `<button class="tile izl ${uy[k] ? 'var' : ''} ${S.mtSec.has(k) ? 'sel' : ''}" data-a="mtsec" data-p="${k}"><small>${k}</small><b>${esc(D.mitre[k].ad)}</b>${uy[k] ? `<span class="cnt">${uy[k].length}</span>` : ''}</button>`).join('')}</div></div>`;
  }).join('');
  const sec = Array.from(S.mtSec);
  let alt = '';
  if (sec.length) {
    const liste = [];
    const goruldu = new Set();
    sec.forEach(k => (uy[k] || []).forEach(u => { if (!goruldu.has(u.id)) { goruldu.add(u.id); liste.push(u); } }));
    let ortak = '';
    if (sec.length === 2) {
      const a = new Set((uy[sec[0]] || []).map(u => u.varlik));
      const o = Array.from(new Set((uy[sec[1]] || []).map(u => u.varlik).filter(v => a.has(v))));
      const ta = D.mitre[sec[0]].taktik, tb = D.mitre[sec[1]].taktik;
      const ikili = sec.join(tt(' ve '));
      ortak = `<div class="verdict dusuk" style="margin-top:20px">${o.length ? `<b>${ikili}</b> ${tt('için ortak varlıklar:')} ${o.map(esc).join(', ')}. ${ta !== tb ? tt('İki teknik farklı aşamalarda ({0}, {1}); aynı varlıkta ardışık aşamalar görülüyor.', esc(ta), esc(tb)) : tt('Her iki teknik de aynı aşamada.')}` : `<b>${ikili}</b> ${tt('için ortak varlık yok.')}`}</div>`;
    }
    alt = `<h3 class="sec">${sec.map(k => k + ' ' + esc(D.mitre[k].ad)).join(' · ')}</h3>${ortak}
    <div class="tw" style="margin-top:14px"><table class="t"><thead><tr><th>${tt('Varlık')}</th><th>${tt('Uyarı türü')}</th><th>${tt('Ne oldu')}</th><th>${tt('Kaynak')}</th><th>${tt('Gün')}</th><th>${tt('İnceleme')}</th></tr></thead><tbody>${liste.map(u => `<tr class="lnk" data-a="ac-inc" data-p="${u.inc}"><td>${esc(u.varlik)}</td><td>${esc(u.tur)}</td><td style="min-width:240px">${esc(u.ne)}</td><td>${esc(KAYNAK_AD(u.kaynak))}</td><td class="nw">${gunEt(u.gun)}</td><td class="nw">${oncBadge(INC[u.inc].oncelik)}</td></tr>`).join('') || `<tr><td colspan="6" style="text-align:center;color:var(--muted);padding:26px">${tt('Seçili teknikte bu dönemde uyarı yok')}</td></tr>`}</tbody></table></div>`;
  }
  return `<div class="top"><div><h1>MITRE ATT&amp;CK</h1><p class="sub">${tt('İzlenen teknikler ve bu dönemde uyarı üretenler')}</p></div></div>
  <div class="kpis3"><div class="kp"><b>${teknikSay}</b><span>${tt('izlenen teknik')}</span></div><div class="kp"><b>${uyarili}</b><span>${tt('teknikte uyarı var')}</span></div><div class="kp"><b>${uyarisayisi}</b><span>${tt('teknik etiketli uyarı')}</span></div><div class="kp"><b>${D.taktik_sirasi.length}</b><span>${tt('aşama')}</span></div></div>
  <div class="mgrid">${cols}</div>${alt || `<p class="note" style="margin-top:8px">${tt('Bir tekniğe tıklayın: o tekniğe düşen uyarılar altta listelenir. İki teknik seçerseniz ortak varlıkları görürsünüz.')}</p>`}`;
}

/* ---------------------------------------------------------------- ag gecisleri */
function viewAg(){
  const K = D.ag.kenarlar;
  const DIS_KAYNAK = D.ag.dis_kaynak;
  const toplam = k => K.reduce((a, e) => a + e[k], 0);
  const disUlasan = K.filter(e => DIS_KAYNAK.indexOf(e.kaynak) >= 0).reduce((a, e) => a + e.ulasan, 0);
  const kpi = `<div class="kpis3"><div class="kp"><b>${sayi(disUlasan)}</b><span>${tt('Dışarıdan kuruma ulaşan istek')}</span></div><div class="kp"><b>${sayi(toplam('reddedilen'))}</b><span>${tt('Reddedilen istek')}</span></div><div class="kp"><b>${D.ag.kumeler.length}</b><span>${tt('Ağ bölgesi')}</span></div><div class="kp"><b>${K.length}</b><span>${tt('Bölge çifti')}</span></div></div>`;
  const seg = `<div class="seg" style="margin-top:26px"><button class="${S.agTab === 'akis' ? 'on' : ''}" data-a="agtab" data-p="akis">${tt('Akış')}</button><button class="${S.agTab === 'matris' ? 'on' : ''}" data-a="agtab" data-p="matris">${tt('Matris')}</button></div>`;
  let govde;
  if (S.agTab === 'akis') {
    const gr = ['kuzey-güney', 'doğu-batı'].map(y => {
      const l = K.filter(e => e.yon === y).sort((a, b) => b.ulasan - a.ulasan);
      const ad = y === 'kuzey-güney' ? tt('Kurum sınırını geçen (kuzey-güney)') : tt('Kurum içi geçişler (doğu-batı)');
      const ust = `<tr class="gh"><td colspan="3">${ad} · ${tt('{0} bölge çifti', l.length)}</td><td class="n">${sayi(l.reduce((a, e) => a + e.ulasan, 0))}</td><td class="n">${sayi(l.reduce((a, e) => a + e.reddedilen, 0))}</td></tr>`;
      return ust + l.map(e => `<tr><td>${esc(e.kaynak)}</td><td>${esc(e.hedef)}</td><td style="color:var(--ink-2)">${esc(e.cihaz)}</td><td class="n">${sayi(e.ulasan)}</td><td class="n">${sayi(e.reddedilen)}</td></tr>`).join('');
    }).join('');
    govde = `<div class="tw" style="margin-top:18px"><table class="t"><thead><tr><th>${tt('Nereden')}</th><th>${tt('Nereye')}</th><th>${tt('Kaydeden cihaz')}</th><th class="n">${tt('Ulaşan')}</th><th class="n">${tt('Reddedilen')}</th></tr></thead><tbody>${gr}</tbody></table></div>`;
  } else {
    const kn = D.ag.kumeler;
    const anah = S.agMod;
    const mx = Math.max.apply(null, K.map(e => e[anah]));
    const renk = v => { if (!v) return ''; const r = Math.log10(v + 1) / Math.log10(mx + 1); const a = .12 + r * .88; return anah === 'ulasan' ? `background:rgba(21,136,103,${a.toFixed(2)});color:${a > .55 ? '#fff' : '#0b5a43'}` : `background:rgba(226,114,95,${a.toFixed(2)});color:${a > .55 ? '#fff' : '#7a2d1f'}`; };
    const satirKumeleri = kn.filter(k => K.some(e => e.kaynak === k));
    const sutunKumeleri = kn.filter(k => K.some(e => e.hedef === k));
    const bas = sutunKumeleri.map(k => `<th>${esc(k)}</th>`).join('');
    const govdeM = satirKumeleri.map(s => {
      const hucreler = sutunKumeleri.map(h => { const e = K.find(x => x.kaynak === s && x.hedef === h); return e && e[anah] ? `<td style="${renk(e[anah])}" title="${esc(s)} → ${esc(h)}: ${sayi(e[anah])}">${kisa(e[anah])}</td>` : '<td class="z">-</td>'; }).join('');
      const tp = K.filter(x => x.kaynak === s).reduce((a, x) => a + x[anah], 0);
      return `<tr><th class="rh">${esc(s)}</th>${hucreler}<td style="background:var(--soft);color:var(--ink);font-weight:700">${kisa(tp)}</td></tr>`;
    }).join('');
    govde = `<div style="margin-top:18px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap"><span class="mtl">${tt('Satır kaynak bölge, sütun hedef bölge. Renk logaritmik ölçekte.')}</span><div class="seg"><button class="${anah === 'ulasan' ? 'on' : ''}" data-a="agmod" data-p="ulasan">${tt('Ulaşan')}</button><button class="${anah === 'reddedilen' ? 'on' : ''}" data-a="agmod" data-p="reddedilen">${tt('Reddedilen')}</button></div></div>
    <div class="tw" style="margin-top:14px;padding:10px"><table class="heat"><thead><tr><th></th>${bas}<th>${tt('Toplam')}</th></tr></thead><tbody>${govdeM}</tbody></table></div>
    <p class="note" style="margin-top:14px">${anah === 'ulasan' ? tt('Matris toplamı: {0} istek, Akış sekmesindeki ulaşan toplamıyla aynıdır.', sayi(toplam(anah))) : tt('Matris toplamı: {0} istek, Akış sekmesindeki reddedilen toplamıyla aynıdır.', sayi(toplam(anah)))}</p>`;
  }
  return `<div class="top"><div><h1>${tt('Ağ geçişleri')}</h1><p class="sub">${tt('Bölgeler arası bağlantılar, hangi güvenlik cihazından geçtikleri')}</p></div></div>${kpi}${seg}${govde}`;
}
function kisa(n){
  const o = DIL === 'en' ? ['.', ' B', ' M', ' K'] : [',', ' Mr', ' Mn', ' B'];
  if (n >= 1e9) return (n / 1e9).toFixed(1).replace('.', o[0]) + o[1];
  if (n >= 1e6) return (n / 1e6).toFixed(1).replace('.', o[0]) + o[2];
  if (n >= 1e3) return (n / 1e3).toFixed(1).replace('.', o[0]) + o[3];
  return String(n);
}

/* ---------------------------------------------------------------- kisi sorgusu */
const NOKTA = {kirmizi:'var(--hi)', turuncu:'var(--md)', yesil:'var(--lo)', bilgi:'var(--sky)'};
function viewKisi(){
  const adlar = Object.keys(D.haftalar);
  const w = D.haftalar[S.kisi];
  const mx = Math.max.apply(null, w.gunler.map(g => g.istek).concat([1]));
  const hk = w.hukumler.map(h => `<div><span class="dot" style="--c:${NOKTA[h[0]]}"></span><span>${esc(h[1])}</span></div>`).join('');
  const satir = w.gunler.map(g => {
    const cip = g.ilk.map(i => `<span class="chp ${i[2] === 'kritik' ? 'kritik' : i[2] === 'uyari' ? 'uyari' : ''}">${esc(i[1])}</span>`).join('');
    return `<tr><td style="white-space:nowrap">${gunEt(g.gun)}</td><td><span class="barw"><span class="bar" style="width:${Math.round(g.istek / mx * 120)}px;--c:var(--sky)"></span><span>${sayi(g.istek)}</span></span></td><td class="n">${g.engel ? sayi(g.engel) : '-'}</td><td class="n">${g.oturum || '-'}</td><td class="n" style="${g.yonetici ? 'color:var(--hi-ink);font-weight:600' : ''}">${g.yonetici || '-'}</td><td>${cip || '<span style="color:var(--faint)">-</span>'}</td></tr>`;
  }).join('');
  const ilkler = w.ad_soyad.split(' ').map(x => x[0]).join('').slice(0, 2);
  const inc = D.incelemeler.find(i => i.varliklar.some(v => v.ad === S.kisi));
  return `<div class="top"><div><h1>${tt('Kişi sorgusu')}</h1><p class="sub">${tt('Bir kullanıcının yedi günü: hangi kayıt kaynağında ne yaptı')}</p></div></div>
  <div class="filters"><label class="search" style="min-width:320px">${icoS('search')}<input id="kisiara" list="kisiliste" type="search" placeholder="${tt('Kullanıcı adı yazın, örn. {0}', adlar[0])}" aria-label="${tt('Kullanıcı ara')}"></label>
    <datalist id="kisiliste">${adlar.map(a => `<option value="${a}">${esc(D.haftalar[a].ad_soyad)}</option>`).join('')}</datalist>
    <span class="mtl">${adlar.slice(0, 6).map(a => `<button class="chip ${a === S.kisi ? 'p' : ''}" data-a="kisisec" data-p="${a}">${a}</button>`).join(' ')}</span></div>
  <div class="kis-h"><div class="kav">${esc(ilkler)}</div><div><h2>${esc(w.ad_soyad)}</h2><p>${esc(w.unvan)} · ${esc(w.birim)} · ${tt('İK durumu:')} ${esc(w.ik)}</p></div>${inc ? `<button class="btn s" style="margin-left:auto" data-a="ac-inc" data-p="${inc.id}">${tt('İncelemeyi aç')} ${icoS('chevr')}</button>` : ''}</div>
  <div class="hk">${hk}</div>
  <h3 class="sec">${tt('Gün gün')}</h3>
  <div class="tw"><table class="t"><thead><tr><th>${tt('Gün')}</th><th>${tt('VPN istek')}</th><th class="n">${tt('Engellenen')}</th><th class="n">${tt('Oturum')}</th><th class="n">${tt('Yönetici yetkisi')}</th><th>${tt('O gün ilk kez')}</th></tr></thead><tbody>${satir}</tbody></table></div>
  <p class="note">${tt('Çözünürlük gündür. Dönemin ilk günü taban sayılır, o günün ilk görülenleri listelenmez.')}</p>`;
}

/* ---------------------------------------------------------------- kaynaklar */
function viewKaynaklar(){
  const rows = D.veri_kaynaklari.map(k => {
    const u = D.uyarilar.filter(x => x.kaynak === k.kod).length;
    return `<tr><td><b style="font-weight:600">${esc(k.ad)}</b></td><td>${esc(k.sistem)}</td><td>${esc(k.aralik)}</td><td><span class="ok">${esc(k.durum)}</span></td><td class="n">${u}</td></tr>`;
  }).join('');
  return `<div class="top"><div><h1>${tt('Veri kaynakları')}</h1><p class="sub">${tt('Okunan kayıtlar ve bunları anlamlandıran bağlam dosyaları')}</p></div></div>
  <h3 class="sec">${tt('Kayıt kaynakları')}</h3>
  <div class="tw"><table class="t"><thead><tr><th>${tt('Kayıt kaynağı')}</th><th>${tt('Sistem')}</th><th>${tt('Kayıt aralığı')}</th><th>${tt('Durum')}</th><th class="n">${tt('Uyarı')}</th></tr></thead><tbody>${rows}</tbody></table></div>
  <h3 class="sec">${tt('Bağlam')}</h3>
  <div class="kcards">${D.baglam.map(b => `<div class="kc"><b>${esc(b.ad)}</b><p>${esc(b.ne)}</p><em>${esc(b.kayit)}</em></div>`).join('')}</div>
  <p class="note">${tt('Kayıtlar kurum dışına çıkmaz. Bağlam dosyaları uyarıdaki her adres ve hesabın kim ya da ne olduğunu bulmak için kullanılır.')}</p>`;
}

/* ---------------------------------------------------------------- cekmece */
function cekmece(){
  const d = $('#drawer');
  if (!S.drawer) { d.classList.remove('acik'); return; }
  let govde = '', baslik = '';
  if (S.drawer === 'varlik') {
    baslik = tt('Varlıklar');
    const harita = {};
    D.incelemeler.forEach(inc => inc.varliklar.forEach(v => { if (!harita[v.ad]) harita[v.ad] = {v, inc}; }));
    const q = norm(S.drAra);
    const liste = Object.values(harita).filter(x => !q || norm(x.v.ad + ' ' + x.v.alt).indexOf(q) >= 0);
    govde = `<label class="search" style="min-width:0;margin-bottom:8px">${icoS('search')}<input id="drara" type="search" placeholder="${tt('Varlık ara')}" value="${esc(S.drAra)}"></label>` + (liste.map(x => `<button class="ent" data-a="ac-inc" data-p="${x.inc.id}"><span class="ei">${ico(TIP_IC[x.v.tip])}</span><span><b>${esc(x.v.ad)}</b><small>${TIP_AD[x.v.tip]} · ${esc(x.v.alt)}</small></span>${oncBadge(x.inc.oncelik)}</button>`).join('') || `<p class="bos" style="color:var(--muted);padding:12px 0">${tt('Eşleşen varlık yok')}</p>`);
  } else {
    baslik = tt('Sabitlenenler');
    const l = Array.from(S.sabit).map(x => INC[x]);
    govde = l.map(inc => `<button class="ent" data-a="ac-inc" data-p="${inc.id}"><span class="ei">${ico('pin')}</span><span><b style="text-transform:uppercase">${esc(inc.baslik)}</b><small>${esc(inc.tur_ad)} · ${tt('{0} uyarı', inc.uyarilar.length)}</small></span>${oncBadge(inc.oncelik)}</button>`).join('') || `<p class="bos" style="color:var(--muted);padding:12px 0">${tt('Henüz sabitlenen inceleme yok. İnceleme dosyasında Sabitle düğmesini kullanın.')}</p>`;
  }
  d.innerHTML = `<div class="dr-h"><h3>${baslik}</h3><button class="dr-x" data-a="cekmece-kapat" aria-label="${tt('Kapat')}">${ico('x')}</button></div><div class="dr-b">${govde}</div>`;
  d.classList.add('acik');
}

/* ---------------------------------------------------------------- sohbet */
const SORULAR = [
  {id:'ozet', et:tt('Özetle'), k:DIL === 'en' ? ['summar', 'overview', 'what happened', 'explain', 'tell me', 'brief'] : ['ozet', 'anlat', 'kisaca', 'ne oldu', 'nedir'],
    f:c => `<p>${esc(c.ozet)}</p><ul>${(c.nedenler.length ? c.nedenler : c.metrikler.map(m => m[0] + ' ' + m[1])).map(n => `<li>${esc(n)}</li>`).join('')}</ul>`, d:c => tt('{0} uyarının kaydından', c.uyarilar.length)},
  {id:'degisti', et:tt('Ne değişti?'), k:DIL === 'en' ? ['change', 'timeline', 'when', 'first', 'order', 'start'] : ['degis', 'zaman', 'ne zaman', 'ilk', 'sira', 'baslad'],
    f:c => { const z = c.zaman.slice().sort((a, b) => (a.gun + a.saat) < (b.gun + b.saat) ? -1 : 1); return `<p>${tt('Kayıtlardaki olayların sırası:')}</p><ul>${z.slice(0, 5).map(x => `<li><b>${gunEt(x.gun)}${x.saat ? ' ' + x.saat : ''}</b>, ${esc(x.baslik)}</li>`).join('')}</ul>`; }, d:c => tt('Zaman sekmesinden'), a:[[tt('Zamanı göster'), 'tab:zaman']]},
  {id:'kim', et:tt('Kim ya da ne etkileniyor?'), k:DIL === 'en' ? ['who', 'people', 'which', 'entity', 'entities', 'address', 'account', 'affected'] : ['kim', 'kisi', 'hangi', 'varlik', 'adres', 'kimler', 'hesap'],
    f:c => `<table class="t"><thead><tr><th>${tt('Varlık')}</th><th>${tt('Ayrıntı')}</th></tr></thead><tbody>${c.varliklar.slice(0, 6).map(v => `<tr><td><span class="who">${esc(v.ad)}</span></td><td>${esc(v.alt)}</td></tr>`).join('')}</tbody></table>${c.varliklar.length > 6 ? `<p class="dyk">${tt('+{0} varlık daha, Uyarılar sekmesinde', c.varliklar.length - 6)}</p>` : ''}`, d:c => tt('{0} varlığın kaydından', c.varliklar.length), a:[[tt('Uyarıları göster'), 'tab:uyarilar']]},
  {id:'sor', et:tt('Kimlere sorulur?'), k:DIL === 'en' ? ['who to ask', 'who should i ask', 'should i ask', 'owner', 'team', 'ask', 'responsible', 'contact'] : ['kime', 'kimlere', 'sorumlu', 'sahip', 'ekip', 'sorulur'],
    f:c => `<table class="t"><thead><tr><th>${tt('Konu')}</th><th>${tt('Kime')}</th></tr></thead><tbody>${c.adimlar.map(a => `<tr><td>${esc(a[0])}</td><td>${esc(a[2])}</td></tr>`).join('')}</tbody></table>`, d:c => tt('Adımlar bölümünden')},
  {id:'mitre', et:tt('MITRE eşlemesi'), k:['mitre', 'technique', 'tactic', 'teknik', 'taktik', 'att&ck'],
    f:c => c.mitre.length ? `<p>${tt('Bu inceleme {0} tekniğin izine düşüyor:', c.mitre.length)}</p><ul>${c.mitre.map(k => `<li><b>${k}</b> ${esc(D.mitre[k].ad)}, ${tt('aşama:')} ${esc(D.mitre[k].taktik)}</li>`).join('')}</ul>` : `<p>${tt('Bu inceleme bir saldırı tekniğiyle eşlenmiyor; operasyonel bir bulgudur.')}</p>`, d:c => tt('Uyarıların teknik etiketlerinden'), a:[[tt('MITRE sayfasını aç'), 'git:mitre']]},
  {id:'saldiri', et:tt('Bu bir saldırı mı?'), k:DIL === 'en' ? ['attack', 'malicious', 'threat', 'dangerous', 'real', 'breach'] : ['saldiri', 'kotu', 'zararli', 'tehdit', 'tehlikeli', 'gercek'],
    f:c => c.lehine.length ? `<p>${tt('Kayıt bunu tek başına söyleyemez. Görülen davranış bir tekniğin izi olabilir, başka açıklamaları da olabilir.')}</p><table class="t"><thead><tr><th>${tt('Bir saldırıyı düşündüren')}</th><th>${tt('Başka açıklamayı düşündüren')}</th></tr></thead><tbody>${c.lehine.map((x, i) => `<tr><td>${esc(x)}</td><td>${esc(c.aleyhine[i] || '')}</td></tr>`).join('')}</tbody></table>` : `<p>${tt('Kayıt bunu tek başına söyleyemez. Bu inceleme için belirleyici bilgi eksik bilgi listesinde.')}</p>`, d:c => tt('Kanıt ve eksik bilgi bölümlerinden'), a:[[tt('Eksik bilgiyi göster'), 'tab:eksik']]},
  {id:'eksik', et:tt('Neler eksik?'), k:DIL === 'en' ? ['missing', 'unknown', 'unanswered', 'gap', 'lack'] : ['eksik', 'bilinmiyor', 'bilinmeyen', 'cevaplanamayan', 'yok'],
    f:c => `<ul>${c.eksik.map(e => `<li><b>${esc(e[0])}</b>, ${tt('cevabı:')} ${esc(e[2])}</li>`).join('')}</ul>`, d:c => tt('{0} eksik bilgi', c.eksik.length), a:[[tt('Eksik bilgiyi göster'), 'tab:eksik']]},
  {id:'ham', et:tt('Ham kayıtlar nerede?'), k:DIL === 'en' ? ['raw', 'log', 'line', 'file', 'evidence', 'original'] : ['ham', 'log', 'satir', 'dosya', 'kanit', 'orijinal'],
    f:c => `<p>${tt('Bu incelemenin ham kayıt satırları <b>Kanıt</b> sekmesinde. {0} satırdan {1} tanesi ekranda, tamamı {2} dosyasında.', sayi(c.ham.toplam), c.ham.satirlar.length, `<span class="who">ham_kanit/${esc(c.ham.dosya)}</span>`)}</p>`, d:c => tt('Ham kayıt paketinden'), a:[[tt('Kanıtı göster'), 'tab:kanit']]}
];
const feed = () => $('#feed');
function sohbetKaydir(){ const f = feed(); f.scrollTop = f.scrollHeight; }
function chatDolu(){ $('#chat').classList.add('dolu'); }
function kullaniciMsg(m){
  const d = document.createElement('div'); d.className = 'msg u'; d.textContent = m; feed().appendChild(d); chatDolu(); sohbetKaydir();
}
function botMsg(html, opts){
  opts = opts || {};
  chatDolu();
  const el = document.createElement('div'); el.className = 'msg a'; el.innerHTML = '<div class="typing"><i></i><i></i><i></i></div>'; feed().appendChild(el); sohbetKaydir();
  const yaz = () => {
    const chips = (opts.chips || []).map(c => `<button class="chip ${c.p ? 'p' : ''}" data-a="chip" data-p="${esc(c.a)}">${esc(c.et)}</button>`).join('');
    el.innerHTML = `<div class="who"><img src="${ASSET}favicon-64.png" alt="">Deepin Security</div>${html}${opts.dayanak ? `<p class="dyk">${esc(opts.dayanak)}</p>` : ''}${chips ? `<div class="chips">${chips}</div>` : ''}`;
    sohbetKaydir();
  };
  if (opts.hemen) yaz(); else zamanla(yaz, 520 + Math.min(500, html.length / 3));
}
function hizliSorular(){}
function brifing(hemen){
  const l = gorunen();
  const y = l.filter(x => x.inc.oncelik === 'yuksek');
  const uy = l.reduce((a, x) => a + x.u.length, 0);
  const kartlar = (y.length ? y : l).slice(0, 3).map(x => `<button data-a="mini" data-p="${x.inc.id}" class="${x.inc.oncelik}"><b>${esc(x.inc.baslik)}</b><span class="r">${tt('{0} uyarı', x.u.length)}</span><small>${esc(x.inc.kart_ozet)}</small></button>`).join('');
  botMsg(`<p>${tt('Bugün dikkat isteyen <b>{0} inceleme</b> var. Toplam {1} inceleme arasından {2} tanesi yüksek öncelikli.', y.length, l.length, y.length)}</p><div class="kpis"><div><b>${uy}</b><span>${tt('uyarı')}</span></div><div><b>${l.length}</b><span>${tt('inceleme')}</span></div><div><b style="color:var(--hi)">${y.length}</b><span>${tt('yüksek')}</span></div><div><b>${new Set(l.flatMap(x => x.inc.kaynaklar)).size}</b><span>${tt('kaynak')}</span></div></div><div class="mini">${kartlar}</div>`, {dayanak:tt('{0} dönemi kayıtlarından', D.donem.etiket), hemen:hemen});
}
function incBaglami(){
  if (!S.incId) return;
  const inc = INC[S.incId];
  botMsg(`<p>${tt('<b>{0}</b> incelemesini açtım.', esc(inc.baslik))} ${tt('{0} uyarı', inc.uyarilar.length)}, ${tt('{0} kaynak', inc.kaynaklar.length)}. ${tt('Şunları sorabilirsiniz:')}</p>`, {chips:['ozet', 'saldiri', 'sor', 'eksik'].map(id => ({et:SORULAR.find(s => s.id === id).et, a:'soru:' + id})), hemen:true});
}
let sohbetCtx = null;
function sohbetGuncelle(){
  $('#geri').hidden = false;
  const yeniCtx = S.incId;
  if (yeniCtx && yeniCtx !== sohbetCtx) { sohbetCtx = yeniCtx; incBaglami(); }
  else if (!yeniCtx) sohbetCtx = null;
}
function cevapla(id){
  if (!S.incId) return;
  const inc = INC[S.incId];
  const s = SORULAR.find(x => x.id === id);
  window.__sonCevap = id;
  kullaniciMsg(s.et);
  botMsg(s.f(inc), {dayanak:s.d(inc), chips:(s.a || []).map(a => ({et:a[0], a:a[1], p:true}))});
}
function genelSoru(m){
  kullaniciMsg(m);
  const l = gorunen();
  if (m === tt('Bugün ne var?')) return brifing();
  if (m === tt('En önemli inceleme')) { const x = l[0]; if (!x) return botMsg(`<p>${tt('Bu dönemde inceleme yok.')}</p>`); return botMsg(`<p>${tt('En önemli inceleme <b>{0}</b>.', esc(x.inc.baslik))}</p><p style="margin-top:6px">${esc(x.inc.ozet)}</p>`, {dayanak:tt('{0} uyarının kaydından', x.u.length), chips:[{et:tt('İncelemeyi aç'), a:'ac:' + x.inc.id, p:true}]}); }
  const y = l.filter(x => x.inc.oncelik === 'yuksek');
  botMsg(`<p>${tt('{0} yüksek öncelikli inceleme var:', y.length)}</p><div class="mini">${y.map(x => `<button data-a="mini" data-p="${x.inc.id}" class="yuksek"><b>${esc(x.inc.baslik)}</b><span class="r">${tt('{0} uyarı', x.u.length)}</span><small>${esc(x.inc.kart_ozet)}</small></button>`).join('')}</div>`, {dayanak:tt('Öncelik sırasına göre')});
}
function serbest(text){
  const q = norm(text).trim();
  if (!q) return;
  kullaniciMsg(text);
  if (S.incId) {
    const inc = INC[S.incId];
    let en = null, sk = 0;
    SORULAR.forEach(s => { const p = s.k.reduce((a, k) => a + (q.indexOf(norm(k)) >= 0 ? 1 : 0), 0); if (p > sk) { sk = p; en = s; } });
    if (en) { window.__sonCevap = en.id; return botMsg(en.f(inc), {dayanak:en.d(inc), chips:(en.a || []).map(a => ({et:a[0], a:a[1], p:true}))}); }
  }
  const bulunan = D.incelemeler.filter(i => norm(i.baslik + ' ' + i.varliklar.map(v => v.ad + ' ' + v.alt).join(' ')).indexOf(q) >= 0 || q.split(' ').some(w => w.length > 3 && norm(i.baslik + ' ' + i.varliklar.map(v => v.ad).join(' ')).split(' ').indexOf(w) >= 0));
  window.__sonCevap = bulunan.length ? 'arama' : 'yok';
  if (bulunan.length) return botMsg(`<p>${tt('{0} inceleme buldum:', bulunan.length)}</p><div class="mini">${bulunan.slice(0, 3).map(i => `<button data-a="mini" data-p="${i.id}" class="${i.oncelik}"><b>${esc(i.baslik)}</b><span class="r">${tt('{0} uyarı', i.uyarilar.length)}</span><small>${esc(i.kart_ozet)}</small></button>`).join('')}</div>`, {dayanak:tt('İnceleme ve varlık adlarında arandı')});
  botMsg(`<p>${tt('Bu soruya cevap verecek bir alan kayıtlarda yok.')}${S.incId ? ' ' + tt('Şu sorular bu incelemenin kayıtlarından cevaplanabilir:') : ' ' + tt('Bir incelemeyi ya da varlık adını yazabilirsiniz.')}</p>`, {chips:S.incId ? SORULAR.slice(0, 5).map(s => ({et:s.et, a:'soru:' + s.id})) : [{et:tt('Bugün ne var?'), a:'genel:' + tt('Bugün ne var?')}]});
}
function chipEylem(a){
  const [tur, p] = a.split(/:(.+)/);
  if (tur === 'soru') cevapla(p);
  else if (tur === 'tab') { git('inc/' + S.incId + '/' + p); }
  else if (tur === 'git') git(p);
  else if (tur === 'ac') git('inc/' + p);
  else if (tur === 'genel') genelSoru(p);
}

/* ---------------------------------------------------------------- cizim */
function toast(m){ const el = $('#toast'); el.textContent = m; el.classList.add('g'); zamanIptal(toast.z); toast.z = zamanla(() => el.classList.remove('g'), 2400); }
function render(korunacak){
  if (!rotaOku()) return;
  const card = $('#card');
  const yer = korunacak ? card.scrollTop : 0;
  const govde = S.rota === 'inc' ? viewInc() : ({home:viewHome, uyarilar:viewUyarilar, mitre:viewMitre, ag:viewAg, kisi:viewKisi, kaynaklar:viewKaynaklar}[S.rota] || viewHome)();
  card.innerHTML = govde;
  card.scrollTop = yer;
  $$('.rb[data-r]').forEach(b => b.classList.toggle('on', b.dataset.r === (S.rota === 'inc' ? (S.tab === 'graf' ? 'graf' : 'home') : S.rota)));
  document.title = (S.rota === 'inc' ? INC[S.incId].baslik + ' · ' : '') + 'deepin | security';
  sohbetGuncelle();
  if (S.drawer) cekmece();
}

/* ---------------------------------------------------------------- olaylar */
document.addEventListener('click', e => {
  const el = e.target.closest('[data-a]');
  const acikMenu = $$('.sort.acik, .donem.acik');
  if (acikMenu.length && !e.target.closest('.sort, .donem')) acikMenu.forEach(m => m.classList.remove('acik'));
  if (!el) return;
  const a = el.dataset.a, p = el.dataset.p;
  switch (a) {
    case 'nav': git(p); if (window.innerWidth <= 1040) $('#chat').classList.remove('acik'); break;
    case 'geri': geri(); break;
    case 'risk': S.risk = p; render(true); break;
    case 'sirala': S.sirala = p; render(true); break;
    case 'donem': S.donem = p; render(true); break;
    case 'donem-menu': $('#donem').classList.toggle('acik'); break;
    case 'sort-menu': $('#sort').classList.toggle('acik'); break;
    case 'satir-ac': e.stopPropagation(); if (S.acik.has(p)) S.acik.delete(p); else S.acik.add(p); { const r = el.closest('.row'); r.classList.toggle('acik'); el.setAttribute('aria-expanded', r.classList.contains('acik')); } break;
    case 'ac-inc': git('inc/' + p); break;
    case 'tab': git('inc/' + S.incId + '/' + p); break;
    case 'sabit': if (S.sabit.has(p)) S.sabit.delete(p); else S.sabit.add(p); kaydetSabit(); render(true); toast(S.sabit.has(p) ? tt('İnceleme sabitlendi') : tt('Sabitleme kaldırıldı')); break;
    case 'adim': { const [i, n] = p.split('|'); S.adim[i + n] = !S.adim[i + n]; render(true); break; }
    case 'gkisi': { const [i, k] = p.split('|'); S.gkisi[i] = k; S.gdugum = null; render(true); break; }
    case 'dugum': S.gdugum = S.gdugum === p ? null : p; render(true); break;
    case 'mtsec': if (S.mtSec.has(p)) S.mtSec.delete(p); else { if (S.mtSec.size >= 2) S.mtSec.delete(Array.from(S.mtSec)[0]); S.mtSec.add(p); } render(true); break;
    case 'agtab': S.agTab = p; render(true); break;
    case 'agmod': S.agMod = p; render(true); break;
    case 'kisisec': git('kisi/' + p); break;
    case 'cekmece': S.drawer = S.drawer === p ? null : p; S.drAra = ''; cekmece(); break;
    case 'cekmece-kapat': S.drawer = null; cekmece(); break;
    case 'dil': if (p !== DIL) { try { localStorage.setItem('dsec_dil', p); } catch (e) {} location.href = (p === 'en' ? 'en/index.html' : '../index.html') + location.hash; } break;
    case 'chat-ac': $('#chat').classList.toggle('acik'); break;
    case 'brifing': kullaniciMsg(tt('Günlük özet')); brifing(); break;
    case 'soru': cevapla(p); break;
    case 'genel-soru': genelSoru(p); break;
    case 'chip': chipEylem(p); break;
    case 'mini': git('inc/' + p); break;
  }
});
document.addEventListener('change', e => {
  const el = e.target.closest('[data-a]');
  if (!el) return;
  if (el.dataset.a === 'uyonc') { S.uyOnc = el.value; render(true); }
  if (el.dataset.a === 'uykay') { S.uyKay = el.value; render(true); }
  if (el.dataset.a === 'uysira') { S.uySira = el.value; render(true); }
  if (e.target.id === 'kisiara') { const v = e.target.value.trim().toLowerCase(); const b = Object.keys(D.haftalar).find(a => a === v); if (b) git('kisi/' + b); }
});
document.addEventListener('input', e => {
  if (e.target.id === 'uyara') { S.uyAra = e.target.value; const c = $('#card'); const y = c.scrollTop; render(true); const i = $('#uyara'); i.focus(); i.setSelectionRange(i.value.length, i.value.length); c.scrollTop = y; }
  if (e.target.id === 'drara') { S.drAra = e.target.value; cekmece(); const i = $('#drara'); i.focus(); i.setSelectionRange(i.value.length, i.value.length); }
  if (e.target.id === 'kisiara') { const v = e.target.value.trim().toLowerCase(); if (D.haftalar[v]) git('kisi/' + v); }
});
document.addEventListener('keydown', e => {
  if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('[data-a="ac-inc"][role="link"], .gnode, .step i')) { e.preventDefault(); e.target.dispatchEvent(new MouseEvent('click', {bubbles:true})); }
  if (e.key === 'Escape') { if (S.drawer) { S.drawer = null; cekmece(); } $$('.sort.acik, .donem.acik').forEach(m => m.classList.remove('acik')); }
});
document.addEventListener('submit', e => {
  if (e.target.id === 'ask') { e.preventDefault(); const i = $('#askin'); const v = i.value; i.value = ''; serbest(v); }
});
window.addEventListener('hashchange', () => render(false));

/* panel boyutlandirma */
(function(){
  let s = null;
  document.addEventListener('mousedown', e => { if (e.target.closest('#handle')) { s = {x:e.clientX, w:$('#chat').offsetWidth}; document.body.style.userSelect = 'none'; e.preventDefault(); } });
  document.addEventListener('mousemove', e => { if (!s) return; const w = Math.max(300, Math.min(620, s.w + e.clientX - s.x)); document.documentElement.style.setProperty('--panel', w + 'px'); });
  document.addEventListener('mouseup', () => { s = null; document.body.style.userSelect = ''; });
})();

iskelet();
render(false);
})();
