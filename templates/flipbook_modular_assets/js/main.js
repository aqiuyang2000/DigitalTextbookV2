// FILE: templates/flipbook_modular_assets/js/main.js
// 功能: (双页翻书模式) JS主入口文件。
//       负责导入所有功能模块并按顺序初始化。

'use strict';

// 1. 导入所有功能模块
import { initFlipbook } from './modules/flipbook.js';
import { hotspotManager } from './modules/hotspotManager.js';
import { initSidebar } from './modules/sidebar.js';
import { initZoomAndPan } from './modules/zoom.js';
import { initKeyboardControls } from './modules/keyboard.js';

// 2. 使用 jQuery 的 document ready 确保 DOM 已加载完毕
$(function() {
    
    // 3. 从全局配置对象中安全地获取数据
    const APP_CONFIG = window.APP_CONFIG || {};
    const { totalPages, hotspotsData, jsPopups } = APP_CONFIG;

    // 4. 注入弹窗JS (如果存在)
    if (jsPopups) {
        const popupScript = document.createElement('script');
        popupScript.textContent = jsPopups;
        document.body.appendChild(popupScript);
    }
    
    // 5. 按顺序初始化所有模块
    
    // a. 首先初始化热区管理器的数据
    hotspotManager.init(hotspotsData);
    
    // b. 然后初始化核心的翻书功能，它依赖 totalPages 和 hotspotManager
    initFlipbook(totalPages, hotspotManager);
    
    // c. 初始化侧边栏交互
    initSidebar();

    // d. 初始化缩放和平移功能
    initZoomAndPan();
    
    // e. 初始化键盘控制
    initKeyboardControls();

    console.log("Flipbook application initialized successfully.");
});