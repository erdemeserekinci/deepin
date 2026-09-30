
/* DEEPIN / ORGANISM — Harness. The same organization answers differently when a
   different event arrives: another role becomes responsible, other capabilities are
   in reach, other policies apply, and the organization ends in a new state. */
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS='http://www.w3.org/2000/svg';
  // navigation darkens while the dark hero is under it
  var dark=document.querySelector('[data-dark]');
  if(dark){var f=function(){var r=dark.getBoundingClientRect();document.body.classList.toggle('on-dark',r.bottom>70)};window.addEventListener('scroll',f,{passive:true});f()}

  document.querySelectorAll('[data-rl]').forEach(function(rl){
    var evs=JSON.parse(rl.getAttribute('data-rl')),graph=rl.querySelector('.rl-graph'),svg=rl.querySelector('.rl-lines');
    var btns=[].slice.call(rl.querySelectorAll('.rl-ev')),nodes={},panel=rl.querySelector('.rl-panel');
    [].slice.call(rl.querySelectorAll('[data-role]')).forEach(function(n){nodes[n.getAttribute('data-role')]=n});
    var cur=0,timer=null,touched=false,visible=false;
    function c(n){var g=graph.getBoundingClientRect(),b=n.getBoundingClientRect();return{x:b.left-g.left+b.width/2,y:b.top-g.top+b.height/2,w:b.width,h:b.height}}
    function add(d,cls){var p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('pathLength','1');p.setAttribute('class',cls+(reduce?'':' draw'));svg.appendChild(p)}
    function lines(ev){
      while(svg.firstChild)svg.removeChild(svg.firstChild);
      var W=graph.clientWidth;svg.setAttribute('viewBox','0 0 '+W+' '+graph.clientHeight);
      ev.edges.forEach(function(e){
        var A=c(nodes[e[0]]);
        if(e[1]==='edge'){var x2=W-2,y=A.y;add('M'+(A.x+A.w/2+4)+' '+y+' H'+(x2-10),'block');
          var q=document.createElementNS(NS,'path');q.setAttribute('d','M'+(x2-16)+' '+(y-6)+' l12 12 M'+(x2-4)+' '+(y-6)+' l-12 12');q.setAttribute('class','x');svg.appendChild(q);return}
        var B=c(nodes[e[1]]),mx=(A.x+B.x)/2,my=(A.y+B.y)/2,dx=B.x-A.x,dy=B.y-A.y,l=Math.hypot(dx,dy)||1,bend=e[2]==='col'?-40:24;
        add('M'+A.x+' '+A.y+' Q'+(mx-dy/l*bend)+' '+(my+dx/l*bend)+' '+B.x+' '+B.y,e[2]);
      });
    }
    function show(i,user){
      cur=i;var ev=evs[i],hit={};ev.edges.forEach(function(e){hit[e[1]]=1});
      btns.forEach(function(b,k){b.classList.toggle('on',k===i);b.setAttribute('aria-pressed',k===i?'true':'false')});
      Object.keys(nodes).forEach(function(k){var n=nodes[k];n.classList.toggle('on',k===ev.active);n.classList.toggle('hit',!!hit[k]);n.classList.toggle('dim',k!==ev.active&&!hit[k])});
      lines(ev);
      panel.classList.add('swap');
      setTimeout(function(){
        [].slice.call(panel.querySelectorAll('[data-a]')).forEach(function(d,k){d.textContent=ev.a[k]});
        panel.querySelector('[data-out]').textContent=ev.out;panel.querySelector('[data-state]').textContent=ev.state;
        panel.querySelector('[data-state-box]').className='rl-state '+ev.kind;panel.classList.remove('swap');
      },reduce?0:220);
      if(user){touched=true;clearTimeout(timer)}
      else schedule();
    }
    function schedule(){clearTimeout(timer);if(reduce||touched||!visible)return;timer=setTimeout(function(){show((cur+1)%evs.length)},6500)}
    btns.forEach(function(b,k){b.addEventListener('click',function(){show(k,true)})});
    new IntersectionObserver(function(en){visible=en[0].isIntersecting;if(visible)schedule();else clearTimeout(timer)},{threshold:.35}).observe(rl);
    window.addEventListener('resize',function(){clearTimeout(window.__rl);window.__rl=setTimeout(function(){lines(evs[cur])},150)});
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){show(cur)});else show(0);
  });
})();
