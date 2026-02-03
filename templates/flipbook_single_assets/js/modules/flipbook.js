// FILE: flipbook.js
// 功能: (单页翻书模式) 封装所有与 turn.js 库相关的核心逻辑。

'use strict';

// 1. 导入配置和 jQuery 实例
import { APP_CONFIG } from './config.js';

// 将 jQuery 实例缓存在模块作用域内
const $flipbook = $('#flipbook');
const $window = $(window);
const $container = $('#viewer-container');

/**
 * 更新当前可视页面上的所有热区的位置和大小。
 * 热区的位置是根据其父容器的实时尺寸和 data-* 属性中的百分比计算的。
 */
function updateHotspots() {
    const view = $flipbook.turn('view');
    if (!view || view.length === 0) return;

    view.forEach(pageNumber => {
        if (pageNumber === 0) return;

        const pageElement = $flipbook.find(`.turn-page[page_num='${pageNumber}']`);
        if (!pageElement.length) return;

        const container = pageElement[0];
        if (!container || container.offsetWidth === 0) return;
        
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;

        pageElement.find('.hotspot').each(function() {
            const $hotspot = $(this);
            const relX = parseFloat($hotspot.data('relX')),
                  relY = parseFloat($hotspot.data('relY')),
                  relW = parseFloat($hotspot.data('relW')),
                  relH = parseFloat($hotspot.data('relH'));

            $hotspot.css({
                left: (containerWidth * relX / 100) + 'px',
                top: (containerHeight * relY / 100) + 'px',
                width: (containerWidth * relW / 100) + 'px',
                height: (containerHeight * relH / 100) + 'px'
            });
        });
    });
}

/**
 * 根据容器尺寸计算翻书组件的最佳尺寸。
 */
function calculateBookSize() {
    const isMobile = $window.width() <= 992;
    const containerWidth = $container.width();
    const containerHeight = $container.height();
    let newWidth, newHeight;
    const firstPage = APP_CONFIG.pagesData[0];
    if (!firstPage) return { width: 0, height: 0 };
    const aspectRatio = firstPage.width / firstPage.height;

    if (isMobile) {
        newWidth = containerWidth;
        newHeight = newWidth / aspectRatio;
    } else {
        newHeight = containerHeight * 0.9;
        newWidth = newHeight * aspectRatio;
        if (newWidth > containerWidth * 0.95) {
           newWidth = containerWidth * 0.95;
           newHeight = newWidth / aspectRatio;
        }
    }
    return { width: Math.floor(newWidth), height: Math.floor(newHeight) };
}

/**
 * 创建 turn.js 实例并绑定事件。
 * @param {object} size - 包含 width 和 height 的对象。
 */
function createTurnJsInstance(size) {
    $flipbook.turn({
        width: size.width,
        height: size.height,
        display: 'single',
        elevation: 50,
        autoCenter: true,
        acceleration: true,
        gradients: Modernizr.cssgradients,
        turnCorners: 'bl,br',
        when: {
            turned: function(event, page, view) {
                setTimeout(updateHotspots, 10); // 翻页后更新热区
            }
        }
    });
}

/**
 * 异步加载所有页面片段并初始化翻书组件。
 */
async function loadPagesAndInit() {
    const { pagesData } = APP_CONFIG;
    if (!pagesData || pagesData.length === 0) {
         $container.html('<p style="text-align:center;">没有可显示的页面。</p>');
         return;
    }
    try {
        const fetchPromises = pagesData.map(pageData =>
            fetch(pageData.url).then(response => {
                if (!response.ok) return `<div class="turn-page missing-page"><div class="error-content"><p>页面加载失败</p></div></div>`;
                return response.text();
            }).catch(error => `<div class="turn-page missing-page"><div class="error-content"><p>网络错误</p></div></div>`)
        );
        const htmlFragments = await Promise.all(fetchPromises);
        $flipbook.html(htmlFragments.join(''));

        const imageLoadPromises = [];
        $flipbook.find('.turn-page:not(.missing-page)').each(function() {
            const bgImage = $(this).css('background-image');
            if (bgImage && bgImage !== 'none') {
                const match = bgImage.match(/url\((['"]?)(.*?)\1\)/);
                const imgUrl = match ? match[2] : null;
                if (imgUrl) {
                    imageLoadPromises.push(new Promise((resolve) => {
                        const img = new Image();
                        img.onload = resolve;
                        img.onerror = resolve;
                        img.src = imgUrl;
                    }));
                }
            }
        });
        await Promise.all(imageLoadPromises);

        const initialSize = calculateBookSize();
        $flipbook.width(initialSize.width).height(initialSize.height);
        createTurnJsInstance(initialSize);
        updateHotspots(); // 初始加载时更新一次热区

    } catch (error) {
        console.error('加载页面或初始化时发生严重错误:', error);
        $container.html('<p style="text-align:center; color:red;">初始化失败，请检查浏览器控制台。</p>');
    }
}

/**
 * 初始化翻书功能，包括窗口大小调整的事件监听。
 */
export function initFlipbook() {
    loadPagesAndInit();
    
    let resizeTimer;
    $window.on('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            if ($flipbook.data() && $flipbook.data().turn) {
                const size = calculateBookSize();
                $flipbook.turn('size', size.width, size.height);
                setTimeout(updateHotspots, 10); // 尺寸调整后也更新热区
            }
        }, 200);
    });
}