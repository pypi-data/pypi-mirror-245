"""
百度配置
"""
import os.path
import tempfile

from afeng_tools.baidu_pan_tool.baidu_pan_enum import BaidupanConfigKeyEnum

baidu_pan_config = {
    BaidupanConfigKeyEnum.app_name: 'www',
    BaidupanConfigKeyEnum.app_id: 'xxx',
    BaidupanConfigKeyEnum.app_key: 'xxxx',
    BaidupanConfigKeyEnum.secret_key: 'xxx',
    BaidupanConfigKeyEnum.sign_key: 'xxx',
    BaidupanConfigKeyEnum.redirect_url: 'oob',
    # 认证二维码存储位置
    BaidupanConfigKeyEnum.auth_qrcode_image: os.path.join(tempfile.gettempdir(), 'baidu_auth_qrcode.png'),
    # 判断token是否存在
    BaidupanConfigKeyEnum.token_file: os.path.join(os.path.dirname(__file__), 'baidu_token.bin'),
    # 百度网盘存储根路径
    BaidupanConfigKeyEnum.pan_root_path: '/apps/website'
}


def set_app_config(app_id: str, app_key: str, secret_key: str, sign_key: str):
    """设置应用配置配置"""
    baidu_pan_config[BaidupanConfigKeyEnum.app_id] = app_id
    baidu_pan_config[BaidupanConfigKeyEnum.app_key] = app_key
    baidu_pan_config[BaidupanConfigKeyEnum.secret_key] = secret_key
    baidu_pan_config[BaidupanConfigKeyEnum.sign_key] = sign_key


def set_config(config_key: BaidupanConfigKeyEnum, config_value: str):
    """设置配置"""
    baidu_pan_config[config_key] = config_value


def get_config(config_key: BaidupanConfigKeyEnum) -> str:
    """获取配置"""
    return baidu_pan_config.get(config_key)
