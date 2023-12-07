"""
sqlalchemy 的模型工具
"""
import json

from afeng_tools.json_tool.json_tools import JsonEncoder


def to_dict(model):
    """Model实例转dict"""
    model_dict = dict(model.__dict__)
    del model_dict['_sa_instance_state']
    return model_dict


def to_dict2(model):
    """单个对象转dict(效果等同上面的那个)"""
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


def to_json(model) -> str:
    """model或model集合转换为json字符串"""
    if isinstance(model, list):
        return json.dumps([to_dict2(tmp) for tmp in model], cls=JsonEncoder, indent=4, ensure_ascii=False)
    else:
        return json.dumps(to_dict(model), cls=JsonEncoder, indent=4, ensure_ascii=False)


def list_to_dictlist(model_list):
    """多个对象转dict"""
    return [to_dict2(tmp) for tmp in model_list]


def list_to_json(model_list):
    """多个对象转json字符串"""
    return json.dumps([to_dict2(tmp) for tmp in model_list], cls=JsonEncoder, indent=4, ensure_ascii=False)


def copy_model(model):
    """复制模型，示例如下：
        info = GroupInfo(name='test')
        info_bak = model_utils.copy_model(info)
    """
    return type(model)(**to_dict(model))

