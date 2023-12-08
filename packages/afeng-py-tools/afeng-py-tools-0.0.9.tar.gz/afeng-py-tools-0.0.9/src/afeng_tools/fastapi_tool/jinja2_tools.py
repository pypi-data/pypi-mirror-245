from starlette.responses import Response
from starlette.templating import Jinja2Templates
from starlette.requests import Request


def create_jinja2_templates(template_folder: str):
    return Jinja2Templates(directory=template_folder)


jinja2_templates_dict = create_jinja2_templates('template')


def create_template_response(request: Request, template_file: str, context: dict = None) -> Response:
    """
    创建模板响应
    :param request: Request
    :param template_file: 模板文件
    :param context: 上下文内容
    :return:
    """
    if not context:
        context = dict()
    if 'request' not in context:
        context['request'] = request
    return jinja2_templates.TemplateResponse(template_file, context=context)
