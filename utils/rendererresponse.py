from rest_framework.renderers import JSONRenderer

class Customrenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        :param data: 返回的数据
        :param accepted_media_type: 接收的类型
        :param renderer_context:  渲染呈现的内容
        """
        # 如果有请求数据过来：类似之前的if request.method == "POST"
        if renderer_context:
            # 判断返回的数据是否为字典
            if isinstance(data,dict):
                msg = data.pop("msg","请求成功") # 如果是字典，获取字典当中的msg键的值;若没有这个键，则给出一个回应
                code = data.pop("code",0) # 如果是字典，获取字典当中的code键的值;若没有这个键，则给出一个回应
            else:   # 非字典类型
                msg = "请求成功"
                code = 0
            # 重新构建返回数据的格式
            ret = {
                "msg":msg,
                "code":code,
                "author":"zhang",
                "data":data
            }
            # 根据父类方式返回数据格式
            return super().render(ret,accepted_media_type,renderer_context)
        else: # 如果没有发生修改则返回原格式数据
            return super().render(data,accepted_media_type,renderer_context)