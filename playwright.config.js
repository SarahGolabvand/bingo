const {defineConfig}=require('@playwright/test');
module.exports=defineConfig({testDir:'./tests',use:{baseURL:'http://127.0.0.1:8000',headless:true,launchOptions:process.env.DINGO_BROWSER ? {executablePath:process.env.DINGO_BROWSER} : {}},workers:1});
