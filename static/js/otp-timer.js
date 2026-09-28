document.addEventListener('alpine:init',()=>{
 Alpine.data('otpTimer',()=>({
  digits:['','','',''], remaining:0, interval:null, deadline:0,
  init(){this.interval=setInterval(()=>{this.remaining=Math.max(0,Math.ceil((this.deadline-Date.now())/1000))},250)},
  destroy(){clearInterval(this.interval)},
  start(){this.deadline=Date.now()+60000;this.remaining=60},
  normalize(value){return value.replace(/[۰-۹]/g,d=>String('۰۱۲۳۴۵۶۷۸۹'.indexOf(d))).replace(/[٠-٩]/g,d=>String('٠١٢٣٤٥٦٧٨٩'.indexOf(d))).replace(/\D/g,'')},
  input(event,index){const v=this.normalize(event.target.value);if(v.length>1){this.fill(v,index);return}this.digits[index]=v;event.target.value=v;if(v&&index<3)this.$refs['digit'+(index+1)].focus()},
  fill(value,start=0){const v=this.normalize(value).slice(0,4-start);[...v].forEach((n,i)=>{this.digits[start+i]=n});this.$nextTick(()=>this.$refs['digit'+Math.min(3,start+v.length)].focus())},
  back(index){if(!this.digits[index]&&index>0)this.$refs['digit'+(index-1)].focus()}
 }));
});
