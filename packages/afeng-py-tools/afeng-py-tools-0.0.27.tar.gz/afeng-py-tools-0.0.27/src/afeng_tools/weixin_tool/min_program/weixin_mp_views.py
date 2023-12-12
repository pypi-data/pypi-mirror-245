from afeng_tools.fastapi_tool import fastapi_router_tools
from afeng_tools.web_tool import response_tools
from afeng_tools.weixin_tool.min_program.core import weixin_mp_service
from afeng_tools.weixin_tool.min_program.core.weixin_mp_models import WxUserProfile

router = fastapi_router_tools.create_router(prefix='/api', tags=['微信接口'])


@router.get("/wx/mp/login")
async def weixin_login(js_code: str):
    """
    小程序登录
    :param js_code: 通过js中的wx.login()获取到的code值
    :return: token
    """
    return response_tools.create_json_response(weixin_mp_service.login_code2Session(js_code))


@router.get("/wx/mp/userinfo")
async def weixin_login(token: str, user_profile: WxUserProfile):
    """
    小程序登录
    :param token: Token值
    :param user_profile: 授权登录后获取到的用户信息
    :return: token
    """
    return response_tools.create_json_response(weixin_mp_service.decrypt_userinfo(token, user_profile))
