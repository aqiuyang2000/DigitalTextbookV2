// FILE: templates/flipbook_modular_assets/js/modules/hotspotManager.js
// 功能: 封装 hotspotManager 对象，负责解析数据并在页面上渲染热区。

'use strict';

/**
 * 热区管理器，一个单例对象。
 */
export const hotspotManager = {
    
    data: null, // 用于存储解析后的热区数据

    /**
     * 初始化管理器，解析从模板传入的JSON数据。
     * @param {object} hotspotsJsonData - 从 APP_CONFIG 传入的原始热区数据对象。
     */
    init: function(hotspotsJsonData) {
        // 如果没有数据或数据为空对象，则设置为 null
        if (!hotspotsJsonData || Object.keys(hotspotsJsonData).length === 0) {
            this.data = null;
        } else {
            this.data = hotspotsJsonData;
        }
    },

    /**
     * 为指定的页面元素渲染其对应的所有热区。
     * @param {jQuery} pageElement - 代表单个页面的jQuery对象 (e.g., <div page="2">...</div>)。
     * @param {number} pageNum - 当前页面的页码。
     */
    renderForPage: function(pageElement, pageNum) {
        // 1. 先移除旧的热区图层，以防重复渲染
        if (pageElement) {
            pageElement.find(".hotspot-layer").remove();
        }

        // 2. 检查是否存在当前页面的热区数据
        if (!this.data || !this.data[pageNum] || !pageElement || !pageElement.length) {
            return; // 没有数据或元素，直接返回
        }

        // 3. 找到页面内的图片元素，它是计算相对位置的基准
        const img = pageElement.find("img")[0];
        if (!img) return;

        /**
         * 核心渲染函数。
         */
        const render = () => {
            const naturalWidth = img.naturalWidth;
            const naturalHeight = img.naturalHeight;

            // 如果图片尺寸无效（例如图片尚未加载完成），则中止
            if (naturalWidth === 0) return;

            // 创建一个新的热区图层
            const layer = $('<div class="hotspot-layer"></div>');

            // 遍历当前页面的所有热区数据
            this.data[pageNum].forEach(hotspot => {
                const link = $(`<a class="hotspot ${hotspot.shape}"></a>`);
                
                // 根据图片原始尺寸和热区绝对像素位置，计算出相对百分比位置
                link.css({
                    left: `${(hotspot.rect.x / naturalWidth) * 100}%`,
                    top: `${(hotspot.rect.y / naturalHeight) * 100}%`,
                    width: `${(hotspot.rect.width / naturalWidth) * 100}%`,
                    height: `${(hotspot.rect.height / naturalHeight) * 100}%`
                });

                // 设置链接和点击事件
                if (hotspot.href) link.attr("href", hotspot.href).attr("target", hotspot.target);
                if (hotspot.onclick) link.attr("onclick", hotspot.onclick);
                
                layer.append(link);
            });

            pageElement.append(layer);
        };

        // 4. 确保在图片加载完成后再执行渲染
        //    如果图片已加载完成，立即渲染；否则，等待 'load' 事件。
        if (img.complete && img.naturalWidth > 0) {
            render();
        } else {
            $(img).on("load", render);
        }
    }
};