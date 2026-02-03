// FILE: templates/dynamic_page/static/js/layout.js
// 功能: (滚动模式专用) 包含所有页面交互和加载逻辑。

(function() {
'use strict';

// --- 0. 从全局配置对象获取数据 ---
// outlineBehavior: 'auto_hide' (默认) 或 'fixed'
const { projectTitle, pagesToLoad, jsPopups, outlineBehavior } = window.APP_CONFIG || {};
const behavior = outlineBehavior || 'auto_hide';

// --- 1. DOM元素获取 ---
const toggleBtn = document.getElementById('sidebar-toggle');
const contentContainer = document.getElementById('content-container');
const sidebar = document.querySelector('.sidebar');
const backToTopBtn = document.getElementById('back-to-top-btn');

// --- 2. 注入弹窗JS ---
if (jsPopups) {
    const popupScript = document.createElement('script');
    popupScript.textContent = jsPopups;
    document.body.appendChild(popupScript);
}

// --- 3. 侧边栏交互逻辑 ---
const sidebarStateKey = `sidebarState__${projectTitle ? projectTitle.replace(/\s+/g, "_") : 'default'}`;

function setSidebarCollapsed(collapsed) {
    if (collapsed) {
        document.body.classList.add('sidebar-collapsed');
    } else {
        document.body.classList.remove('sidebar-collapsed');
    }

    // 只有在非固定模式下，才记录用户的折叠偏好
    // 在固定模式下，刷新页面应恢复默认展开，除非用户手动操作（这里保留手动操作的记忆也是一种选择，但为了严格符合"固定显示"语义，通常倾向于保持展开）
    if (behavior !== 'fixed') {
        localStorage.setItem(sidebarStateKey, collapsed ? 'collapsed' : 'expanded');
    }
}

// 初始化侧边栏状态
if (behavior === 'fixed') {
    // 如果是固定模式，默认展开
    setSidebarCollapsed(false);
} else {
    // 否则恢复用户上次的状态
    if (localStorage.getItem(sidebarStateKey) === 'collapsed') {
        setSidebarCollapsed(true);
    } else if (window.innerWidth > 768) {
        // 在桌面端默认展开
        setSidebarCollapsed(false);
    } else {
        // 移动端默认折叠
        setSidebarCollapsed(true);
    }
}

if (toggleBtn) {
    toggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        setSidebarCollapsed(!document.body.classList.contains('sidebar-collapsed'));
    });
}

if (sidebar) {
    sidebar.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (link && link.hash) {
            // 在移动端，允许默认的跳转行为
            if (window.innerWidth <= 768) { return; }

            // 在桌面端，使用平滑滚动
            e.preventDefault();
            const targetElement = document.querySelector(link.hash);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
}

// 点击内容区时自动折叠逻辑
if (contentContainer) {
    contentContainer.addEventListener('mousedown', () => {
        // 核心修改: 只有在非固定模式 ('auto_hide') 下，点击内容区才自动折叠侧边栏
        if (behavior !== 'fixed') {
            if (!document.body.classList.contains('sidebar-collapsed')) {
                setSidebarCollapsed(true);
            }
        }
    });
}

// --- 4. "返回顶部"按钮逻辑 ---
if (backToTopBtn) {
    // 根据屏幕尺寸决定监听哪个元素的滚动事件
    const scrollTarget = window.matchMedia("(max-width: 768px)").matches ? window : contentContainer;

    const handleScroll = () => {
        const scrollTop = (scrollTarget === window) ? window.scrollY : scrollTarget.scrollTop;
        if (scrollTop > 200) {
            backToTopBtn.style.display = 'flex';
            requestAnimationFrame(() => backToTopBtn.classList.add('visible'));
        } else {
            backToTopBtn.classList.remove('visible');
            // 修复：当滚动到顶部时隐藏按钮
            backToTopBtn.style.display = 'none';
        }
    };

    scrollTarget.addEventListener('scroll', handleScroll);

    backToTopBtn.addEventListener('click', () => {
        scrollTarget.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // 初始化按钮状态
    handleScroll();
}

// --- 5. 页面动态加载逻辑 ---
async function loadPages() {
    if (!pagesToLoad || !contentContainer) {
        console.error("Pages to load or content container not found.");
        return;
    }

    for (const pageUrl of pagesToLoad) {
        try {
            const response = await fetch(pageUrl);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const htmlFragment = await response.text();
            contentContainer.insertAdjacentHTML('beforeend', htmlFragment);
        } catch (error) {
            console.error('Failed to load page:', pageUrl, error);
            contentContainer.insertAdjacentHTML('beforeend', `<p style="color:red;text-align:center;">内容加载失败: ${pageUrl}</p>`);
        }
    }
}

// 确保在DOM加载完毕后执行页面加载
if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', loadPages);
} else {
    loadPages();
}

})();