"""
主窗口 — 集成数据加载、表格预览、图表绘制的动漫风格主界面。
"""

import os
import numpy as np
import pandas as pd

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QStatusBar, QSplitter, QGroupBox,
    QPushButton, QComboBox, QLabel, QFileDialog,
    QMessageBox, QSizePolicy, QFrame,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QFont

from data_loader.loader import load_file, get_file_info
from plot_engine.chart_canvas import AnimeChartCanvas, setup_chinese_font
from ui.data_table import DataTable
from ui.anime_style import get_anime_stylesheet


# 图表类型选项
CHART_TYPES = {
    '📈 折线图': 'line',
    '📊 柱状图': 'bar',
    '✨ 散点图': 'scatter',
    '🍩 饼图':   'pie',
    '📊 直方图': 'histogram',
}


class AnimeMainWindow(QMainWindow):
    """动漫风格的数据分析主窗口。"""

    def __init__(self):
        super().__init__()
        self.df: pd.DataFrame | None = None
        self.filepath: str | None = None
        self.chart_canvas: AnimeChartCanvas | None = None

        # 设置中文字体
        self._font_name = setup_chinese_font()

        self._init_ui()
        self._apply_style()
        self._connect_signals()

    # ================================================================
    #  UI 初始化
    # ================================================================

    def _init_ui(self):
        """构建界面布局。"""
        self.setWindowTitle('🌸 Sakura Data — 动漫风数据分析工具')
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # ---- 菜单栏 ----
        self._create_menu_bar()

        # ---- 工具栏 ----
        self._create_toolbar()

        # ---- 中央区域 ----
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # 左侧控制面板
        left_panel = self._create_left_panel()
        left_panel.setFixedWidth(260)

        # 右侧：表格 + 图表
        right_splitter = QSplitter(Qt.Orientation.Vertical)

        # 数据表格
        table_group = QGroupBox('📋 数据预览')
        table_layout = QVBoxLayout(table_group)
        self.data_table = DataTable()
        table_layout.addWidget(self.data_table)
        right_splitter.addWidget(table_group)

        # 图表区域
        chart_group = QGroupBox('🎨 图表展示')
        chart_layout = QVBoxLayout(chart_group)
        self.chart_canvas = AnimeChartCanvas(self, width=9, height=4, dpi=100)
        chart_layout.addWidget(self.chart_canvas)
        right_splitter.addWidget(chart_group)

        # 分割比例
        right_splitter.setStretchFactor(0, 3)  # 表格占 3 份
        right_splitter.setStretchFactor(1, 5)  # 图表占 5 份

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_splitter, stretch=1)

        # ---- 状态栏 ----
        self._create_status_bar()

    def _create_menu_bar(self):
        """创建菜单栏。"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('📁 文件')

        open_action = QAction('📂 打开数据文件...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self._on_open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        export_action = QAction('💾 导出图表为图片...', self)
        export_action.setShortcut('Ctrl+S')
        export_action.triggered.connect(self._on_export_chart)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction('🚪 退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 帮助菜单
        help_menu = menubar.addMenu('❓ 帮助')

        about_action = QAction('✨ 关于 Sakura Data', self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _create_toolbar(self):
        """创建工具栏。"""
        toolbar = QToolBar('主工具栏')
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # 打开文件按钮
        btn_open = QPushButton('📂 打开文件')
        btn_open.setObjectName('')
        btn_open.clicked.connect(self._on_open_file)
        toolbar.addWidget(btn_open)

        toolbar.addSeparator()

        # 导出按钮
        btn_export = QPushButton('💾 导出图表')
        btn_export.clicked.connect(self._on_export_chart)
        toolbar.addWidget(btn_export)

        toolbar.addSeparator()

        # 标题标签
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        title = QLabel('🌸 Sakura Data')
        title.setObjectName('titleLabel')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #F5989E; padding-right: 16px;')
        toolbar.addWidget(title)

    def _create_left_panel(self) -> QWidget:
        """创建左侧控制面板。"""
        panel = QWidget()
        panel.setObjectName('leftPanel')
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(12)

        # ---- 文件信息 ----
        info_group = QGroupBox('📁 文件信息')
        info_layout = QVBoxLayout(info_group)
        self.lbl_filename = QLabel('📄 未加载文件')
        self.lbl_filename.setWordWrap(True)
        self.lbl_filename.setStyleSheet('color: #999; font-size: 12px;')
        self.lbl_shape = QLabel('📊 行列: —')
        self.lbl_shape.setStyleSheet('color: #999; font-size: 12px;')
        info_layout.addWidget(self.lbl_filename)
        info_layout.addWidget(self.lbl_shape)
        layout.addWidget(info_group)

        # ---- 图表配置 ----
        chart_group = QGroupBox('⚙️ 图表配置')
        chart_layout = QVBoxLayout(chart_group)
        chart_layout.setSpacing(10)

        # X 轴选择
        lbl_x = QLabel('📐 X 轴列:')
        lbl_x.setObjectName('sectionLabel')
        self.cmb_x = QComboBox()
        self.cmb_x.setPlaceholderText('— 选择 X 轴 —')
        chart_layout.addWidget(lbl_x)
        chart_layout.addWidget(self.cmb_x)

        # Y 轴选择
        lbl_y = QLabel('📏 Y 轴列:')
        lbl_y.setObjectName('sectionLabel')
        self.cmb_y = QComboBox()
        self.cmb_y.setPlaceholderText('— 选择 Y 轴 —')
        chart_layout.addWidget(lbl_y)
        chart_layout.addWidget(self.cmb_y)

        # 图表类型
        lbl_chart = QLabel('🎨 图表类型:')
        lbl_chart.setObjectName('sectionLabel')
        self.cmb_chart = QComboBox()
        self.cmb_chart.addItems(list(CHART_TYPES.keys()))
        chart_layout.addWidget(lbl_chart)
        chart_layout.addWidget(self.cmb_chart)

        layout.addWidget(chart_group)

        # ---- 绘制按钮 ----
        self.btn_plot = QPushButton('🌸 绘制图表')
        self.btn_plot.setObjectName('btnPlot')
        self.btn_plot.setMinimumHeight(48)
        self.btn_plot.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.btn_plot)

        # 弹性空间
        layout.addStretch()

        # ---- 小提示 ----
        tip_frame = QFrame()
        tip_frame.setStyleSheet(
            'QFrame { background: #FFF0F3; border: 1px solid #FFB7C5; '
            'border-radius: 10px; padding: 8px; }'
        )
        tip_layout = QVBoxLayout(tip_frame)
        tip_text = QLabel(
            '💡 小提示:\n'
            '• 支持 CSV/JSON/Excel/TXT\n'
            '• 右键可导出图表图片\n'
            '• 表格点击列头可排序'
        )
        tip_text.setWordWrap(True)
        tip_text.setStyleSheet('font-size: 11px; color: #999;')
        tip_layout.addWidget(tip_text)
        layout.addWidget(tip_frame)

        return panel

    def _create_status_bar(self):
        """创建状态栏。"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('🌸 欢迎使用 Sakura Data！请打开一个数据文件开始分析～')

    def _apply_style(self):
        """应用动漫主题样式。"""
        self.setStyleSheet(get_anime_stylesheet())

    def _connect_signals(self):
        """连接信号和槽。"""
        self.btn_plot.clicked.connect(self._on_plot)
        self.cmb_chart.currentTextChanged.connect(self._on_chart_type_changed)

    # ================================================================
    #  事件处理
    # ================================================================

    def _on_open_file(self):
        """打开文件对话框并加载数据。"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, '📂 打开数据文件',
            os.path.expanduser('~'),
            '数据文件 (*.csv *.tsv *.json *.xlsx *.xls *.txt);;'
            'CSV 文件 (*.csv);;'
            'JSON 文件 (*.json);;'
            'Excel 文件 (*.xlsx *.xls);;'
            '文本文件 (*.txt *.tsv);;'
            '所有文件 (*)'
        )
        if not filepath:
            return

        try:
            self.df = load_file(filepath)
            self.filepath = filepath

            # 更新 UI
            self._update_file_info()
            self._update_column_selectors()
            self.data_table.load_dataframe(self.df)
            self._auto_plot()

            self.status_bar.showMessage(
                f'✅ 已加载: {os.path.basename(filepath)} | '
                f'{self.df.shape[0]} 行 × {self.df.shape[1]} 列'
            )

        except Exception as e:
            QMessageBox.warning(self, '❌ 加载失败', str(e))
            self.status_bar.showMessage(f'❌ 加载失败: {filepath}')

    def _update_file_info(self):
        """更新文件信息显示。"""
        if self.df is None:
            return
        basename = os.path.basename(self.filepath or '')
        self.lbl_filename.setText(f'📄 {basename}')
        self.lbl_shape.setText(
            f'📊 {self.df.shape[0]:,} 行 × {self.df.shape[1]} 列'
        )

    def _update_column_selectors(self):
        """更新 X/Y 轴下拉框的列名列表。"""
        if self.df is None:
            return
        columns = [str(c) for c in self.df.columns]

        self.cmb_x.clear()
        self.cmb_y.clear()
        self.cmb_x.addItems(columns)
        self.cmb_y.addItems(columns)

        # 默认选择：第一列作为 X，最后一列/第二列作为 Y
        if len(columns) >= 2:
            self.cmb_x.setCurrentIndex(0)
            self.cmb_y.setCurrentIndex(1)
        elif len(columns) == 1:
            self.cmb_x.setCurrentIndex(0)
            self.cmb_y.setCurrentIndex(0)

    def _on_chart_type_changed(self, chart_name: str):
        """图表类型切换时，更新 Y 轴选择器状态。"""
        chart_type = CHART_TYPES.get(chart_name, 'line')
        # 饼图只需要 Y 列（标签和数据用同一列或不同列，这里简化处理）
        if chart_type == 'pie' or chart_type == 'histogram':
            self.cmb_x.setEnabled(chart_type == 'pie')
        else:
            self.cmb_x.setEnabled(True)

    def _on_plot(self):
        """执行绘图。"""
        if self.df is None:
            QMessageBox.information(self, '💡 提示', '请先打开一个数据文件～')
            return

        chart_name = self.cmb_chart.currentText()
        chart_type = CHART_TYPES.get(chart_name, 'line')

        x_col = self.cmb_x.currentText()
        y_col = self.cmb_y.currentText()

        if not x_col or not y_col:
            QMessageBox.warning(self, '⚠️ 警告', '请选择 X 轴和 Y 轴对应的列～')
            return

        try:
            self._draw_chart(chart_type, x_col, y_col)
        except Exception as e:
            QMessageBox.critical(self, '❌ 绘图错误', f'绘制图表时出错:\n{str(e)}')

    def _draw_chart(self, chart_type: str, x_col: str, y_col: str):
        """根据类型和列名绘制图表。"""
        df = self.df

        # 获取数据
        x_data = df[x_col].values
        y_data = df[y_col].values

        # 删除 NaN
        mask = pd.notna(x_data) & pd.notna(y_data)
        x_clean = x_data[mask]
        y_clean = y_data[mask]

        if len(x_clean) == 0:
            QMessageBox.warning(self, '⚠️ 警告', '所选列没有有效数据～')
            return

        xlabel = str(x_col)
        ylabel = str(y_col)

        if chart_type == 'line':
            self.chart_canvas.plot_line(
                x_clean, y_clean,
                title=f'📈 {y_col} 趋势图',
                xlabel=xlabel, ylabel=ylabel
            )
        elif chart_type == 'bar':
            # 柱状图最多展示前 30 条
            n_show = min(30, len(x_clean))
            self.chart_canvas.plot_bar(
                x_clean[:n_show], y_clean[:n_show],
                title=f'📊 {y_col} 柱状图',
                xlabel=xlabel, ylabel=ylabel
            )
        elif chart_type == 'scatter':
            self.chart_canvas.plot_scatter(
                x_clean, y_clean,
                title=f'✨ {y_col} vs {x_col}',
                xlabel=xlabel, ylabel=ylabel
            )
        elif chart_type == 'pie':
            # 饼图：用 X 列作为标签，Y 列作为数值
            n_show = min(12, len(x_clean))
            self.chart_canvas.plot_pie(
                [str(l) for l in x_clean[:n_show]],
                y_clean[:n_show],
                title=f'🍩 {y_col} 分布'
            )
        elif chart_type == 'histogram':
            self.chart_canvas.plot_histogram(
                y_clean, bins=min(30, len(y_clean) // 5 + 1),
                title=f'📊 {y_col} 分布直方图',
                xlabel=ylabel
            )

        self.status_bar.showMessage(
            f'✅ 已绘制: {chart_type} | X={x_col} Y={y_col} | '
            f'数据点: {len(x_clean):,}'
        )

    def _auto_plot(self):
        """加载文件后自动尝试绘图。"""
        if self.df is None or self.df.shape[1] < 1:
            return
        self._on_plot()

    def _on_export_chart(self):
        """导出图表为图片文件。"""
        if self.chart_canvas is None:
            QMessageBox.information(self, '💡 提示', '请先绘制一个图表～')
            return

        filepath, _ = QFileDialog.getSaveFileName(
            self, '💾 导出图表', 'chart.png',
            'PNG 图片 (*.png);;'
            'JPEG 图片 (*.jpg *.jpeg);;'
            'PDF 文件 (*.pdf);;'
            'SVG 矢量图 (*.svg)'
        )
        if not filepath:
            return

        try:
            self.chart_canvas.fig.savefig(
                filepath, dpi=150, bbox_inches='tight',
                facecolor=self.chart_canvas.fig.get_facecolor()
            )
            self.status_bar.showMessage(f'✅ 图表已导出: {filepath}')
        except Exception as e:
            QMessageBox.critical(self, '❌ 导出失败', str(e))

    def _on_about(self):
        """显示关于对话框。"""
        QMessageBox.about(
            self,
            '✨ 关于 Sakura Data',
            '<h2>🌸 Sakura Data v1.0</h2>'
            '<p><b>动漫风格数据分析工具</b></p>'
            '<p>技术栈: Python + PyQt6 + Matplotlib + Pandas</p>'
            '<p>功能特色:</p>'
            '<ul>'
            '<li>📂 支持 CSV / JSON / Excel / TXT 格式</li>'
            '<li>📈 折线图 · 柱状图 · 散点图 · 饼图 · 直方图</li>'
            '<li>🌸 樱花动漫风主题 UI</li>'
            '<li>💾 支持导出高清图表</li>'
            '</ul>'
            '<p style="color: #F5989E;">✨ 让数据分析变得可爱起来～ ✨</p>'
        )

    # ================================================================
    #  窗口事件
    # ================================================================

    def resizeEvent(self, event):
        """窗口大小变化时更新图表布局。"""
        super().resizeEvent(event)
        if self.chart_canvas:
            self.chart_canvas.fig.tight_layout()
            self.chart_canvas.draw_idle()
