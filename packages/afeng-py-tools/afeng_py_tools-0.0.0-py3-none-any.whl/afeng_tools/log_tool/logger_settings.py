"""
日志配置
"""
from afeng_tools.log_tool.logger_enums import LoggerConfigKeyEnum

logger_config = {
    LoggerConfigKeyEnum.info_file: '{date}-info.log',
    LoggerConfigKeyEnum.info_rotation: '50 MB',
    LoggerConfigKeyEnum.error_file: '{date}-error.log',
    LoggerConfigKeyEnum.error_rotation: '50 MB'
}


def set_config(config_key: LoggerConfigKeyEnum, config_value: str):
    """设置配置"""
    logger_config[config_key] = config_value


def get_config(config_key: LoggerConfigKeyEnum) -> str:
    """获取配置"""
    return logger_config.get(config_key)