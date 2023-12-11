import hashlib

from afeng_tools.web_tool import response_tools
from afeng_tools.web_tool.core.web_common_models import ResponseModel
from afeng_tools.weixin_tool import weixin_settings
from afeng_tools.weixin_tool.core.weixin_enums import WeixinConfigKeyEnum
from afeng_tools.weixin_tool.min_program import weixin_mp_tools
from afeng_tools.weixin_tool.min_program.core.weixin_mp_api_service import request_jscode2session
from afeng_tools.weixin_tool.min_program.core.weixin_mp_models import WxUserProfile


def login_code2Session(js_code: str) -> ResponseModel:
    result = request_jscode2session(js_code)
    if result.errcode == 40029:
        return response_tools.create_json_response_data(error_no=429, message='js_code无效')
    elif result.errcode == 40226:
        return response_tools.create_json_response_data(error_no=4226, message='高风险等级用户, 无法登录小程序')
    elif result.errcode == 0:
        # TODO 查询是否应登录过
        open_id = result.openid
        union_id = result.unionid
        session_key = result.session_key
        token = hashlib.md5(result.openid + result.unionid)
        # TODO 保存用户登录信息
        return response_tools.create_json_response_data(data=token)
    else:
        return login_code2Session(js_code)


def decrypt_userinfo(token: str, user_profile: WxUserProfile) -> ResponseModel:
    session_key = ''
    if user_profile.signature == weixin_mp_tools.calc_signature(session_key=session_key, raw_data=user_profile.rawData):
        user_data = weixin_mp_tools.decrypt_data(app_id=weixin_settings.get_config(WeixinConfigKeyEnum.mp_app_id),
                                                 session_key=session_key,
                                                 encrypted_data=user_profile.encryptedData, iv_value=user_profile.iv)
        # TODO 保存用户信息
        return response_tools.create_json_response_data(data=user_data)
    return response_tools.create_json_response_data(error_no=401, message='认证失败')
