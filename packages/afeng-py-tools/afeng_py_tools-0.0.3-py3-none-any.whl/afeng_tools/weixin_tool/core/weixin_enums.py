from enum import Enum
from typing import Callable

from pydantic import BaseModel

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


class WeixinConfigKeyEnum(Enum):
    """微信配置枚举"""
    weixin_app_id = 'weixin_app_id'
    weixin_app_secret = 'weixin_app_secret'
    weixin_token = 'weixin_token'
    weixin_encoding_aes_key = 'weixin_encoding_aes_key'
    weixin_msg_callback = 'weixin_msg_callback'
