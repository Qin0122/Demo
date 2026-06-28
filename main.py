"""
🌸 Sakura Data — 动漫风格数据分析工具

入口文件：启动 PyQt6 应用，加载动漫主题，显示主窗口。
"""

import sys
import os

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from ui.main_window import AnimeMainWindow
from ui.anime_style import get_anime_stylesheet


def main():
    # 高 DPI 支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName('Sakura Data')
    app.setApplicationVersion('1.0.0')
    app.setOrganizationName('SakuraLab')

    # 应用全局动漫主题
    app.setStyleSheet(get_anime_stylesheet())

    # 创建并显示主窗口
    window = AnimeMainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
