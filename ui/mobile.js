(()=>{const b=document.createElement('button');b.className='burger';b.setAttribute('aria-label','Меню');b.innerHTML='<span></span><span></span><span></span>';const s=document.createElement('div');s.className='scrim';document.body.append(b,s);
const tg=()=>document.body.classList.toggle('menu-open');b.onclick=tg;s.onclick=tg;
document.addEventListener('click',e=>{if(e.target.closest('.psb a'))document.body.classList.remove('menu-open')});})();
