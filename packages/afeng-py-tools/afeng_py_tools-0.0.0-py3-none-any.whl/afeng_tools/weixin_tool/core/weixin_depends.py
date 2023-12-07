import hashlib

from fastapi import Query
from starlette.requests import Request

from tool.weixin import weixin_settings
from tool.weixin.core.model.item.receive_event_models import WeixinEventItem
from tool.weixin.core.model.item.receive_msg_models import WeixinImageMsgItem, WeixinTextMsgItem, WeixinVoiceMsgItem, \
    WeixinVideoMsgItem, WeixinLocationMsgItem, WeixinLinkMsgItem
from tool.weixin.core.parse import parse_receive


async def convert_params(request: Request, signature: str = Query(title='微信加密签名'),
                         timestamp: str = Query(title='时间戳'),
                         nonce: str = Query(title='随机数'),
                         openid: str = Query(title='OpenID')) -> WeixinTextMsgItem | WeixinImageMsgItem | WeixinVoiceMsgItem | WeixinVideoMsgItem | WeixinLocationMsgItem | WeixinLinkMsgItem | WeixinEventItem:
    """格式化参数"""
    if signature == hashlib.sha1(
            ''.join(sorted([weixin_settings.weixin_token, timestamp, nonce])).encode('utf-8')).hexdigest():
        # 证明请求来自微信服务器
        if request.headers['content-type'] == 'text/xml':
            body = await request.body()
            return parse_receive.parse(openid, body)
