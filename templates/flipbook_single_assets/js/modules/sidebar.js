// FILE: sidebar.js
// 功能: (单页翻书模式) 封装所有与侧边栏相关的交互逻辑。
'use strict';
import { APP_CONFIG } from './config.js';
/**
初始化侧边栏功能。
*/
export function initSidebar() {
    const $body = $('body');
    const $window = $(window);
    const $container = $('#viewer-container');
    const $sidebarToggle = $('#sidebar-toggle');
    const $outlineNav = $('#outline-nav');
    const $outlineTitle = $('#outline-title');
    const $flipbook = $('#flipbook');
    // 获取配置的行为模式 ('auto_hide' 或 'fixed')
    const outlineBehavior = APP_CONFIG.outlineBehavior || 'auto_hide';
    // --- 修复 1: 添加反引号，修正模板字符串语法 ---
    const sidebarStateKey = `sidebarState__${APP_CONFIG.projectTitle ? APP_CONFIG.projectTitle.replace(/\s+/g, "_") : 'default_single'}`;

    /**
    设置侧边栏的折叠状态 (仅PC端)。
    @param {boolean} collapsed - 是否折叠。
    */
    function setSidebarCollapsed(collapsed) {
        if (collapsed) {
            $body.addClass('sidebar-collapsed');
        } else {
            $body.removeClass('sidebar-collapsed');
        }
        // 只有在非固定模式下才保存状态，固定模式总是展开
        if (outlineBehavior !== 'fixed') {
            localStorage.setItem(sidebarStateKey, collapsed ? 'collapsed' : 'expanded');
        }
        setTimeout(() => $window.trigger('resize'), 350);
    }

    /**
    恢复侧边栏状态。
    */
    function restoreSidebarState() {
        // 如果是固定显示模式，强制展开，忽略本地存储
        if (outlineBehavior === 'fixed') {
            setSidebarCollapsed(false);
            return;
        }
        if (localStorage.getItem(sidebarStateKey) === 'collapsed') {
            setSidebarCollapsed(true);
        } else if ($window.width() > 992) {
            setSidebarCollapsed(false);
        }
    }

    // --- 事件绑定 ---
    // --- 修复 2: 补全 $sidebarToggle 点击事件头部 ---
    // 1. 切换按钮点击 (PC端)
    $sidebarToggle.on('click', function() {
        setSidebarCollapsed(!$body.hasClass('sidebar-collapsed'));
    });

    // --- 修复 3: 修正变量名 ($body) 和逻辑 ---
    // 2. 点击主内容区自动折叠 (PC端)
    $container.on('click', () => {
        // 只有在"非固定"模式下，且侧边栏当前是展开状态时，点击内容区才自动折叠
        if (outlineBehavior !== 'fixed' && !$body.hasClass('sidebar-collapsed')) {
            setSidebarCollapsed(true);
        }
    });

    // --- 修复 4: 补全 $outlineTitle 点击事件头部 ---
    // 3. 目录标题点击 (移动端 "手风琴" 效果)
    $outlineTitle.on('click', function() {
        if ($window.width() <= 992) {
            $(this).toggleClass('active');
            $outlineNav.slideToggle(200);
        }
    });

    // 4. 目录链接点击 (通用)
    $outlineNav.on('click', 'a', function(e) {
        e.preventDefault();
        const href = $(this).attr('href');
        if (href && href.startsWith('#page/')) {
            const pageNum = parseInt(href.substring(6), 10);
            if (!isNaN(pageNum) && $flipbook.turn('hasPage', pageNum)) {
                $flipbook.turn('page', pageNum);
            }
        }
    });

    // --- 初始化 ---
    restoreSidebarState();
    // 如果是固定模式，确保移除折叠类
    if (outlineBehavior === 'fixed') {
        $body.removeClass('sidebar-collapsed');
    }
}