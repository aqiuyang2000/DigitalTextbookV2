# D:\projects\singlepage\hotspot_editor\main_window.py (FIXED)
#
# 功能: 这是 HotspotEditor 主窗口的最终组合文件。

# --- A. 基础类别 ---
from main_window_parts._base import HotspotEditorBase

# --- B. UI 设置与初始化 ---
from main_window_parts._mixin_setup_ui import SetupUiMixin
from main_window_parts._mixin_setup_properties_panel import SetupPropertiesPanelMixin
from main_window_parts._mixin_connect_signals import ConnectSignalsMixin
from main_window_parts._mixin_create_menus import CreateMenusMixin
from main_window_parts._mixin_open_settings_dialog import OpenSettingsDialogMixin
from main_window_parts._mixin_on_settings_applied import OnSettingsAppliedMixin
from main_window_parts._mixin_aspect_ratio_handler import AspectRatioHandlerMixin
# --- *** 核心修改: 导入新的 AutoIconHandlerMixin *** ---
from main_window_parts._mixin_auto_icon_handler import AutoIconHandlerMixin

# --- C. UI 状态更新 ---
from main_window_parts._mixin_update_ui_for_active_session import UpdateUiForActiveSessionMixin
# ... (其他导入保持不变) ...
from main_window_parts._mixin_update_hotspot_info import UpdateHotspotInfoMixin
from main_window_parts._mixin_update_viewers_layout import UpdateViewersLayoutMixin
from main_window_parts._mixin_update_window_title import UpdateWindowMixin
from main_window_parts._mixin_set_dirty import SetDirtyMixin
from main_window_parts._mixin_set_properties_enabled import SetPropertiesEnabledMixin
from main_window_parts._mixin_update_popup_size_visibility import UpdatePopupSizeVisibilityMixin
from main_window_parts._mixin_validate_page_input_text import ValidatePageInputTextMixin

# --- D. 事件处理 (Event Handling) ---
from main_window_parts._mixin_close_event import CloseEventMixin
from main_window_parts._mixin_resize_event import ResizeEventMixin
from main_window_parts._mixin_on_scroll import OnScrollMixin
from main_window_parts._mixin_on_geometry_field_committed import OnGeometryFieldCommittedMixin
from main_window_parts._mixin_handle_viewer_press import HandleViewerPressMixin

# --- E. 专案档案管理 (I/O) ---
from main_window_parts._mixin_new_project import NewProjectMixin
from main_window_parts._mixin_open_project import OpenProjectMixin
from main_window_parts._mixin_save_project import SaveProjectMixin
from main_window_parts._mixin_save_project_as import SaveProjectAsMixin
from main_window_parts._mixin_perform_project_load import PerformProjectLoadMixin
from main_window_parts._mixin_load_last_project import LoadLastProjectMixin
from main_window_parts._mixin_clear_project import ClearProjectMixin
from main_window_parts._mixin_process_and_load_source_for_page import ProcessAndLoadSourceForPageMixin

# --- F. 页面与会话管理 ---
from main_window_parts._mixin_open_image import OpenImageMixin
from main_window_parts._mixin_load_image_path import LoadImagePathMixin
from main_window_parts._mixin_active_session_property import ActiveSessionPropertyMixin
from main_window_parts._mixin_set_active_session import SetActiveSessionMixin
from main_window_parts._mixin_set_active_session_by_viewer import SetActiveSessionByViewerMixin
from main_window_parts._mixin_next_page import NextPageMixin
from main_window_parts._mixin_previous_page import PreviousPageMixin
from main_window_parts._mixin_go_to_page import GoToPageMixin
from main_window_parts._mixin_go_to_page_from_input import GoToPageFromInputMixin
from main_window_parts._mixin_delete_current_page import DeleteCurrentPageMixin

# --- G. 热区核心操作 ---
from main_window_parts._mixin_copy_selected_hotspots import CopySelectedHotspotsMixin
from main_window_parts._mixin_paste_hotspots import PasteHotspotsMixin
from main_window_parts._mixin_delete_selected_hotspot import DeleteSelectedHotspotMixin
from main_window_parts._mixin_select_hotspot_file import SelectHotspotFileMixin
from main_window_parts._mixin_toggle_outline_panel import ToggleOutlinePanelMixin

# --- H. 热区资料提交 (Commands) ---
from main_window_parts._mixin_commit_geometry_change import CommitGeometryChangeMixin
from main_window_parts._mixin_commit_batch_geometry_change import CommitBatchGeometryChangeMixin
from main_window_parts._mixin_commit_data_change import CommitDataChangeMixin
from main_window_parts._mixin_on_outline_changed import OnOutlineChangedMixin

