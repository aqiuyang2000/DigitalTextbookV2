// FILE: templates/flipbook_modular_assets/js/modules/sidebar.js
// 功能: (双页翻书模式) 封装所有与侧边栏相关的交互逻辑。
// 优化: 参照用户提供的独立逻辑，使用 stopPropagation + 标志位完美实现交互需求。

'use strict';

import { resetZoomAndPan } from './zoom.js';

/**
 * 初始化侧边栏功能。
 */
export function initSidebar() {

    const $body = $('body');
    const $sidebarToggle = $('#sidebar-toggle');
    const $sidebar = $('.sidebar'); // 获取侧边栏容器
    const $outlineNav = $('#outline-nav');
    const $flipbook = $("#flipbook");

    // 获取配置对象
    const APP_CONFIG = window.APP_CONFIG || {};
    const outlineBehavior = APP_CONFIG.outlineBehavior || 'auto_hide';

    // 状态键名
    const sidebarStateKey = `sidebarState__${APP_CONFIG.projectTitle ? APP_CONFIG.projectTitle.replace(/\s+/g, "_") : 'default_modular'}`;

    // --- 核心逻辑变量 1: 标志位 ---
    // 用来判断当前的翻页动作是否是由点击提纲触发的
    let isOutlineNavigating = false;

    /**
     * 设置侧边栏的折叠状态。
     */
    function setSidebarCollapsed(collapsed, animate) {
        if (outlineBehavior === 'fixed') return; // 固定模式下不允许改变状态

        const isCurrentlyCollapsed = $body.hasClass('sidebar-collapsed');
        if (collapsed === isCurrentlyCollapsed) return;

        if (collapsed) {
            $body.addClass('sidebar-collapsed');
        } else {
            $body.removeClass('sidebar-collapsed');
        }

        // 保存状态
        localStorage.setItem(sidebarStateKey, collapsed ? 'collapsed' : 'expanded');

        // 触发重绘
        if (animate) {
            setTimeout(() => {
                $(window).trigger('resize');
            }, 350);
        }
    }

    /**
     * 恢复侧边栏初始状态。
     */
    function restoreSidebarState() {
        if (outlineBehavior === 'fixed') {
            // 固定模式：强制移除折叠类
            $body.removeClass('sidebar-collapsed');
            return;
        }

        if (localStorage.getItem(sidebarStateKey) === 'collapsed') {
            $body.addClass('sidebar-collapsed');
        } else if ($(window).width() > 992) {
            $body.removeClass('sidebar-collapsed');
        } else {
            $body.addClass('sidebar-collapsed');
        }
    }

    // =========================================================
    // 事件绑定逻辑 (完全参照参考代码的逻辑移植)
    // =========================================================

    // 1. 切换按钮点击：阻止冒泡，切换状态
    $sidebarToggle.on('click', function(e) {
        e.stopPropagation(); // <--- 关键：防止触发 document 的关闭逻辑
        setSidebarCollapsed(!$body.hasClass('sidebar-collapsed'), true);
    });

    // 2. 侧边栏自身点击：阻止冒泡
    // 这样点击侧边栏空白处或滚动条时，不会触发关闭
    $sidebar.on('click', function(e) {
        e.stopPropagation(); // <--- 关键
    });

    // 3. 提纲链接点击逻辑
    $outlineNav.on('click', 'a', function(e) {
        e.preventDefault();
        e.stopPropagation(); // <--- 关键：防止触发 document 点击

        const page = $(this).data('page');
        if (page) {
            // 【关键步骤】设置标志位，告诉 start 事件“这是提纲触发的”
            isOutlineNavigating = true;

            resetZoomAndPan();
            $flipbook.turn('page', page);
        }
    });

    if (outlineBehavior !== 'fixed') {
        // 4. 监听 turn.js 的翻页开始事件
        $flipbook.bind("start", function(event, pageObject, corner) {
            // 逻辑参照参考代码：
            if (isOutlineNavigating) {
                // 如果是点击提纲触发的翻页，不要关闭侧边栏
                // 仅重置标志位，以便下次手动翻页时能正常关闭
                isOutlineNavigating = false;
            } else {
                // 否则（手动拖拽、点击箭头、键盘翻页），关闭侧边栏
                if (!$body.hasClass('sidebar-collapsed')) {
                    setSidebarCollapsed(true, true);
                }
            }
        });

        // 5. 全局文档点击 (处理点击页面内容、屏幕空白处)
        $(document).on('click', function() {
            // 只要代码运行到这里，说明点击事件没有被 $sidebar 或 $toggle 拦截(stopPropagation)
            // 这意味着用户点击了 页面内容、背景空白 等区域
            if (!$body.hasClass('sidebar-collapsed')) {
                setSidebarCollapsed(true, true);
            }
        });
    }

    // --- 初始化 ---
    restoreSidebarState();
}