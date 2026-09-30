
/* DEEPIN / ORGANISM — homepage motion. Every movement answers a product question:
   an event arrives, the Investigation organizes, evidence emerges, a person decides,
   and the organization underneath becomes visible. Reduced motion: the same states,
   switched by the step buttons, without movement. */
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NSV='http://www.w3.org/2000/svg';
  function sm(p,a,b){var t=Math.min(1,Math.max(0,(p-a)/(b-a)));return t*t*(3-2*t)}
  function lerp(a,b,t){return a+(b-a)*t}
  var navH=function(){var n=document.querySelector('.nav');return n?n.offsetHeight:64};

  /* ---------------------------------------------------------------- the Investigation scene */
  var scene=document.querySelector('[data-scene]');
  if(scene){
    var stage=scene.querySelector('.stage'),svg=stage.querySelector('.stage-lines');
    var phs=[].slice.call(scene.querySelectorAll('.ph')),steps=[].slice.call(scene.querySelectorAll('[data-step]'));
    var nodes={};[].slice.call(stage.querySelectorAll('[data-node]')).forEach(function(n){nodes[n.getAttribute('data-node')]=n});
    var notes=[].slice.call(stage.querySelectorAll('.st-tn'));
    var tangle=JSON.parse(stage.getAttribute('data-tangle')||'[]');
    var srcIds=['reg1','reg2','graph','pdf','crm','mail','sheet','web'];
    var rel={reg1:'E1',reg2:'E2',graph:'E3'};
    // [x,y,rotation] in % of the stage: scattered (today) and organized (with Deepin)
    var L={
      wide:{
        chaos:{co:[50,50,0],reg1:[24,17,-5],reg2:[69,77,4],graph:[84,51,5],pdf:[70,19,3],crm:[16,45,-4],mail:[27,79,5],sheet:[49,90,-2],web:[88,25,-6]},
        order:{co:[50,7,0],reg1:[14,20,0],reg2:[14,30,0],graph:[14,40,0],pdf:[14,51,0],crm:[14,60,0],mail:[14,69,0],sheet:[14,78,0],web:[14,87,0]},
        ev:{E1:[47,25],E2:[47,46],E3:[47,67]},find:[80.5,40],dec:[80.5,77],vertical:false
      },
      tall:{
        chaos:{co:[50,48,0],reg1:[27,13,-5],reg2:[72,83,4],graph:[74,29,5],pdf:[27,31,3],crm:[25,66,-4],mail:[71,64,5],sheet:[30,89,-2],web:[73,11,-6]},
        order:{co:[50,4.5,0],reg1:[26,12,0],reg2:[74,12,0],graph:[26,20,0],pdf:[74,20,0],crm:[26,28,0],mail:[74,28,0],sheet:[26,36,0],web:[74,36,0]},
        ev:{E1:[50,47],E2:[50,57],E3:[50,67]},find:[50,66],dec:[50,89],vertical:true
      }
    };
    var P=reduce?1:0,layout=null,W=0,H=0;
    function pick(){layout=stage.clientWidth<560?L.tall:L.wide;W=stage.clientWidth;H=stage.clientHeight;svg.setAttribute('viewBox','0 0 '+W+' '+H)}
    function place(n,x,y,r,o,s){n.style.setProperty('--x',x.toFixed(2));n.style.setProperty('--y',y.toFixed(2));n.style.setProperty('--r',(r||0).toFixed(2));n.style.setProperty('--o',o.toFixed(3));n.style.setProperty('--s',(s||1).toFixed(3))}
    function box(id){var n=nodes[id];if(!n)return null;var x=parseFloat(n.style.getPropertyValue('--x'))/100*W,y=parseFloat(n.style.getPropertyValue('--y'))/100*H;return{x:x,y:y,w:n.offsetWidth,h:n.offsetHeight}}
    function path(d,cls,o){var p=document.createElementNS(NSV,'path');p.setAttribute('d',d);p.setAttribute('class',cls);p.style.opacity=o;svg.appendChild(p)}
    function curve(a,b,bend){var mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2,dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy)||1,nx=-dy/l,ny=dx/l;
      return{d:'M'+a[0]+' '+a[1]+' Q'+(mx+nx*bend)+' '+(my+ny*bend)+' '+b[0]+' '+b[1],m:[mx+nx*bend/2,my+ny*bend/2]}}
    function render(){
      var p=P,org=sm(p,.14,.34),chaosO=1-sm(p,.1,.26),dim=sm(p,.86,.96);
      var ph=p<.14?0:p<.4?1:p<.6?2:p<.8?3:4;
      stage.classList.toggle('org',org>.5);stage.classList.toggle('ev',p>.4);stage.classList.toggle('dimmed',dim>0);
      stage.style.setProperty('--dim',dim.toFixed(3));
      phs.forEach(function(x,i){x.classList.toggle('on',i===ph)});
      steps.forEach(function(b,i){b.classList.toggle('on',i===ph);b.setAttribute('aria-pressed',i===ph?'true':'false')});
      var fo=sm(p,.6,.7),dO=sm(p,.8,.88),tall=layout.vertical,lift=tall?fo*18:0;
      ['co'].concat(srcIds).forEach(function(id){var a=layout.chaos[id],b=layout.order[id];place(nodes[id],lerp(a[0],b[0],org),lerp(a[1],b[1],org),lerp(a[2],b[2],org),tall?1-.85*fo:1)});
      var evO={};
      ['E1','E2','E3'].forEach(function(id,i){var o=sm(p,.4+.045*i,.5+.045*i),c=layout.ev[id];evO[id]=o;place(nodes[id],c[0],c[1]+(1-o)*3-lift,0,o,.94+.06*o)});
      place(nodes.find,layout.find[0],layout.find[1]+(1-fo)*3,0,fo,.95+.05*fo);
      place(nodes.dec,layout.dec[0],layout.dec[1]+(1-dO)*3,0,dO,(.95+.05*dO)*(1+dim*.06));
      // lines
      while(svg.firstChild)svg.removeChild(svg.firstChild);
      if(chaosO>.01){tangle.forEach(function(t,i){var A=box(t[0]),B=box(t[1]);if(!A||!B)return;var c=curve([A.x,A.y],[B.x,B.y],(i%2?1:-1)*Math.min(60,W*.06));path(c.d,'ch',chaosO*.9);
        notes.forEach(function(n){if(n.getAttribute('data-a')===t[0]&&n.getAttribute('data-b')===t[1]){n.style.left=c.m[0]+'px';n.style.top=c.m[1]+'px';n.style.setProperty('--o',chaosO.toFixed(3))}})})}
      else notes.forEach(function(n){n.style.setProperty('--o','0')});
      Object.keys(rel).forEach(function(s){var o=evO[rel[s]];if(o<.01)return;var A=box(s),B=box(rel[s]);
        if(layout.vertical){path('M'+A.x+' '+(A.y+A.h/2)+' C'+A.x+' '+(B.y-40)+' '+(B.x-B.w/2+20)+' '+(B.y-B.h/2-20)+' '+(B.x-B.w/2+20)+' '+(B.y-B.h/2),'or',o*(1-dim*.5))}
        else{var x1=A.x+A.w/2,x2=B.x-B.w/2,m=(x2-x1)/2;path('M'+x1+' '+A.y+' C'+(x1+m)+' '+A.y+' '+(x2-m)+' '+B.y+' '+x2+' '+B.y,'or',o*(1-dim*.5))}});
      if(fo>.01){['E1','E2','E3'].forEach(function(id){var A=box(id),B=box('find');
        if(layout.vertical){if(id!=='E3')return;path('M'+A.x+' '+(A.y+A.h/2)+' V'+(B.y-B.h/2),'or',fo)}
        else{var x1=A.x+A.w/2,x2=B.x-B.w/2,m=(x2-x1)/2;path('M'+x1+' '+A.y+' C'+(x1+m)+' '+A.y+' '+(x2-m)+' '+B.y+' '+x2+' '+B.y,'or',fo)}})}
      if(dO>.01){var A=box('find'),B=box('dec');path('M'+A.x+' '+(A.y+A.h/2)+' V'+(B.y-B.h/2),'hu',dO)}
    }
    var scrollMode=false;
    function measure(){
      pick();
      scrollMode=!reduce&&window.innerHeight>=520&&window.innerHeight<=1600;
      scene.classList.toggle('is-scroll',scrollMode);
      if(scrollMode){scene.style.setProperty('--len',window.innerWidth<860?5:5.2)}
      onScroll();
    }
    function onScroll(){
      if(scrollMode){var r=scene.getBoundingClientRect(),nh=navH(),span=scene.offsetHeight-window.innerHeight+nh;P=Math.min(1,Math.max(0,(nh-r.top)/span))}
      render();
    }
    var anchors=[.05,.3,.52,.72,.97];
    steps.forEach(function(b,i){b.addEventListener('click',function(){
      if(scrollMode){var top=scene.getBoundingClientRect().top+window.scrollY,span=scene.offsetHeight-window.innerHeight+navH();window.scrollTo({top:top-navH()+anchors[i]*span,behavior:'smooth'})}
      else{P=anchors[i];render()}
    })});
    scene.classList.add('js-on');
    var raf=null;window.addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(function(){raf=null;onScroll()})},{passive:true});
    window.addEventListener('resize',function(){clearTimeout(window.__sc);window.__sc=setTimeout(measure,120)});
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(render);
    measure();
  }

  /* ---------------------------------------------------------------- the decision */
  document.querySelectorAll('[data-dcard]').forEach(function(card){
    var cites=[].slice.call(card.querySelectorAll('[data-cite]')),slips=[].slice.call(card.querySelectorAll('[data-slip]'));
    function lit(id){cites.forEach(function(c){c.classList.toggle('lit',c.getAttribute('data-cite')===id)});slips.forEach(function(s){s.classList.toggle('lit',s.getAttribute('data-slip')===id)})}
    cites.concat(slips).forEach(function(x){var id=x.getAttribute('data-cite')||x.getAttribute('data-slip');
      x.addEventListener('mouseenter',function(){lit(id)});x.addEventListener('mouseleave',function(){lit(null)});
      x.addEventListener('click',function(){lit(id)})});
    var res=card.querySelector('.d-res'),more=[].slice.call(card.querySelectorAll('.d-next li')),btns=[].slice.call(card.querySelectorAll('[data-act]'));
    btns.forEach(function(b){b.addEventListener('click',function(){
      btns.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
      var a=b.getAttribute('data-act');
      if(a==='further'){res.hidden=true;more.forEach(function(li,i){li.hidden=true;setTimeout(function(){li.hidden=false},reduce?0:i*450)})}
      else{more.forEach(function(li){li.hidden=true});res.textContent=b.getAttribute('data-msg');res.className='d-res '+a;res.hidden=false}
    })});
  });

  /* ---------------------------------------------------------------- lifting the floor */
  var under=document.querySelector('[data-under]');
  if(under){
    var slab=under.querySelector('.slab'),topo=under.querySelector('.topo'),copy=under.querySelector('.under-copy'),uScroll=false;
    function uMeasure(){uScroll=!reduce&&window.innerWidth>860&&window.innerHeight>=600&&window.innerHeight<=1600;under.classList.toggle('is-scroll',uScroll);uUpdate()}
    function uUpdate(){
      var q=1;
      if(uScroll){var tr=under.querySelector('.under-track'),r=tr.getBoundingClientRect();q=Math.min(1,Math.max(0,-r.top/(tr.offsetHeight-window.innerHeight)))}
      else if(!reduce&&window.innerHeight<=1600){var r2=under.getBoundingClientRect();q=r2.top<window.innerHeight*.75?1:0}
      slab.style.setProperty('--lift',uScroll?sm(q,.06,.4).toFixed(3):1);
      copy.style.setProperty('--copy',uScroll?sm(q,.22,.46).toFixed(3):1);
      topo.style.setProperty('--draw',uScroll?sm(q,.3,.78).toFixed(3):(reduce?1:q));
      var rr=under.getBoundingClientRect(),lifted=!uScroll||sm(q,.06,.4)>.6;document.body.classList.toggle('on-dark',lifted&&rr.top<window.innerHeight/2&&rr.bottom>window.innerHeight/2);
    }
    under.classList.add('js-on');
    if(!reduce)topo.style.transition='none';
    var uraf=null;window.addEventListener('scroll',function(){if(!uraf)uraf=requestAnimationFrame(function(){uraf=null;uUpdate()})},{passive:true});
    window.addEventListener('resize',function(){clearTimeout(window.__un);window.__un=setTimeout(uMeasure,120)});
    uMeasure();
  }

  /* ---------------------------------------------------------------- the rail: where the signal is */
  var rail=[].slice.call(document.querySelectorAll('.rail a'));
  if(rail.length&&'IntersectionObserver' in window){
    var ids=rail.map(function(a){return a.getAttribute('data-rail')});
    var io=new IntersectionObserver(function(en){en.forEach(function(x){if(!x.isIntersecting)return;var k=ids.indexOf(x.target.id);
      rail.forEach(function(a,i){a.classList.toggle('on',i===k);a.classList.toggle('done',i<k)})})},{rootMargin:'-45% 0px -50% 0px'});
    ids.forEach(function(id){var s=document.getElementById(id);if(s)io.observe(s)});
  }
})();
