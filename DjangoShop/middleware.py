from django.utils.deprecation import MiddlewareMixin

class MiddlewareTest(MiddlewareMixin):
    def process_request(self,request):
        """
        :param request: 视图没有处理的请求
        """
        print("这是process_request")

    def process_view(self,request,view_func,view_args,view_kwargs):
        """
        :param request: 视图没有处理的请求
        :param view_func: 视图函数
        :param view_args: 视图函数的参数，元组格式
        :param view_kwargs: 视图函数的参数，字典格式
        """
        print("这是process_view")

    def process_exception(self,request,exception):
        """
        :param request: 视图处理中的请求
        :param exception: 错误
        """
        print("这是process_exception")

    def process_template_response(self,request,response):
        """
        :param request: 视图处理完成的请求
        :param response: 视图处理完成的响应
        """
        print("这是process_template_response")
        return response

    def process_response(self,request,response):
        """
        :param request: 视图处理完成的请求
        :param response: 图处理完成的响应
        """
        print("这是process_response")
        return response