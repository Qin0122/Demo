"""
动漫风格全局样式表 — 樱花粉 + 天空蓝 + 薰衣草紫的柔和配色。
"""

# ============================================================
#  配色常量
# ============================================================
SAKURA_PINK     = '#FFB7C5'
SAKURA_LIGHT    = '#FFF0F3'
SAKURA_DARK     = '#F5989E'
SKY_BLUE        = '#87CEEB'
SKY_LIGHT       = '#E8F6FB'
SKY_DARK        = '#5BA4CF'
LAVENDER        = '#B39DDB'
LAVENDER_LIGHT  = '#F3EDF9'
LAVENDER_DARK   = '#9575CD'
MINT_GREEN      = '#A5D6A7'
WARM_WHITE      = '#FFFAFA'
SOFT_GRAY       = '#F5F0F0'
TEXT_DARK        = '#555555'
TEXT_LIGHT       = '#999999'
BORDER_SOFT      = '#E8D8D8'


def get_anime_stylesheet() -> str:
    """返回完整的动漫主题 QSS 样式表。"""
    return f"""
/* ============================================================
   全局样式
   ============================================================ */
QMainWindow {{
    background-color: {WARM_WHITE};
}}

QWidget {{
    font-family: "Microsoft YaHei", "PingFang SC", "幼圆", "YouYuan", sans-serif;
    font-size: 13px;
    color: {TEXT_DARK};
}}

/* ============================================================
   菜单栏
   ============================================================ */
QMenuBar {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 {SAKURA_LIGHT}, stop:1 {LAVENDER_LIGHT});
    padding: 4px 8px;
    border-bottom: 2px solid {SAKURA_PINK};
    font-size: 14px;
}}

QMenuBar::item {{
    padding: 6px 14px;
    margin: 2px 4px;
    border-radius: 10px;
    background: transparent;
}}

QMenuBar::item:selected {{
    background: rgba(255, 183, 197, 0.45);
    border: 1px solid {SAKURA_PINK};
}}

QMenu {{
    background-color: {WARM_WHITE};
    border: 2px solid {SAKURA_PINK};
    border-radius: 10px;
    padding: 6px;
}}

QMenu::item {{
    padding: 7px 28px 7px 16px;
    border-radius: 6px;
    margin: 2px 4px;
}}

QMenu::item:selected {{
    background-color: {SAKURA_LIGHT};
    color: {TEXT_DARK};
}}

/* ============================================================
   工具栏
   ============================================================ */
QToolBar {{
    background: {WARM_WHITE};
    border-bottom: 1px solid {BORDER_SOFT};
    padding: 4px 8px;
    spacing: 8px;
}}

QToolButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {WARM_WHITE}, stop:1 {SAKURA_LIGHT});
    border: 1.5px solid {SAKURA_PINK};
    border-radius: 12px;
    padding: 7px 18px;
    font-weight: bold;
    color: {TEXT_DARK};
    font-size: 13px;
}}

QToolButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {SAKURA_LIGHT}, stop:1 {SAKURA_PINK});
    border-color: {SAKURA_DARK};
    padding: 6px 17px;  /* 轻微放大感 */
}}

QToolButton:pressed {{
    background: {SAKURA_PINK};
    border-color: {SAKURA_DARK};
    padding: 8px 19px;
}}

/* ============================================================
   按钮（通用）
   ============================================================ */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {SKY_LIGHT}, stop:1 {SKY_BLUE});
    border: 1.5px solid {SKY_DARK};
    border-radius: 14px;
    padding: 9px 22px;
    font-weight: bold;
    font-size: 13px;
    color: {TEXT_DARK};
    min-height: 20px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {SKY_BLUE}, stop:1 {SKY_DARK});
    color: white;
}}

QPushButton:pressed {{
    background: {SKY_DARK};
    color: white;
}}

QPushButton:disabled {{
    background: #E0E0E0;
    border-color: #cccccc;
    color: #aaaaaa;
}}

/* 主要操作按钮（粉色） */
QPushButton#btnPlot {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {SAKURA_LIGHT}, stop:1 {SAKURA_PINK});
    border: 1.5px solid {SAKURA_DARK};
    font-size: 15px;
    padding: 11px 32px;
}}

QPushButton#btnPlot:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {SAKURA_PINK}, stop:1 {SAKURA_DARK});
    color: white;
}}

/* ============================================================
   下拉框
   ============================================================ */
QComboBox {{
    background-color: {WARM_WHITE};
    border: 1.5px solid {LAVENDER};
    border-radius: 10px;
    padding: 7px 14px;
    min-width: 120px;
    font-size: 13px;
    color: {TEXT_DARK};
}}

QComboBox:hover {{
    border-color: {LAVENDER_DARK};
}}

QComboBox:focus {{
    border-color: {LAVENDER_DARK};
    box-shadow: 0 0 6px rgba(179, 157, 219, 0.4);
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid {LAVENDER};
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    background: {LAVENDER_LIGHT};
}}

QComboBox QAbstractItemView {{
    background-color: {WARM_WHITE};
    border: 2px solid {LAVENDER};
    border-radius: 8px;
    padding: 4px;
    selection-background-color: {LAVENDER_LIGHT};
    outline: none;
}}

/* ============================================================
   表格
   ============================================================ */
QTableWidget {{
    background-color: {WARM_WHITE};
    border: 2px solid {BORDER_SOFT};
    border-radius: 10px;
    gridline-color: {SAKURA_LIGHT};
    selection-background-color: {SAKURA_LIGHT};
    selection-color: {TEXT_DARK};
    alternate-background-color: #FFF8F8;
}}

QTableWidget::item {{
    padding: 5px 10px;
}}

QTableWidget::item:selected {{
    background-color: {SAKURA_LIGHT};
    color: {TEXT_DARK};
    border: 1px solid {SAKURA_PINK};
}}

QHeaderView::section {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {SAKURA_LIGHT}, stop:1 {LAVENDER_LIGHT});
    padding: 8px 12px;
    border: none;
    border-right: 1px solid {BORDER_SOFT};
    border-bottom: 2px solid {SAKURA_PINK};
    font-weight: bold;
    font-size: 13px;
    color: {TEXT_DARK};
}}

/* ============================================================
   滚动条
   ============================================================ */
QScrollBar:vertical {{
    background: {WARM_WHITE};
    width: 12px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 {SAKURA_PINK}, stop:1 {LAVENDER});
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 {SAKURA_DARK}, stop:1 {LAVENDER_DARK});
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {WARM_WHITE};
    height: 12px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {SAKURA_PINK}, stop:1 {LAVENDER});
    border-radius: 6px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {SAKURA_DARK}, stop:1 {LAVENDER_DARK});
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* ============================================================
   标签页
   ============================================================ */
QTabWidget::pane {{
    border: 2px solid {BORDER_SOFT};
    border-radius: 10px;
    background: {WARM_WHITE};
}}

QTabBar::tab {{
    background: {SOFT_GRAY};
    border: 1.5px solid {BORDER_SOFT};
    border-radius: 10px;
    padding: 7px 18px;
    margin: 2px 3px;
    font-size: 13px;
}}

QTabBar::tab:selected {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 {SAKURA_LIGHT}, stop:1 {LAVENDER_LIGHT});
    border-color: {SAKURA_PINK};
    font-weight: bold;
}}

QTabBar::tab:hover {{
    background: {SAKURA_LIGHT};
}}

/* ============================================================
   分组框
   ============================================================ */
QGroupBox {{
    border: 2px solid {LAVENDER};
    border-radius: 12px;
    margin-top: 12px;
    padding: 18px 14px 14px 14px;
    background-color: {WARM_WHITE};
    font-weight: bold;
    font-size: 14px;
    color: {LAVENDER_DARK};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 14px;
    margin-left: 14px;
    background-color: {WARM_WHITE};
    border: 2px solid {LAVENDER};
    border-radius: 10px;
    color: {LAVENDER_DARK};
}}

/* ============================================================
   状态栏
   ============================================================ */
QStatusBar {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 {SAKURA_LIGHT}, stop:1 {LAVENDER_LIGHT});
    border-top: 2px solid {SAKURA_PINK};
    padding: 4px 12px;
    font-size: 12px;
    color: {TEXT_LIGHT};
}}

/* ============================================================
   标签
   ============================================================ */
QLabel#titleLabel {{
    font-size: 18px;
    font-weight: bold;
    color: {SAKURA_DARK};
    padding: 4px 0px;
}}

QLabel#sectionLabel {{
    font-size: 14px;
    font-weight: bold;
    color: {LAVENDER_DARK};
    padding: 6px 0px;
}}

/* ============================================================
   分割线
   ============================================================ */
QSplitter::handle {{
    background-color: {BORDER_SOFT};
    width: 2px;
    height: 2px;
}}

/* ============================================================
   输入框
   ============================================================ */
QLineEdit {{
    background-color: {WARM_WHITE};
    border: 1.5px solid {LAVENDER};
    border-radius: 10px;
    padding: 7px 12px;
    font-size: 13px;
    color: {TEXT_DARK};
}}

QLineEdit:focus {{
    border-color: {LAVENDER_DARK};
    box-shadow: 0 0 6px rgba(179, 157, 219, 0.4);
}}
"""


def get_matplotlib_rc_params() -> dict:
    """获取 matplotlib 的动漫主题 rcParams 配置。"""
    return {
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'axes.facecolor': '#FFFAFA',
        'figure.facecolor': '#FFF5F5',
        'grid.color': '#F0D0D0',
        'grid.alpha': 0.5,
        'grid.linestyle': '--',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.edgecolor': '#E0D0D0',
        'xtick.color': '#888888',
        'ytick.color': '#888888',
    }
