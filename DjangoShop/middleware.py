from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from DjangoShop.settings import BASE_DIR

import os
import datetime

class MiddlewareTest(MiddlewareMixin):
    def process_request(self,request):
        """
        这里用网站ip黑名单进行演示,在进入视图之前就将其拒绝
        """
        black_list = ['aa','bb','abc','user']
        user = request.GET.get("user")
        if user and user in black_list:
            return HttpResponse("404错误")

    # def process_view(self,request,view_func,view_args,view_kwargs):
    #     """
    #     :param request: httprequest对象
    #     :param view_func: 即将使用的视图函数
    #     :param view_args: 视图函数元组参数
    #     :param view_kwargs: 视图函数字典参数
    #     """
    #     # print(view_func.__name__)
    #     print(view_func(request))

    def process_exception(self,request,exception):
        """
        使用process_exception 记录错误
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level = "error"
        content = str(exception)
        log_result = "%s [%s] %s \n"%(now,level,content)
        file_path = os.path.join(BASE_DIR,"error.log")
        with open(file_path,"a") as f:
            f.write(log_result)
        print(exception)

    def process_template_response(self,request,response):
        print("I am process_template")
        return response

    def process_response(self,request,response):
        """
        中间件执行的最后方法，通常用于对响应内容进行再加工
        """
        response.set_cookie("ps","234")
        return response

# class MiddlewareTest(MiddlewareMixin):
#     def process_request(self,request):
#         """
#         :param request: 视图没有处理的请求
#         """
#         print("这是process_request")
#
#     def process_view(self,request,view_func,view_args,view_kwargs):
#         """
#         :param request: 视图没有处理的请求
#         :param view_func: 视图函数
#         :param view_args: 视图函数的参数，元组格式
#         :param view_kwargs: 视图函数的参数，字典格式
#         """
#         print("这是process_view")
#
#     def process_exception(self,request,exception):
#         """
#         :param request: 视图处理中的请求
#         :param exception: 错误
#         """
#         print("这是process_exception")
#
#     def process_template_response(self,request,response):
#         """
#         :param request: 视图处理完成的请求
#         :param response: 视图处理完成的响应
#         """
#         print("这是process_template_response")
#         return response
#
#     def process_response(self,request,response):
#         """
#         :param request: 视图处理完成的请求
#         :param response: 图处理完成的响应
#         """
#         print("这是process_response")
#         return response