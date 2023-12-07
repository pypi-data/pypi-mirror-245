import hashlib

from fastapi import Query, Depends
from starlette.responses import PlainTextResponse

from model.po import BookInfoPo
from service import book_service, book_info_service
from tool import id_code_tools
from tool.fastapi import fastapi_router_tools
from tool.sqlalchemy.base import base_crdu
from tool.weixin import weixin_settings
from tool.weixin.core import weixin_depends, weixin_reply_tool
from tool.weixin.core.model.item.receive_msg_models import WeixinTextMsgItem

router = fastapi_router_tools.create_router(prefix='/openapi', tags=['微信接口'])


@router.get("/wx")
async def check_valid_api(signature: str = Query(title='微信加密签名'),
                          timestamp: str = Query(title='时间戳'),
                          nonce: str = Query(title='随机数'),
                          echo_str: str = Query(title='随机字符串', alias='echostr')):
    if signature == hashlib.sha1(
            ''.join(sorted([weixin_settings.weixin_token, timestamp, nonce])).encode('utf-8')).hexdigest():
        # 证明请求来自微信服务器
        return PlainTextResponse(echo_str)
    else:
        return 'Invalid request'


@router.post("/wx")
async def receive_data_api(msg_model=Depends(weixin_depends.convert_params)):
    print(type(msg_model))
    print(msg_model.model_dump())
    if msg_model:
        if isinstance(msg_model, WeixinTextMsgItem):
            msg_text = msg_model.msg_content.strip()
            print(msg_text)
            if msg_text.isdigit():
                book_query = book_info_service.create_book_query(include_download=True)
                book_query_result = book_query.filter(BookInfoPo.code == int(msg_text)).first()
                if book_query_result:
                    book_info_po, download_info_po = book_query_result
                    if book_info_po:
                        share_pwd = id_code_tools.get_tmp_pwd(book_info_po.code)
                        zip_pwd = 'afeng'
                        if download_info_po:
                            if download_info_po.share_pwd:
                                share_pwd = share_pwd
                            if download_info_po.zip_pwd:
                                zip_pwd = download_info_po.zip_pwd
                        return weixin_reply_tool.reply_text(msg_model,
                                                            f'{book_info_po.title}\n 网盘提取码：{share_pwd}\n zip解压码：{zip_pwd}')
                    else:
                        return weixin_reply_tool.reply_text(msg_model,
                                                            f'抱歉，暂无编码为[{msg_text}]的书籍，请检查您的输入！')
        return weixin_reply_tool.reply_text(msg_model, '抱歉，暂无相关服务！现有服务如下：\n 阿锋书屋：https://www.afengbook.com！')
    return 'success'
