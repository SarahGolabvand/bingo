import QRCode from 'qrcode';
document.addEventListener('alpine:init',()=>{
 Alpine.data('qrPackage',()=>({
  count:6, codes:[], busy:false, error:false,
  async generate(){
   if(!Number.isInteger(this.count)||this.count<1||this.count>50)return;
   this.busy=true;this.error=false;
   try {const rows=[];for(let i=1;i<=this.count;i++){
    const url=new URL(this.$el.dataset.menuUrl,window.location.origin);url.searchParams.set('table',String(i));
    rows.push({table:i,url:url.href,image:await QRCode.toDataURL(url.href,{width:360,margin:4,errorCorrectionLevel:'M',color:{dark:'#0D191D',light:'#FFFFFF'}})});
   }this.codes=rows;}catch(_){this.error=true}finally{this.busy=false}
  }
 }));
});
