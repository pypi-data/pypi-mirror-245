from enum import Enum
from typing import Callable

from pydantic import BaseModel


class WeixinConfigItem(BaseModel):
    """微信配置枚举"""
    weixin_app_id: str
    weixin_app_secret: str
    weixin_token: str
    weixin_encoding_aes_key: str
    weixin_msg_callback: Callable


class WeixinConfigKeyEnum(Enum):
    """微信配置枚举"""
    weixin_app_id = 'weixin_app_id'
    weixin_app_secret = 'weixin_app_secret'
    weixin_token = 'weixin_token'
    weixin_encoding_aes_key = 'weixin_encoding_aes_key'
    weixin_msg_callback = 'weixin_msg_callback'
