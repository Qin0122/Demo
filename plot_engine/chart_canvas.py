"""
图表绘制引擎 — 基于 matplotlib 的画布封装，嵌入 PyQt6，自动适配动漫配色。
"""

import matplotlib
matplotlib.use('QtAgg')  # PyQt6 后端

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

# ============================================================
#  动漫配色方案
# ============================================================
SAKURA_PINK     = '#FFB7C5'   # 樱花粉
SKY_BLUE        = '#87CEEB'   # 天空蓝
LAVENDER_PURPLE = '#B39DDB'   # 薰衣草紫
MINT_GREEN      = '#A5D6A7'   # 薄荷绿
WARM_ORANGE     = '#FFCC80'   # 暖橘
CORAL           = '#FF8A80'   # 珊瑚红
LIGHT_YELLOW    = '#FFF9C4'   # 淡黄

# 图表配色序列
ANIME_PALETTE = [
    '#FF8A80', '#FFB7C5', '#B39DDB', '#87CEEB',
    '#A5D6A7', '#FFCC80', '#FFF9C4', '#80CBC4',
    '#F48FB1', '#CE93D8', '#90CAF9', '#A5D6A7',
]

# 图表背景色
FIGURE_BG = '#FFF5F5'   # 暖白偏粉
AXES_BG   = '#FFFAFA'   # 雪白


def setup_chinese_font():
    """尝试设置中文字体，使图表中的中文标签正常显示。"""
    import platform
    system = platform.system()

    font_candidates = []
    if system == 'Windows':
        font_candidates = [
            'Microsoft YaHei', 'SimHei', 'KaiTi', 'FangSong',
            'STSong', 'NSimSun', 'YouYuan',
        ]
    elif system == 'Darwin':  # macOS
        font_candidates = [
            'PingFang SC', 'Heiti SC', 'STHeiti',
            'Apple LiGothic', 'Hiragino Sans GB',
        ]
    else:  # Linux
        font_candidates = [
            'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei',
            'Noto Sans CJK SC', 'Droid Sans Fallback',
        ]

    # 回退：使用 sans-serif
    font_candidates.append('sans-serif')

    for font_name in font_candidates:
        try:
            matplotlib.rcParams['font.family'] = font_name
            # 测试是否支持中文字符
            fig = Figure(figsize=(0.1, 0.1))
            fig.text(0, 0, '测试', fontfamily=font_name)
            plt.close('all')
            return font_name
        except Exception:
            continue
    return 'sans-serif'


