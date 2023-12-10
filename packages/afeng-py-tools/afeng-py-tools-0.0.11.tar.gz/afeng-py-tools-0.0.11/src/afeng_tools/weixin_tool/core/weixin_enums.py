import os
from enum import Enum
from typing import Callable, Optional

from pydantic import BaseModel

from afeng_tools.os_tool.os_tools import get_user_home
from afeng_tools.weixin_tool.core.model.item.wx_receive_event_models import WeixinEventItem, WeixinSubscribeEventItem, \
    WeixinQrEventItem, WeixinScanEventItem, WeixinLocationEventItem, WeixinMenuEventItem
from afeng_tools.weixin_tool.core.model.item.wx_receive_msg_models import WeixinVoiceMsgItem, WeixinTextMsgItem, \
    WeixinImageMsgItem, WeixinVideoMsgItem, WeixinLocationMsgItem, WeixinLinkMsgItem
from afeng_tools.weixin_tool.core.response import XmlResponse


class WeixinConfigItem(BaseModel):
    """微信配置枚举"""
    weixin_app_id: str
    weixin_app_secret: str
    weixin_token: str
    weixin_encoding_aes_key: str
    weixin_msg_callback: Callable[[
        WeixinTextMsgItem | WeixinImageMsgItem | WeixinVoiceMsgItem | WeixinVideoMsgItem | WeixinLocationMsgItem | WeixinLinkMsgItem | WeixinEventItem | WeixinSubscribeEventItem | WeixinQrEventItem | WeixinScanEventItem | WeixinLocationEventItem | WeixinMenuEventItem], XmlResponse]
    weixin_token_file: Optional[str] = os.path.join(get_user_home(), f'.wx_access_token.bin')


class WeixinConfigKeyEnum(Enum):
    """微信配置枚举"""
    weixin_app_id = 'weixin_app_id'
    weixin_app_secret = 'weixin_app_secret'
    weixin_token = 'weixin_token'
    weixin_encoding_aes_key = 'weixin_encoding_aes_key'
    weixin_msg_callback = 'weixin_msg_callback'
    weixin_token_file = 'weixin_token_file'
