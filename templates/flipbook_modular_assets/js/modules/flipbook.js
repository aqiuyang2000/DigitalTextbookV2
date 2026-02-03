// FILE: flipbook.js (NEW SIMPLIFIED VERSION)
// 功能: 封装与 turn.js 相关的逻辑。在新架构下，它不再需要手动调用热区渲染。

'use strict';

/**
 * 初始化 turn.js 翻书组件。
 * @param {number} totalPages - 书本的总页数。
 * @param {object} hotspotManager - (不再直接使用，为保持接口兼容而传入)
 */
export function initFlipbook(totalPages, hotspotManager) {
    
    const $flipbook = $("#flipbook");
    const $container = $("#viewer-container");

    /**
     * 根据容器尺寸计算并更新翻书组件的尺寸。
     * @param {number} pageAspectRatio - 单页的宽高比 (height / width)。
     */
    function updateFlipbookSize(pageAspectRatio) {
        if (!$flipbook.turn('is')) return;

        const availableWidth = $container.width() * 0.95;
        const availableHeight = $container.height() * 0.95;
        
        let singlePageWidth, singlePageHeight;

        // 以宽度为基准计算
        let pageWidthByWidth = availableWidth / 2;
        let pageHeightByWidth = pageWidthByWidth * pageAspectRatio;

        // 如果计算出的高度超出可用高度，则以高度为基准重新计算
        if (pageHeightByWidth > availableHeight) {
            singlePageHeight = availableHeight;
            singlePageWidth = singlePageHeight / pageAspectRatio;
        } else {
            singlePageWidth = pageWidthByWidth;
            singlePageHeight = pageHeightByWidth;
        }
        
        $flipbook.turn('size', Math.floor(singlePageWidth * 2), Math.floor(singlePageHeight));
    }

    /**
     * 创建 turn.js 实例。
     * @param {number} aspectRatio - 单页的宽高比。
     */
    function createTurnJsInstance(aspectRatio) {
        $flipbook.turn({
            display: "double",
            autoCenter: true,
            pages: totalPages,
            elevation: 50,
            when: {
                // 当 turn.js 需要加载缺失的页面时触发
                missing: function (event, pages) {
                    for (let pageNum of pages) {
                        const $page = $('<div>', {'page': pageNum});
                        $flipbook.turn('addPage', $page, pageNum);
                        
                        // 只需加载HTML，无需后续处理
                        $.get(`pages/page-${pageNum}.html`).done(function(data) {
                            $page.html(data);
                            // *** 核心修改: 不再需要调用 hotspotManager.renderForPage ***
                        }).fail(function() {
                            if (pageNum > 1) { // 首页通常是空白，无需占位符
                                $page.html('<div class="page-placeholder"><h3>页面加载失败</h3></div>');
                            }
                        });
                    }
                },
                // turned 回调可以保留，以备未来可能需要在此处执行操作
                turned: function(event, page, view) {
                    // console.log("Turned to page", page);
                }
            }
        });

        // 初始化尺寸并监听窗口大小变化
        updateFlipbookSize(aspectRatio);
        $(window).on('resize', () => setTimeout(() => updateFlipbookSize(aspectRatio), 100));
    }


    // --- 启动逻辑 (保持不变) ---
    // 首先尝试加载第一张有效页面（通常是第2页）以获取图片宽高比，
    // 这是确保翻书组件比例正确的关键。
    if (totalPages > 1) {
        // 尝试加载页面以获取宽高比
        $.get(`pages/page-2.html`).done(htmlContent => {
            // 使用更健壮的方式从HTML字符串中找到img
            const imgSrc = $(htmlContent).find('img').attr('src');
            if (imgSrc) {
                const img = new Image();
                img.onload = function() {
                    const realAspectRatio = this.naturalHeight / this.naturalWidth;
                    createTurnJsInstance(realAspectRatio);
                };
                // 如果图片加载失败，使用一个默认的A4纸比例
                img.onerror = () => createTurnJsInstance(1.414); 
                // 路径需要修正，因为$.get的路径是相对于index.html的
                img.src = imgSrc.replace('../', ''); 
            } else {
                 createTurnJsInstance(1.414); // 页面内容中没有img标签
            }
        }).fail(() => createTurnJsInstance(1.414)); // 页面加载失败
    } else {
         createTurnJsInstance(1.414); // 只有一页或没有页面
    }
}