class AnimeChartCanvas(FigureCanvas):
    """动漫风格的图表画布，嵌入 PyQt6 窗口。"""

    def __init__(self, parent=None, width=8, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=FIGURE_BG)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(AXES_BG)

        super().__init__(self.fig)
        self.setParent(parent)
        self._apply_anime_style()

    def _apply_anime_style(self):
        """应用动漫风格的图表美化。"""
        ax = self.ax
        # 柔和边框
        for spine in ax.spines.values():
            spine.set_color('#E0D0D0')
            spine.set_linewidth(1.2)

        # 刻度样式
        ax.tick_params(colors='#888888', labelsize=9, grid_color='#F0E0E0',
                       grid_alpha=0.6)
        ax.grid(True, linestyle='--', alpha=0.4, color='#F0D0D0')

        # 标题样式
        ax.title.set_fontsize(14)
        ax.title.set_fontweight('bold')
        ax.title.set_color('#555555')
        ax.xaxis.label.set_color('#777777')
        ax.yaxis.label.set_color('#777777')

    def _clear_and_style(self, title: str = '', xlabel: str = '', ylabel: str = ''):
        """清空并重新设置轴样式。"""
        self.ax.clear()
        self._apply_anime_style()
        if title:
            self.ax.set_title(title)
        if xlabel:
            self.ax.set_xlabel(xlabel)
        if ylabel:
            self.ax.set_ylabel(ylabel)
        self.draw_idle()

    # ---- 各类图表绘制方法 ----

    def plot_line(self, x, y, title: str = '📈 折线图',
                  xlabel: str = '', ylabel: str = ''):
        """绘制折线图。"""
        self._clear_and_style(title, xlabel, ylabel)
        self.ax.plot(x, y, color=SAKURA_PINK, linewidth=2.5, marker='o',
                     markersize=5, markerfacecolor=CORAL,
                     markeredgecolor='white', markeredgewidth=1.2)
        self.ax.fill_between(range(len(x)), y, alpha=0.1, color=SAKURA_PINK)
        self.ax.legend(['数据曲线'], loc='best', framealpha=0.7,
                       facecolor='#FFF0F0', edgecolor='#FFB7C5')
        self._auto_format_xticks(x)
        self.fig.tight_layout()
        self.draw_idle()

    def plot_bar(self, x, y, title: str = '📊 柱状图',
                 xlabel: str = '', ylabel: str = ''):
        """绘制柱状图（渐变动漫色）。"""
        self._clear_and_style(title, xlabel, ylabel)
        n = len(y)
        colors = [ANIME_PALETTE[i % len(ANIME_PALETTE)] for i in range(n)]
        bars = self.ax.bar(range(n), y, color=colors, edgecolor='white',
                           linewidth=1.5, alpha=0.9)
        # 顶部数值标注
        for bar, val in zip(bars, y):
            self.ax.text(bar.get_x() + bar.get_width() / 2.,
                         bar.get_height() + max(y) * 0.01,
                         f'{val:.1f}' if isinstance(val, float) else str(val),
                         ha='center', va='bottom', fontsize=8, color='#999999')
        self.ax.set_xticks(range(n))
        self.ax.set_xticklabels([str(l)[:12] for l in x], rotation=30, ha='right')
        self.fig.tight_layout()
        self.draw_idle()

    def plot_scatter(self, x, y, title: str = '✨ 散点图',
                     xlabel: str = '', ylabel: str = ''):
        """绘制散点图。"""
        self._clear_and_style(title, xlabel, ylabel)
        sizes = np.linspace(40, 120, len(x))
        colors = np.linspace(0.2, 0.9, len(x))
        self.ax.scatter(x, y, s=sizes, c=colors, cmap='RdPu',
                        alpha=0.75, edgecolors='white', linewidth=0.8)
        self.fig.tight_layout()
        self.draw_idle()

    def plot_pie(self, labels, values, title: str = '🍩 饼图'):
        """绘制饼图。"""
        self._clear_and_style(title)
        colors = ANIME_PALETTE[:len(labels)]
        wedges, texts, autotexts = self.ax.pie(
            values, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=90,
            pctdistance=0.75, explode=[0.03] * len(labels),
            shadow=False, wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        # 美化百分比文字
        for at in autotexts:
            at.set_color('#555555')
            at.set_fontsize(9)
            at.set_fontweight('bold')
        for t in texts:
            t.set_fontsize(10)
            t.set_color('#666666')
        self.ax.legend(wedges, labels, loc='center left',
                       bbox_to_anchor=(1, 0, 0.5, 1),
                       framealpha=0.7, facecolor='#FFF0F0',
                       edgecolor='#FFB7C5')
        self.fig.tight_layout()
        self.draw_idle()

    def plot_histogram(self, data, bins: int = 20,
                       title: str = '📊 直方图',
                       xlabel: str = '', ylabel: str = '频数'):
        """绘制直方图。"""
        self._clear_and_style(title, xlabel, ylabel)
        self.ax.hist(data, bins=bins, color=LAVENDER_PURPLE,
                     edgecolor='white', linewidth=1.2, alpha=0.85)
        self.fig.tight_layout()
        self.draw_idle()

    def _auto_format_xticks(self, x):
        """自动格式化 X 轴刻度，避免标签重叠。"""
        if len(x) > 20:
            step = max(1, len(x) // 10)
            self.ax.set_xticks(range(0, len(x), step))
            self.ax.set_xticklabels(
                [str(x[i])[:12] for i in range(0, len(x), step)],
                rotation=30, ha='right'
            )
        else:
            self.ax.set_xticks(range(len(x)))
            self.ax.set_xticklabels([str(v)[:12] for v in x], rotation=30, ha='right')
