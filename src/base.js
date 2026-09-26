
(function(){
  // Outside the live domain (local file, preview), folder links need an explicit index.html
  if(!/(^|\.)deepin\.space$/.test(location.hostname)){
    document.querySelectorAll('a[href]').forEach(function(a){
      var h=a.getAttribute('href');
      if(h&&!/^([a-z]+:|#|\/)/i.test(h)&&/\/$/.test(h))a.setAttribute('href',h+'index.html');
    });
  }
  // sticky nav border
  var nav=document.querySelector('.nav');
  var onScroll=function(){nav.classList.toggle('scrolled',window.scrollY>8)};
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();

  // copy email
  var btn=document.getElementById('copyBtn'),em=document.getElementById('email');
  if(btn&&em)btn.addEventListener('click',function(){
    var done=function(){btn.textContent='Copied';setTimeout(function(){btn.textContent='Copy email'},1800)};
    var fallback=function(){var r=document.createRange();r.selectNodeContents(em);var s=getSelection();s.removeAllRanges();s.addRange(r);btn.textContent='Selected';};
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

  // deepin.risk demo interactions
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
