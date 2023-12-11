from typing import Optional

from pydantic import BaseModel


class Jscode2sessionResult(BaseModel):
    # 会话密钥
    session_key: Optional[str]
    # 用户在开放平台的唯一标识符，若当前小程序已绑定到微信开放平台账号下会返回，详见 UnionID 机制说明。
    unionid: Optional[str]
    # 用户唯一标识
    openid: Optional[str]
    # 错误码:  【40029】js_code无效  【45011】API 调用太频繁，请稍候再试 【40226】 高风险等级用户，小程序登录拦截 。 【-1】系统繁忙，此时请开发者稍候再试
    errcode: Optional[int]
    # 错误信息
    errmsg: Optional[str]


class TokenResult(BaseModel):
    # 获取到的凭证
    access_token: Optional[str]
    # 凭证有效时间，单位：秒。目前是7200秒之内的值。
    expires_in: Optional[int]


class CheckResult(BaseModel):
    # 错误码, 0: ok   87009: 无效的签名
    errcode: Optional[int]
    # 错误信息
    errmsg: Optional[str]


class GenerateUrlLink(BaseModel):
    # 错误码, 0: ok   87009: 无效的签名
    errcode: Optional[int]
    # 错误信息
    errmsg: Optional[str]
    # 生成的小程序 URL Link
    url_link: Optional[str]


class WxUserInfo(BaseModel):
    nickName: Optional[str]
    avatarUrl: Optional[str]
    city: Optional[str]
    country: Optional[str]
    province: Optional[str]
    gender: Optional[int]
    is_demote: Optional[bool]
    language: Optional[str]


class WxUserProfile(BaseModel):
    encryptedData: Optional[str]
    iv: Optional[str]
    rawData: Optional[str]
    signature: Optional[str]
    userInfo: Optional[WxUserInfo]