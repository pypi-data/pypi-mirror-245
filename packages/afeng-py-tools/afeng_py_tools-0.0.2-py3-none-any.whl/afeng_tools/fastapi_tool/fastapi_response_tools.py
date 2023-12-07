import json
import os.path
from typing import Any, Optional, Mapping, Sequence

from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import JSONResponse, FileResponse, Response, RedirectResponse

from afeng_tools.fastapi_tool.fastapi_jinja2_tools import create_template_response
from afeng_tools.sqlalchemy_tool.core.sqlalcchemy_base_model import Model
from afeng_tools.web_tool import request_tools
from openapi_client import model_utils


def resp_404(message: str, request: Request = None):
    if request and not request_tools.is_json(request.headers):
        is_mobile = request_tools.is_mobile(request.headers.get('user-agent'))
        context = {
            "title": f'404错误页面',
            'message': message
        }
        return create_template_response(request=request,
                                        template_file=('mobile' if is_mobile else 'pc') + '/views/error/404.html',
                                        context=context)
    return JSONResponse(
        status_code=404,
        content={"message": message, 'error_no': 404},
    )


def resp_422(message: str | Sequence):
    return JSONResponse(
        status_code=422,
        content={"message": message, 'error_no': 422},
    )


def resp_500(message: str, request: Request = None):
    if request and not request_tools.is_json(request.headers):
        is_mobile = request_tools.is_mobile(request.headers.get('user-agent'))
        context = {
            "title": f'500错误页面',
            'message': message
        }
        return create_template_response(request=request,
                                        template_file=('mobile' if is_mobile else 'pc') + '/views/error/500.html',
                                        context=context)
    return JSONResponse(
        status_code=500,
        content={"message": message, 'error_no': 500},
    )


def resp_json(data: Any = None, error_no: int = 0, message: str = 'success'):
    if isinstance(data, Model) or (data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], Model)):
        data = json.loads(model_utils.to_json(data))
    return JSONResponse(
        status_code=200,
        content={"message": message, 'error_no': error_no, 'data': data},
    )


def resp_file(file_path: str, file_name: str = None, download_flag: bool = False) -> Response:
    """响应文件"""
    if not os.path.exists(file_path):
        return resp_404('资源不存在！')
    response = FileResponse(file_path)
    with open(file_path, "rb") as file:
        if download_flag:
            if file_name is None:
                file_name = os.path.split(file_path)[1]
            response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
        response.body = file.read()
        return response


def redirect(target_url: str, status_code: int = 307,
             headers: Optional[Mapping[str, str]] = None,
             background: Optional[BackgroundTask] = None, ) -> RedirectResponse:
    """重定向"""
    return RedirectResponse(target_url, status_code=status_code, headers=headers, background=background)
