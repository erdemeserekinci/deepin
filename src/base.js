
(function(){
  // Outside the live domain (local file, preview), folder links need an explicit index.html
  if(!/(^|\.)deepin\.space$/.test(location.hostname)){
    document.querySelectorAll('a[href]').forEach(function(a){
      var h=a.getAttribute('href');
      if(h&&!/^([a-z]+:|#|\/)/i.test(h)&&/\/$/.test(h))a.setAttribute('href',h+'index.html');
    });
  }
  // Inside a frame (e.g. a preview window) the scroll position belongs to the outer page,
  // so the browser neither starts a new page at its top nor restores the spot on Back.
  // Remember the link a visitor leaves through, and on load scroll the frame's own
  // content: back to that link after Back, to the top (or #section) otherwise.
  if(window.top!==window){
    var POS='deepin-pos:'+location.pathname,user=false;
    try{if('scrollRestoration' in history)history.scrollRestoration='manual'}catch(e){}
    document.addEventListener('click',function(ev){
      var a=ev.target.closest&&ev.target.closest('a[href]');if(!a)return;
      var h=a.getAttribute('href');if(!h||h.charAt(0)==='#'||/^(mailto|tel|javascript):/i.test(h))return;
      try{sessionStorage.setItem(POS,[].indexOf.call(document.querySelectorAll('a[href]'),a))}catch(e){}
    },true);
    ['wheel','touchstart','keydown','mousedown'].forEach(function(t){window.addEventListener(t,function(){user=true},{passive:true,once:true})});
    var nav0=performance.getEntriesByType&&performance.getEntriesByType('navigation')[0],back=!!nav0&&nav0.type==='back_forward';
    var land=function(){
      if(user)return;
      var t=null,i=null;
      if(back){try{i=sessionStorage.getItem(POS)}catch(e){}if(i!==null)t=document.querySelectorAll('a[href]')[+i]}
      if(!t&&location.hash){try{t=document.querySelector(location.hash)}catch(e){}}
      if(t)t.scrollIntoView({block:back?'center':'start'});
      else{window.scrollTo(0,0);document.documentElement.scrollIntoView({block:'start'})}
    };
    if(!back){try{sessionStorage.removeItem(POS)}catch(e){}}
    // run now, and again once the page has settled (a preview window may restore its own position late)
    land();requestAnimationFrame(land);
    window.addEventListener('load',function(){land();setTimeout(land,150);setTimeout(land,450)});
    window.addEventListener('pageshow',function(ev){if(ev.persisted){back=true;user=false;land()}});
  }
  // remember the language the visitor picks
  document.querySelectorAll('.langs a[hreflang]').forEach(function(a){
    a.addEventListener('click',function(){try{localStorage.setItem('deepin-lang',a.getAttribute('hreflang'))}catch(e){}});
  });
  // sticky nav border
  var nav=document.querySelector('.nav');
  var onScroll=function(){nav.classList.toggle('scrolled',window.scrollY>8)};
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();

  // copy email
  var btn=document.getElementById('copyBtn'),em=document.getElementById('email');
  if(btn&&em)btn.addEventListener('click',function(){
    var label=btn.textContent;
    var done=function(){btn.textContent=btn.getAttribute('data-copied')||'Copied';setTimeout(function(){btn.textContent=label},1800)};
    var fallback=function(){var r=document.createRange();r.selectNodeContents(em);var s=getSelection();s.removeAllRanges();s.addRange(r);btn.textContent=btn.getAttribute('data-selected')||'Selected';};
    try{navigator.clipboard.writeText(em.textContent).then(done,fallback)}catch(e){fallback()}
  });


  // signal line through the process steps
  var NS='http://www.w3.org/2000/svg';
  function el(n,a){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);return e}
  function smooth(p){ // Catmull-Rom -> cubic bezier
    var d='M'+p[0][0]+' '+p[0][1];
    for(var i=0;i<p.length-1;i++){
      var p0=p[i-1]||p[i],p1=p[i],p2=p[i+1],p3=p[i+2]||p2;
      d+=' C'+(p1[0]+(p2[0]-p0[0])/6).toFixed(1)+' '+(p1[1]+(p2[1]-p0[1])/6).toFixed(1)+','+(p2[0]-(p3[0]-p1[0])/6).toFixed(1)+' '+(p2[1]-(p3[1]-p1[1])/6).toFixed(1)+','+p2[0].toFixed(1)+' '+p2[1].toFixed(1);
    }
    return d;
  }
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function drawFlows(){
    document.querySelectorAll('.flow-wrap').forEach(function(w,wi){
      var svg=w.querySelector('.flow-line'),lis=[].slice.call(w.querySelectorAll('.flow > li'));
      var oneRow=lis.length&&lis.every(function(li){return li.offsetTop===lis[0].offsetTop});
      w.classList.toggle('drawn',oneRow);
      while(svg.firstChild)svg.removeChild(svg.firstChild);
      if(!oneRow)return;
      var W=w.clientWidth,mid=40,amp=9,pts=[[0,mid+amp*0.6]];
      var nodes=lis.map(function(li,i){return [li.offsetLeft+26,mid+(i%2?-amp:amp)]});
      pts=pts.concat(nodes,[[W,mid-amp*0.6]]);
      svg.setAttribute('viewBox','0 0 '+W+' 80');
      var gid='fg'+wi,g=el('linearGradient',{id:gid,x1:'0',x2:'1',y1:'0',y2:'0'});
      [[0,.1],[.25,.55],[.7,1],[1,.25]].forEach(function(s){g.appendChild(el('stop',{offset:s[0],style:'stop-color:var(--accent);stop-opacity:'+s[1]}))});
      var defs=el('defs',{});defs.appendChild(g);svg.appendChild(defs);
      var d=smooth(pts);
      svg.appendChild(el('path',{d:smooth(pts.map(function(p,i){return [p[0],mid+(mid-p[1])*0.7]})),class:'ghost'}));
      var trace=el('path',{d:d,class:'trace',stroke:'url(#'+gid+')',id:'ft'+wi});svg.appendChild(trace);
      var keyIdx=lis.findIndex(function(li){return li.classList.contains('human')});
      nodes.forEach(function(p,i){
        if(i===keyIdx){svg.appendChild(el('circle',{cx:p[0],cy:p[1],r:15,class:'halo'}));svg.appendChild(el('circle',{cx:p[0],cy:p[1],r:7,class:'node key'}))}
        else svg.appendChild(el('circle',{cx:p[0],cy:p[1],r:5,class:'node'}));
      });
      if(still||keyIdx<0)return;
      // pulse travels the line and waits at the approval step
      var total=trace.getTotalLength(),kx=nodes[keyIdx][0],lo=0,hi=total;
      for(var n=0;n<30;n++){var m=(lo+hi)/2;if(trace.getPointAtLength(m).x<kx)lo=m;else hi=m}
      var k=(lo/total).toFixed(3);
      var pulse=el('circle',{r:3.5,class:'pulse'});
      var am=el('animateMotion',{dur:'9s',repeatCount:'indefinite',calcMode:'linear',keyPoints:'0;'+k+';'+k+';1',keyTimes:'0;0.55;0.75;1'});
      var mp=el('mpath',{});mp.setAttributeNS('http://www.w3.org/1999/xlink','href','#ft'+wi);mp.setAttribute('href','#ft'+wi);
      am.appendChild(mp);pulse.appendChild(am);svg.appendChild(pulse);
    });
  }
  drawFlows();
  var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(drawFlows,120)});
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(drawFlows);


  // live investigation replay (resting state = complete case); any figure with [data-live]
  document.querySelectorAll('[data-live]').forEach(function(card){
    if(still)return;
    var bar=[].slice.call(card.querySelectorAll('.live-bar li')),st=card.querySelector('[data-live-status]');
    var parts=[].slice.call(card.querySelectorAll('[data-s]'));
    var labels=[];try{labels=JSON.parse(card.getAttribute('data-labels')||'[]')}catch(e){}
    var last=parts.reduce(function(m,p){return Math.max(m,+p.getAttribute('data-s'))},0);
    var step=-1,timer=null,visible=false,restCls=st?st.className:'';
    function paint(){
      bar.forEach(function(b,i){b.className=i<step?'done':(i===step?'on':'')});
      parts.forEach(function(p){var s=+p.getAttribute('data-s');p.classList.toggle('later',s>step);p.classList.toggle('on',s===step)});
      if(st&&labels.length){st.textContent=labels[Math.min(step,labels.length-1)];st.className='chip '+(step===last?restCls.replace('chip ',''):'st-deploying')}
    }
    function rest(){card.classList.remove('playing');parts.forEach(function(p){p.classList.remove('later','on')});bar.forEach(function(b){b.className=''});if(st&&labels.length){st.textContent=labels[labels.length-1];st.className=restCls}}
    function tick(){
      if(!visible){timer=null;rest();step=-1;return}
      step++;
      if(step>last){rest();step=-1;timer=setTimeout(tick,5200);return}
      card.classList.add('playing');paint();
      timer=setTimeout(tick,step===last?1800:(last>7?900:1250));
    }
    new IntersectionObserver(function(en){visible=en[0].isIntersecting;if(visible&&!timer)timer=setTimeout(tick,900)},{threshold:.35}).observe(card);
  });

  // homepage: fragmented human investigation paths
  function drawTangles(){
    document.querySelectorAll('.tangle').forEach(function(t){
      var svg=t.querySelector('.tangle-paths'),edges=[];
      try{edges=JSON.parse(t.getAttribute('data-edges')||'[]')}catch(e){}
      [].slice.call(svg.querySelectorAll('path:not(marker path)')).forEach(function(p){p.remove()});
      [].slice.call(t.querySelectorAll('.tg-lbl')).forEach(function(l){l.remove()});
      var box=t.getBoundingClientRect(),labels=[];
      function r(id){var el=document.getElementById(id);if(!el)return null;var b=el.getBoundingClientRect();return{x:b.left-box.left,y:b.top-box.top,w:b.width,h:b.height,cx:b.left-box.left+b.width/2,cy:b.top-box.top+b.height/2}}
      function clip(a,tx,ty){ // point on rect a's border toward (tx,ty)
        var dx=tx-a.cx,dy=ty-a.cy;if(!dx&&!dy)return[a.cx,a.cy];
        var sx=dx?(a.w/2+3)/Math.abs(dx):1e9,sy=dy?(a.h/2+3)/Math.abs(dy):1e9,s=Math.min(sx,sy);
        return[a.cx+dx*s,a.cy+dy*s];
      }
      edges.forEach(function(ed,i){
        var A=r(ed[0]),B=r(ed[1]);if(!A||!B)return;
        var back=ed[2]==='b',p0=clip(A,B.cx,B.cy),p3=clip(B,A.cx,A.cy);
        var dx=p3[0]-p0[0],dy=p3[1]-p0[1],len=Math.hypot(dx,dy)||1,nx=-dy/len,ny=dx/len;
        var k=(back?0.42:0.16)*(i%2?1:-1)*(back?-1:1),off=len*k;
        var c1=[p0[0]+dx*.3+nx*off,p0[1]+dy*.3+ny*off],c2=[p0[0]+dx*.7+nx*off,p0[1]+dy*.7+ny*off];
        var p=document.createElementNS('http://www.w3.org/2000/svg','path');
        p.setAttribute('d','M'+p0.join(' ')+' C'+c1.join(' ')+' '+c2.join(' ')+' '+p3.join(' '));
        if(back)p.setAttribute('class','b');
        p.setAttribute('marker-end','url(#tg-arrow)');
        svg.appendChild(p);
        if(ed[3]){
          var mx=.125*p0[0]+.375*c1[0]+.375*c2[0]+.125*p3[0],my=.125*p0[1]+.375*c1[1]+.375*c2[1]+.125*p3[1];
          var l=document.createElement('span');l.className='tg-lbl';l.textContent=ed[3];t.appendChild(l);
          var lw=l.offsetWidth,lh=l.offsetHeight,rects=[].slice.call(t.querySelectorAll('.tn')).map(function(n){var b=n.getBoundingClientRect();return{x:b.left-box.left,y:b.top-box.top,w:b.width,h:b.height}});
          var placed=labels||[];
          function hit(x,y){var L={x:x-lw/2-2,y:y-lh/2-2,w:lw+4,h:lh+4};return rects.concat(placed).some(function(q){return L.x<q.x+q.w&&L.x+L.w>q.x&&L.y<q.y+q.h&&L.y+L.h>q.y})}
          var best=null;[0,12,-12,24,-24,36,-36,48,-48,60,-60].some(function(o){var x=Math.max(lw/2+4,Math.min(box.width-lw/2-4,mx+nx*o)),y=my+ny*o;if(y<lh/2+2||y>box.height-lh/2-2)return false;if(!hit(x,y)){best=[x,y];return true}});
          if(!best){l.remove();return}
          l.style.left=best[0]+'px';l.style.top=best[1]+'px';placed.push({x:best[0]-lw/2,y:best[1]-lh/2,w:lw,h:lh});labels=placed;
        }
      });
    });
  }
  drawTangles();
  window.addEventListener('resize',function(){clearTimeout(window.__tg);window.__tg=setTimeout(drawTangles,120)});
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(drawTangles);

  // deepin.risk demo interactions
  document.querySelectorAll('[data-tabs]').forEach(function(box){
    var tabs=[].slice.call(box.querySelectorAll('[role="tab"]'));if(!tabs.length)return;
    function sel(t,focus){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;document.getElementById(x.getAttribute('aria-controls')).hidden=!on});if(focus)t.focus()}
    box.classList.add('tabbed');sel(tabs[0]);
    tabs.forEach(function(t,i){
      t.addEventListener('click',function(){sel(t)});
      t.addEventListener('keydown',function(ev){var k=ev.key==='ArrowRight'?1:ev.key==='ArrowLeft'?-1:0;if(k){ev.preventDefault();sel(tabs[(i+k+tabs.length)%tabs.length],true)}});
    });
  });
  document.querySelectorAll('.liv-tl').forEach(function(tl){
    var btns=[].slice.call(tl.querySelectorAll('.lt-btn')),panels=[].slice.call(tl.querySelectorAll('.lt-panel'));
    btns.forEach(function(b){b.addEventListener('click',function(){
      var i=b.getAttribute('data-ev');
      btns.forEach(function(x){var on=x===b;x.classList.toggle('sel',on);x.setAttribute('aria-pressed',on?'true':'false')});
      panels.forEach(function(p){p.hidden=p.getAttribute('data-panel')!==i});
    })});
  });
  document.querySelectorAll('.rgraph').forEach(function(g){
    var info=g.querySelector('.rg-info'),nodes=[].slice.call(g.querySelectorAll('.gn'));
    function pick(n){nodes.forEach(function(x){x.classList.toggle('sel',x===n)});info.textContent=n.getAttribute('aria-label')+': '+n.getAttribute('data-info')}
    nodes.forEach(function(n){
      n.addEventListener('click',function(){pick(n)});
      n.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();pick(n)}});
    });
  });
  document.querySelectorAll('details.ev-d').forEach(function(d){
    var s=d.querySelector('summary');
    d.addEventListener('toggle',function(){s.textContent=d.open?s.getAttribute('data-hide'):s.getAttribute('data-view')});
  });
  document.querySelectorAll('[data-ev-all]').forEach(function(b){
    var list=b.parentNode.querySelector('.why3s');if(!list)return;
    list.classList.add('closed');b.hidden=false;
    b.addEventListener('click',function(){var c=list.classList.toggle('closed');b.textContent=b.getAttribute(c?'data-show':'data-hide')});
  });
  document.querySelectorAll('[data-decision]').forEach(function(box){
    var res=box.querySelector('.rcx-result'),steps=[].slice.call(box.querySelectorAll('.rcx-further li'));
    box.querySelectorAll('[data-act]').forEach(function(b){b.addEventListener('click',function(){
      var a=b.getAttribute('data-act');
      if(a==='further'){
        b.disabled=true;res.hidden=true;
        steps.forEach(function(li,i){setTimeout(function(){li.hidden=false;li.classList.add('in')},still?0:i*700)});
      }else{res.textContent=b.getAttribute('data-msg');res.hidden=false;res.className='rcx-result '+a}
    })});
  });
  // request form as a sheet on small screens
  (function(){
    var sheet=document.getElementById('request-sheet');if(!sheet)return;
    var mq=window.matchMedia('(max-width:760px)');
    function open(){sheet.classList.add('open');document.documentElement.classList.add('noscroll');setTimeout(function(){var i=document.getElementById('rq-company');if(i)i.focus()},60)}
    function close(){sheet.classList.remove('open');document.documentElement.classList.remove('noscroll')}
    document.querySelectorAll('a[href="#request"],[data-open-request]').forEach(function(a){a.addEventListener('click',function(ev){if(mq.matches){ev.preventDefault();open()}})});
    sheet.querySelector('[data-close]').addEventListener('click',close);
    document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&sheet.classList.contains('open'))close()});
  })();

  // request form: two steps, then email (or POST to data-endpoint when configured)
  document.querySelectorAll('form.rq').forEach(function(f){
    var pages=[].slice.call(f.querySelectorAll('.rq-page')),dots=[].slice.call(f.querySelectorAll('.rq-steps li'));
    function show(n){pages.forEach(function(p,i){p.hidden=i!==n});dots.forEach(function(d,i){d.className=i===n?'on':''})}
    function valid(p){var ok=true;p.querySelectorAll('[required]').forEach(function(i){var bad=!i.value.trim()||(i.type==='email'&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(i.value));i.setAttribute('aria-invalid',bad?'true':'false');if(bad&&ok){i.focus();ok=false}});return ok}
    show(0);
    f.querySelector('[data-next]').addEventListener('click',function(){if(valid(pages[0])){show(1);pages[1].querySelector('input').focus()}});
    f.querySelector('[data-back]').addEventListener('click',function(){show(0)});
    f.addEventListener('submit',function(ev){
      ev.preventDefault();if(!valid(pages[1]))return;
      var data={};new FormData(f).forEach(function(v,k){data[k]=v});
      var done=f.querySelector('.rq-done'),ep=f.getAttribute('data-endpoint');
      if(ep){fetch(ep,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).catch(function(){})}
      else{
        var lines=[].slice.call(f.querySelectorAll('label')).map(function(l){var i=l.querySelector('input,textarea');return l.querySelector('span').textContent.replace('*','').trim()+': '+(i.value||'-')});
        location.href='mailto:info@deepin.space?subject='+encodeURIComponent(f.getAttribute('data-subject')+': '+(data.company||''))+'&body='+encodeURIComponent(lines.join('\n'));
      }
      pages.forEach(function(p){p.hidden=true});done.hidden=false;
    });
  });
  document.querySelectorAll('a[href="#request"]').forEach(function(a){a.addEventListener('click',function(){setTimeout(function(){var i=document.getElementById('rq-company');if(i)i.focus({preventScroll:true})},450)})});

  // evidence UI: link each reason to its source
  document.querySelectorAll('.evui').forEach(function(ui){
    var items=[].slice.call(ui.querySelectorAll('[data-ref]'));
    function lit(r){items.forEach(function(x){x.classList.toggle('lit',r!==null&&x.getAttribute('data-ref')===r)})}
    items.forEach(function(x){
      x.addEventListener('mouseenter',function(){lit(x.getAttribute('data-ref'))});
      x.addEventListener('mouseleave',function(){lit(null)});
    });
  });

  // connectors between [data-n] nodes of a [data-links] figure (edge: [from,to,kind]).
  // A figure whose CSS sets --links:0 (stacked mobile layouts) gets no lines.
  function drawLinks(){
    document.querySelectorAll('[data-links]').forEach(function(w){
      var svg=w.querySelector(':scope>svg.links');
      if(!svg){svg=el('svg',{'class':'links','aria-hidden':'true'});w.insertBefore(svg,w.firstChild)}
      while(svg.firstChild)svg.removeChild(svg.firstChild);
      if(getComputedStyle(w).getPropertyValue('--links').trim()==='0'){svg.style.display='none';return}
      svg.style.display='';
      var edges=[];try{edges=JSON.parse(w.getAttribute('data-links')||'[]')}catch(e){}
      var box=w.getBoundingClientRect();
      svg.setAttribute('width',box.width);svg.setAttribute('height',box.height);
      function r(id){var n=w.querySelector('[data-n="'+id+'"]');if(!n)return null;var b=n.getBoundingClientRect();
        return{l:b.left-box.left,r:b.right-box.left,t:b.top-box.top,b:b.bottom-box.top,cx:(b.left+b.right)/2-box.left,cy:(b.top+b.bottom)/2-box.top}}
      edges.forEach(function(ed){
        var A=r(ed[0]),B=r(ed[1]),k=ed[2]||'',d,g=3;if(!A||!B)return;
        var hz=w.getAttribute('data-links-dir')==='h'&&(B.l>=A.r-2||A.l>=B.r-2);
        if(hz&&B.l>=A.r-2){var x1=A.r+g,x2=B.l-g,m=(x2-x1)/2;d='M'+x1+' '+A.cy+' C'+(x1+m)+' '+A.cy+' '+(x2-m)+' '+B.cy+' '+x2+' '+B.cy}
        else if(hz){var x1=A.l-g,x2=B.r+g,m=(x1-x2)/2;d='M'+x1+' '+A.cy+' C'+(x1-m)+' '+A.cy+' '+(x2+m)+' '+B.cy+' '+x2+' '+B.cy}
        else if(B.t>=A.b-2){var y1=A.b+g,y2=B.t-g,m=(y2-y1)/2;d='M'+A.cx+' '+y1+' C'+A.cx+' '+(y1+m)+' '+B.cx+' '+(y2-m)+' '+B.cx+' '+y2}
        else if(A.t>=B.b-2){var y1=A.t-g,y2=B.b+g,m=(y1-y2)/2;d='M'+A.cx+' '+y1+' C'+A.cx+' '+(y1-m)+' '+B.cx+' '+(y2+m)+' '+B.cx+' '+y2}
        else if(B.l>=A.r-2){var x1=A.r+g,x2=B.l-g,m=(x2-x1)/2;d='M'+x1+' '+A.cy+' C'+(x1+m)+' '+A.cy+' '+(x2-m)+' '+B.cy+' '+x2+' '+B.cy}
        else{var x1=A.l-g,x2=B.r+g,m=(x1-x2)/2;d='M'+x1+' '+A.cy+' C'+(x1-m)+' '+A.cy+' '+(x2+m)+' '+B.cy+' '+x2+' '+B.cy}
        var p=el('path',{d:d,'class':k});
        if(k!=='nd')p.setAttribute('marker-end','url(#'+(k==='w'||k==='d'?'lk-w':'lk-a')+')');
        svg.appendChild(p);
      });
    });
  }
  if(document.querySelector('[data-links]')){
    drawLinks();
    window.addEventListener('resize',function(){clearTimeout(window.__lk);window.__lk=setTimeout(drawLinks,120)});
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(drawLinks);
    window.addEventListener('load',drawLinks);
  }

  // governance gate: pick an example request, see which checks pass and the outcome
  document.querySelectorAll('[data-gate]').forEach(function(g){
    var btns=[].slice.call(g.querySelectorAll('.gt-btn')),checks=[].slice.call(g.querySelectorAll('.gt-checks li')),
        outs=[].slice.call(g.querySelectorAll('.gt-o')),label=g.querySelector('[data-gate-label]'),why=g.querySelector('[data-gate-why]');
    btns.forEach(function(b){b.addEventListener('click',function(){
      var res=JSON.parse(b.getAttribute('data-res')),out=+b.getAttribute('data-out');
      btns.forEach(function(x){var on=x===b;x.classList.toggle('sel',on);x.setAttribute('aria-pressed',on?'true':'false')});
      checks.forEach(function(li,i){li.setAttribute('data-state',res[i])});
      outs.forEach(function(o,i){o.classList.toggle('on',i===out)});
      label.textContent=b.textContent;why.textContent=b.getAttribute('data-why');
    })});
  });

  // execution trace: select a step to inspect its record
  document.querySelectorAll('[data-trace]').forEach(function(t){
    var rows=[].slice.call(t.querySelectorAll('[data-tr]')),panels=[].slice.call(t.querySelectorAll('[data-trp]'));
    rows.forEach(function(b){b.addEventListener('click',function(){
      var i=b.getAttribute('data-tr');
      rows.forEach(function(x){var on=x===b;x.classList.toggle('sel',on);x.setAttribute('aria-pressed',on?'true':'false')});
      panels.forEach(function(p){p.hidden=p.getAttribute('data-trp')!==i});
    })});
  });

  // dotted wave field, echoing the brand's hero texture
  var c=document.getElementById('field');if(!c||!c.getContext)return;
  var ctx=c.getContext('2d'),w,h,dpr,t=0,raf;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function rgb(){return getComputedStyle(document.documentElement).getPropertyValue('--dot').trim()||'21,136,103'}
  var col=rgb();
  function size(){dpr=Math.min(window.devicePixelRatio||1,2);w=c.clientWidth;h=c.clientHeight;c.width=w*dpr;c.height=h*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)}
  function draw(){
    ctx.clearRect(0,0,w,h);
    var rows=34,cols=Math.round(w/9);
    for(var r=0;r<rows;r++){
      var z=r/(rows-1);                    // 0 far, 1 near
      var p=0.35+z*0.65;                   // perspective
      var baseY=h*0.12+Math.pow(z,1.35)*h*0.95;
      for(var i=0;i<cols;i++){
        var u=i/(cols-1);
        var x=(u-0.5)*w*(0.9+p*0.6)+w/2;
        var y=baseY
          +Math.sin(u*6.2+z*2.4+t)*14*p
          +Math.sin(u*2.1-z*3.3+t*0.6)*22*p;
        var a=(0.08+0.55*z)*(0.25+0.75*u);
        ctx.fillStyle='rgba('+col+','+a.toFixed(3)+')';
        var s=0.6+p*1.1;
        ctx.fillRect(x,y,s,s);
      }
    }
  }
  function loop(){t+=0.006;draw();raf=requestAnimationFrame(loop)}
  size();draw();
  window.addEventListener('resize',function(){size();draw()});
  if(window.matchMedia){matchMedia('(prefers-color-scheme: dark)').addEventListener('change',function(){col=rgb();draw()})}
  new MutationObserver(function(){col=rgb();draw()}).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  if(!reduce){
    var io=new IntersectionObserver(function(e){if(e[0].isIntersecting){if(!raf)loop()}else{cancelAnimationFrame(raf);raf=null}});
    io.observe(c);
  }
})();