# --- I. 批次处理与工具 ---
from main_window_parts._mixin_batch_import_hotspots import BatchImportHotspotsMixin
from main_window_parts._mixin_open_batch_scale_dialog import OpenBatchScaleDialogMixin
from main_window_parts._mixin_open_pdf_toolbox import OpenPdfToolboxMixin
from main_window_parts._mixin_update_pdf_conversion_progress import UpdatePdfConversionProgressMixin
from main_window_parts._mixin_preview_in_browser import PreviewInBrowserMixin
# --- J. 汇出功能 ---
from main_window_parts._mixin_export_all_formats import ExportAllFormatsMixin
from main_window_parts._mixin_update_all_fragments import UpdateAllFragmentsMixin
from main_window_parts._mixin_export_hotspot_data import ExportHotspotDataMixin
from main_window_parts._mixin_export_current_page_data import ExportCurrentPageDataMixin
from main_window_parts._mixin_export_as_double_page_flipbook_wrapper import ExportAsDoublePageFlipbookWrapperMixin
from main_window_parts._mixin_export_as_single_page_flipbook_wrapper import ExportAsSinglePageFlipbookWrapperMixin
from main_window_parts._mixin_export_as_dynamic_page_wrapper import ExportAsDynamicPageWrapperMixin
from main_window_parts._mixin_export_as_double_page_fragment_wrapper import ExportAsDoublePageFragmentWrapperMixin
from main_window_parts._mixin_export_as_single_flipbook_page_wrapper import ExportAsSingleFlipbookPageWrapperMixin
from main_window_parts._mixin_export_to_html_wrapper import ExportToHtmlWrapperMixin
from main_window_parts._mixin_run_export import RunExportMixin
from main_window_parts._mixin_run_fragment_export import RunFragmentExportMixin

# --- K. 辅助/内部方法 (Helpers & Getters) ---
from main_window_parts._mixin_get_workspace_path import GetWorkspacePathMixin
from main_window_parts._mixin_get_project_asset_dir_path import GetProjectAssetDirPathMixin
from main_window_parts._mixin_get_output_directory import GetOutputDirectoryMixin
from main_window_parts._mixin_ensure_output_directory import EnsureOutputDirectoryMixin
from main_window_parts._mixin_get_common_output_dir import GetCommonOutputDirectoryMixin
from main_window_parts._mixin_get_hotspot_pen import GetHotspotPenMixin
from main_window_parts._mixin_get_hotspot_brush import GetHotspotBrushMixin
from main_window_parts._mixin_get_session_by_viewer import GetSessionByViewerMixin
from main_window_parts._mixin_generate_new_hotspot_id import GenerateNewHotspotIdMixin
from main_window_parts._mixin_get_current_shape import GetCurrentShapeMixin


class HotspotEditor(
    # --- 继承顺序 ---
    HotspotEditorBase,

    ActiveSessionPropertyMixin,
    AspectRatioHandlerMixin,
    # --- *** 核心修改: 将新的 AutoIconHandlerMixin 添加到继承列表中 *** ---
    AutoIconHandlerMixin,
    # --- *** 修复结束 *** ---
    BatchImportHotspotsMixin,
    ClearProjectMixin,
    CloseEventMixin,
    CommitBatchGeometryChangeMixin,
    CommitDataChangeMixin,
    CommitGeometryChangeMixin,
    ConnectSignalsMixin,
    CopySelectedHotspotsMixin,
    CreateMenusMixin,
    DeleteCurrentPageMixin,
    DeleteSelectedHotspotMixin,
    EnsureOutputDirectoryMixin,
    ExportAllFormatsMixin,
    ExportAsDoublePageFlipbookWrapperMixin,
    ExportAsDoublePageFragmentWrapperMixin,
    ExportAsDynamicPageWrapperMixin,
    ExportAsSingleFlipbookPageWrapperMixin,
    ExportAsSinglePageFlipbookWrapperMixin,
    ExportCurrentPageDataMixin,
    ExportHotspotDataMixin,
    ExportToHtmlWrapperMixin,
    GenerateNewHotspotIdMixin,
    GetCommonOutputDirectoryMixin,
    GetCurrentShapeMixin,
    GetHotspotBrushMixin,
    GetHotspotPenMixin,
    GetOutputDirectoryMixin,
    GetProjectAssetDirPathMixin,
    GetSessionByViewerMixin,
    GetWorkspacePathMixin,
    GoToPageMixin,
    GoToPageFromInputMixin,
    HandleViewerPressMixin,
    LoadImagePathMixin,
    LoadLastProjectMixin,
    NewProjectMixin,
    NextPageMixin,
    OnGeometryFieldCommittedMixin,
    OnOutlineChangedMixin,
    OnScrollMixin,
    OnSettingsAppliedMixin,
    OpenBatchScaleDialogMixin,
    OpenImageMixin,
    OpenPdfToolboxMixin,
    OpenProjectMixin,
    OpenSettingsDialogMixin,
    PasteHotspotsMixin,
    PerformProjectLoadMixin,
    PreviousPageMixin,
    ProcessAndLoadSourceForPageMixin,
    PreviewInBrowserMixin,
    ResizeEventMixin,
    RunExportMixin,
    RunFragmentExportMixin,
    SaveProjectAsMixin,
    SaveProjectMixin,
    SelectHotspotFileMixin,
    SetActiveSessionByViewerMixin,
    SetActiveSessionMixin,
    SetDirtyMixin,
    SetPropertiesEnabledMixin,
    SetupPropertiesPanelMixin,
    SetupUiMixin,
    ToggleOutlinePanelMixin,
    UpdateAllFragmentsMixin,
    UpdateHotspotInfoMixin,
    UpdatePdfConversionProgressMixin,
    UpdatePopupSizeVisibilityMixin,
    UpdateUiForActiveSessionMixin,
    UpdateViewersLayoutMixin,
    UpdateWindowMixin,
    ValidatePageInputTextMixin
):
    """
    通过多重继承组合所有功能性 Mixin 类，构建最终的 HotspotEditor 主窗口。
    """
    pass