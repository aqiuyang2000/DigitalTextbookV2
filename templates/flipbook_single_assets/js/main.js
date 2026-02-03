// FILE: main.js
// 功能: (单页翻书模式) JS主入口文件。
//       负责导入所有功能模块并按顺序初始化。

'use strict';

// 1. 导入所有功能模块
import { APP_CONFIG, initConfig } from './modules/config.js';
import { initFlipbook } from './modules/flipbook.js';
import { initSidebar } from './modules/sidebar.js';
import { initNavigation } from './modules/navigation.js';

// 2. 使用 jQuery 的 document ready 确保 DOM 已加载完毕
$(function() {
    
    // 3. 首先，初始化配置模块，让它从 window 对象中读取数据
    initConfig();

    // 4. 注入全局弹窗JS (如果存在)
    if (APP_CONFIG.jsPopups) {
        $('body').append(`<script>${APP_CONFIG.jsPopups}<\/script>`);
    }
    
    // 5. 按顺序初始化所有UI模块
    
    // a. 初始化核心的翻书功能
    initFlipbook();
    
    // b. 初始化侧边栏交互
    initSidebar();

    // c. 初始化页面导航功能（翻页按钮 + 键盘控制）
    initNavigation();
    
    console.log("Single-page flipbook application initialized successfully.");
});