// FILE: config.js
// 功能: (单页翻书模式) 统一管理从模板注入的全局配置数据。

'use strict';

// 1. 定义一个将被导出的配置对象
export const APP_CONFIG = {
    projectTitle: 'Untitled Project',
    pagesData: [],
    jsPopups: ''
};

/**
 * 初始化配置。
 * 从 window.APP_CONFIG 读取数据并填充到导出的 APP_CONFIG 对象中。
 * 这样做可以避免其他模块直接依赖全局的 window 对象，实现更好的封装。
 */
export function initConfig() {
    const globalConfig = window.APP_CONFIG || {};
    
    // 安全地合并数据，如果全局配置中缺少某个键，则使用默认值
    Object.assign(APP_CONFIG, globalConfig);
    
    // 清理全局对象，避免污染
    // (可选步骤，但这是一个好的实践)
    try {
        delete window.APP_CONFIG;
    } catch (e) {
        window.APP_CONFIG = undefined;
    }
}