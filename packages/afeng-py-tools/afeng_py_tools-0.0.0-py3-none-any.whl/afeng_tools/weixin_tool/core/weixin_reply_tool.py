import math
import time

from tool.weixin.core.format import format_replay
from tool.weixin.core.format.reply_msg.models import WeixinReplyTextMsg
from tool.weixin.core.response import XmlResponse


def reply_text(source_msg_model, text_content: str):
    """响应文本内容"""
    crate_time = math.floor(time.time())
    reply_msg = WeixinReplyTextMsg(to_user=source_msg_model.from_user, from_user=source_msg_model.to_user,
                                   create_time=crate_time,
                                   content=text_content)
    return XmlResponse(format_replay.format_msg(reply_msg))


def reply_text(source_msg_model, text_content: str):
    """响应文本内容"""
    crate_time = math.floor(time.time())
    reply_msg = WeixinReplyTextMsg(to_user=source_msg_model.from_user, from_user=source_msg_model.to_user,
                                   create_time=crate_time,
                                   content=text_content)
    return XmlResponse(format_replay.format_msg(reply_msg))