import {mkdir,copyFile,cp} from 'node:fs/promises';
await mkdir('static/vendor',{recursive:true});
for(const [src,dst] of [['alpinejs/dist/cdn.min.js','alpine.js'],['@alpinejs/persist/dist/cdn.min.js','persist.js'],['@alpinejs/focus/dist/cdn.min.js','focus.js'],['htmx.org/dist/htmx.min.js','htmx.js']]) await copyFile('node_modules/'+src,'static/vendor/'+dst);
for(const font of ['inter','vazirmatn']) await cp('node_modules/@fontsource/'+font+'/files','static/vendor/'+font,{recursive:true});

const { build } = await import('esbuild');
await build({entryPoints:['static/js/qr.js'],outfile:'static/js/qr.bundle.js',bundle:true,minify:true});
