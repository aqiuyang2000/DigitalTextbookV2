// FILE: navigation.js
// 功能: (单页翻书模式) 封装所有页面导航逻辑，包括按钮和键盘控制。

'use strict';

/**
 * 初始化页面导航功能。
 */
export function initNavigation() {

    const $flipbook = $('#flipbook');

    // --- 事件绑定 ---

    // 1. 上一页按钮点击
    $('#prev-page').on('click', () => {
        if ($flipbook.turn('is')) {
            $flipbook.turn('previous');
        }
    });

    // 2. 下一页按钮点击
    $('#next-page').on('click', () => {
        if ($flipbook.turn('is')) {
            $flipbook.turn('next');
        }
    });
    
    // 3. 键盘左右箭头事件
    $(document).on('keydown', function(e){
        // 检查焦点是否在输入框内，如果是，则不响应
        const activeElement = document.activeElement;
        if (activeElement && (activeElement.tagName.toUpperCase() === 'INPUT' || activeElement.tagName.toUpperCase() === 'TEXTAREA')) {
            return;
        }

        if (!$flipbook.turn('is')) return;

        switch (e.key) {
            case "ArrowLeft":
                $flipbook.turn('previous');
                break;
            case "ArrowRight":
                $flipbook.turn('next');
                break;
        }
    });
}