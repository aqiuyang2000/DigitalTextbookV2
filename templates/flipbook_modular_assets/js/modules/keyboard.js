// FILE: keyboard.js
// 功能: 封装键盘左右箭头翻页的逻辑。

'use strict';

/**
 * 初始化键盘控制功能。
 */
export function initKeyboardControls() {

    const $flipbook = $("#flipbook");

    // 在整个 document 上监听 keydown 事件
    $(document).on('keydown', function(e) {
        
        // 检查焦点是否在输入框或文本域内，如果是，则不进行翻页
        const activeElement = document.activeElement;
        if (activeElement && (activeElement.tagName.toUpperCase() === 'INPUT' || activeElement.tagName.toUpperCase() === 'TEXTAREA')) {
            return;
        }

        // 根据按键执行翻页
        switch (e.key) {
            case "ArrowLeft":
                if ($flipbook.turn('is')) {
                    $flipbook.turn('previous');
                }
                break;
            case "ArrowRight":
                if ($flipbook.turn('is')) {
                    $flipbook.turn('next');
                }
                break;
        }
    });
}