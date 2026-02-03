// FILE: templates/flipbook_modular_assets/js/modules/zoom.js
// 功能: 封装所有与画册缩放和平移相关的交互逻辑。

'use strict';

// 模块内的私有变量，用于存储状态
let scale = 1.0;
const minScale = 1.0;
const maxScale = 4.0;
let pan = { x: 0, y: 0 };
let isPanning = false;
let panStart = { x: 0, y: 0 };

const $flipbook = $("#flipbook");
const $container = $("#viewer-container");

/**
 * 应用当前的 scale 和 pan 变换到 #flipbook 元素。
 * 同时根据缩放状态禁用或启用翻页功能。
 */
function applyTransform() {
    if (scale <= minScale) {
        // 重置到最小缩放级别
        scale = minScale;
        pan.x = 0;
        pan.y = 0;
        $flipbook.removeClass('zoomable');
        if ($flipbook.turn('is')) {
            $flipbook.turn('disable', false); // 重新启用翻页
        }
    } else {
        // 进入缩放状态
        $flipbook.addClass('zoomable');
        if ($flipbook.turn('is')) {
            $flipbook.turn('disable', true); // 禁用翻页
        }
    }
    $flipbook.css('transform', `translate(${pan.x}px, ${pan.y}px) scale(${scale})`);
}

/**
 * (Exported) 重置缩放和平移状态到初始值。
 * 这个函数被 sidebar.js 模块导入和调用。
 */
export function resetZoomAndPan() {
    if (scale > minScale) {
        scale = minScale;
        pan = { x: 0, y: 0 };
        applyTransform();
    }
}

/**
 * 初始化缩放和平移的所有事件监听器。
 */
export function initZoomAndPan() {

    // 1. 鼠标滚轮事件 (用于缩放)
    $container.on('wheel', function(event) {
        // 只在 flipbook 区域内滚动才触发缩放
        if ($(event.target).closest('#flipbook').length === 0) return;
        
        event.preventDefault();
        const delta = event.originalEvent.deltaY;
        const zoomFactor = 1.1;
        
        if (delta < 0) { // 向上滚动 = 放大
            scale *= zoomFactor;
        } else { // 向下滚动 = 缩小
            scale /= zoomFactor;
        }

        // 限制缩放范围
        scale = Math.max(minScale, Math.min(maxScale, scale));
        
        applyTransform();
    });

    // 2. 鼠标按下事件 (用于开始平移)
    $flipbook.on('mousedown', function(event) {
        // 只有在已缩放的状态下才允许平移
        if (scale > minScale) {
            event.preventDefault();
            isPanning = true;
            panStart.x = event.pageX - pan.x;
            panStart.y = event.pageY - pan.y;
            $flipbook.addClass('dragging');
        }
    });

    // 3. 鼠标移动和松开事件 (在 window 上监听，以确保在容器外拖动也能响应)
    $(window).on('mousemove', function(event) {
        if (isPanning) {
            pan.x = event.pageX - panStart.x;
            pan.y = event.pageY - panStart.y;
            applyTransform();
        }
    }).on('mouseup', function() {
        if (isPanning) {
            isPanning = false;
            $flipbook.removeClass('dragging');
        }
    });
}