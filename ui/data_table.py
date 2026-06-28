"""
数据预览表格组件 — 基于 QTableWidget，显示 DataFrame 前 N 行。
"""

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import pandas as pd


MAX_PREVIEW_ROWS = 1000  # 预览最多显示行数


class DataTable(QTableWidget):
    """动漫风格的数据预览表格。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """初始化表格外观。"""
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.setSelectionMode(
            QTableWidget.SelectionMode.ExtendedSelection
        )
        self.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        # 表头自适应
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        header.setMinimumSectionSize(60)

        vheader = self.verticalHeader()
        vheader.setDefaultSectionSize(28)
        vheader.setVisible(True)

        # 初始占位
        self.setRowCount(0)
        self.setColumnCount(0)

    def load_dataframe(self, df: pd.DataFrame):
        """加载 DataFrame 到表格中显示。

        Args:
            df: pandas DataFrame
        """
        # 限制预览行数
        preview_df = df.head(MAX_PREVIEW_ROWS)

        n_rows, n_cols = preview_df.shape
        self.setRowCount(n_rows)
        self.setColumnCount(n_cols)

        # 设置列头
        self.setHorizontalHeaderLabels([str(c) for c in preview_df.columns])

        # 填充数据
        for row in range(n_rows):
            for col in range(n_cols):
                val = preview_df.iat[row, col]
                if pd.isna(val):
                    text = ''
                elif isinstance(val, float):
                    text = f'{val:.6g}'
                else:
                    text = str(val)

                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # 数值列右对齐
                if pd.api.types.is_numeric_dtype(preview_df.dtypes[col]):
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )

                self.setItem(row, col, item)

        # 自适应列宽
        self.resizeColumnsToContents()

        # 行号显示
        self.setVerticalHeaderLabels(
            [str(i + 1) for i in range(n_rows)]
        )

    def clear_data(self):
        """清空表格。"""
        self.setRowCount(0)
        self.setColumnCount(0)
        self.setHorizontalHeaderLabels([])
