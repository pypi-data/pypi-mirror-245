from typing import Callable, Optional

from pydantic import BaseModel


class FastapiConfigItem(BaseModel):
    # 错误404创建context_data的函数，参数：(message: str, is_mobile: bool = False)
    error404_context_data_func: Optional[Callable[[str, bool], dict]] = None
    # 错误500创建context_data的函数，参数：(message: str, is_mobile: bool = False)
    error500_context_data_func: Optional[Callable[[str, bool], dict]] = None
