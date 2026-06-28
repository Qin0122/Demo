"""
数据加载模块 — 支持 CSV、TSV、JSON、Excel、TXT 等常见格式的统一加载接口。
"""

import os
import pandas as pd


SUPPORTED_FORMATS = {
    '.csv':  'CSV (逗号分隔)',
    '.tsv':  'TSV (Tab 分隔)',
    '.txt':  '文本文件',
    '.json': 'JSON 文件',
    '.xlsx': 'Excel 工作簿 (.xlsx)',
    '.xls':  'Excel 工作簿 (.xls)',
}


def load_file(filepath: str) -> pd.DataFrame:
    """根据文件扩展名自动选择加载方式，返回 pandas DataFrame。

    Args:
        filepath: 文件的完整路径

    Returns:
        pandas DataFrame

    Raises:
        ValueError: 不支持的格式
        FileNotFoundError: 文件不存在
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ 找不到文件: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()

    if ext not in SUPPORTED_FORMATS:
        raise ValueError(
            f"❌ 不支持的格式 '{ext}'\n"
            f"支持的格式: {', '.join(SUPPORTED_FORMATS.keys())}"
        )

    try:
        if ext == '.csv':
            # 尝试常见编码
            df = _read_csv_with_fallback(filepath, sep=',')
        elif ext == '.tsv':
            df = _read_csv_with_fallback(filepath, sep='\t')
        elif ext == '.txt':
            # TXT 可能是分隔符文件，尝试自动检测
            df = _read_csv_with_fallback(filepath, sep=None)
        elif ext == '.json':
            df = pd.read_json(filepath, encoding='utf-8')
        elif ext in ('.xlsx', '.xls'):
            df = pd.read_excel(filepath, engine='openpyxl' if ext == '.xlsx' else 'xlrd')
        else:
            raise ValueError(f"❌ 不支持的格式: {ext}")

        # 清理列名
        df.columns = [str(col).strip() for col in df.columns]

        return df

    except Exception as e:
        raise ValueError(f"❌ 文件加载失败: {filepath}\n错误详情: {str(e)}")


def _read_csv_with_fallback(filepath: str, sep: str | None = ',') -> pd.DataFrame:
    """尝试多种编码读取 CSV/TXT 文件。"""
    # 如果 sep 为 None，让 pandas 自动检测（Python 引擎的 sep=None）
    for encoding in ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'gb18030', 'latin-1']:
        try:
            if sep is None:
                # 自动检测分隔符
                df = pd.read_csv(
                    filepath, sep=None, engine='python',
                    encoding=encoding, on_bad_lines='skip'
                )
            else:
                df = pd.read_csv(
                    filepath, sep=sep, encoding=encoding,
                    on_bad_lines='skip'
                )
            return df
        except (UnicodeDecodeError, UnicodeError):
            continue

    # 最后尝试 latin-1 + 宽松模式
    return pd.read_csv(
        filepath, sep=sep if sep else ',', encoding='latin-1',
        on_bad_lines='skip'
    )


def get_file_info(df: pd.DataFrame) -> dict:
    """获取 DataFrame 的基本信息。"""
    return {
        'rows': len(df),
        'cols': len(df.columns),
        'columns': list(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'null_count': df.isnull().sum().sum(),
    }
