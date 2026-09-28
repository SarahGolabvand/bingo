document.addEventListener('alpine:init', () => {
 Alpine.data('menuCart', () => ({
  items:[], catalog:[], active:null, drawer:false, category:'all', milk:'regular', shot:false, sweetness:'normal', quantity:1, syncError:false,
  init() {
   this.catalog=JSON.parse(document.getElementById('menu-data').textContent);
   try { const saved=JSON.parse(sessionStorage.getItem('dingo:demo:cart') || '[]');
    this.items=Array.isArray(saved)?saved.filter(r=>this.catalog.some(p=>p.id===r.id)&&Number.isInteger(r.quantity)&&r.quantity>0&&r.quantity<=20&&['regular','oat'].includes(r.milk)&&typeof r.shot==='boolean'&&['none','normal','extra'].includes(r.sweetness)):[];
   } catch (_) { this.items=[]; }
   this.$watch('items',()=>{ try {sessionStorage.setItem('dingo:demo:cart',JSON.stringify(this.items));} catch(_){} });
  },
  get count(){return this.items.reduce((s,r)=>s+r.quantity,0)},
  get unit(){return (this.active?.price || 0)+(this.milk==='oat'?80:0)+(this.shot?100:0)},
  money(cents){return new Intl.NumberFormat(document.documentElement.lang,{style:'currency',currency:'USD'}).format(cents/100)},
  name(row){return this.catalog.find(p=>p.id===row.id)?.name || ''},
  rowPrice(row){return ((this.catalog.find(p=>p.id===row.id)?.price||0)+(row.milk==='oat'?80:0)+(row.shot?100:0))*row.quantity},
  get total(){return this.items.reduce((s,r)=>s+this.rowPrice(r),0)},
  choose(id){this.active=this.catalog.find(p=>p.id===id);this.milk='regular';this.shot=false;this.sweetness='normal';this.quantity=1},
  add(){if(!this.active)return;const key=[this.active.id,this.milk,this.shot,this.sweetness].join(':');const existing=this.items.find(r=>r.key===key);if(existing)existing.quantity=Math.min(20,existing.quantity+Number(this.quantity));else if(this.items.length<50)this.items.push({key,id:this.active.id,milk:this.milk,shot:this.shot,sweetness:this.sweetness,quantity:Number(this.quantity)});this.active=null},
  change(key,delta){this.items=this.items.map(r=>r.key===key?{...r,quantity:Math.min(20,r.quantity+delta)}:r).filter(r=>r.quantity>0);this.sync()},
  openCart(){this.drawer=true;this.sync()},
  sync(){this.syncError=false;this.$nextTick(()=>htmx.trigger(document.getElementById('cart-sync'),'cart-sync'))}
 }));
});
