(()=>{
  const home=document.querySelector('.vc-home');
  if(!home)return;
  document.body.classList.add('vc-cinematic-page');
  document.documentElement.classList.add('vc-js');
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  const reveals=[...document.querySelectorAll('.vc-reveal')];
  if(!reduce&&'IntersectionObserver'in window){
    const io=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('vc-in');io.unobserve(entry.target)}
    }),{threshold:.12,rootMargin:'0px 0px -6%'});
    reveals.forEach(el=>io.observe(el));
  }else reveals.forEach(el=>el.classList.add('vc-in'));

  const heroVisual=document.querySelector('.vc-hero-visual');
  if(heroVisual&&!reduce&&matchMedia('(pointer:fine)').matches){
    window.addEventListener('pointermove',e=>{
      const x=(e.clientX/innerWidth-.5)*10;
      const y=(e.clientY/innerHeight-.5)*7;
      heroVisual.style.transform=`scale(1.035) translate3d(${x}px,${y}px,0)`;
    },{passive:true});
  }

  const cards=[...document.querySelectorAll('.vc-project-card,.vc-cap-card,.vc-film')];
  if(!reduce&&matchMedia('(pointer:fine)').matches){
    cards.forEach(card=>{
      card.addEventListener('pointermove',e=>{
        const r=card.getBoundingClientRect();
        const x=(e.clientX-r.left)/r.width-.5;
        const y=(e.clientY-r.top)/r.height-.5;
        card.style.setProperty('--rx',`${-y*1.4}deg`);
        card.style.setProperty('--ry',`${x*1.4}deg`);
      });
      card.addEventListener('pointerleave',()=>{card.style.removeProperty('--rx');card.style.removeProperty('--ry')});
    });
  }

  const dialog=document.getElementById('vc-film-dialog');
  const video=dialog?.querySelector('video');
  const close=dialog?.querySelector('.vc-film-close');
  const closeFilm=()=>{if(!dialog||!video)return;video.pause();video.removeAttribute('src');video.load();dialog.close()};
  document.querySelectorAll('[data-film]').forEach(btn=>btn.addEventListener('click',()=>{
    if(!dialog||!video)return;
    video.src=btn.dataset.film;
    dialog.showModal();
    video.play().catch(()=>{});
  }));
  close?.addEventListener('click',closeFilm);
  dialog?.addEventListener('click',e=>{if(e.target===dialog)closeFilm()});

  document.querySelectorAll('[data-wa]').forEach(a=>{
    a.href='https://wa.me/16478324443?text='+encodeURIComponent('Hi VisionCraft Labs, I would like to discuss a project.');
  });
})();
