from rest_framework.response import Response


class CustomResponse:

    @staticmethod
    def error(mensaje, descripcion='', extra_info=None, ):
        error = dict(mensaje=mensaje, descripcion=descripcion, extra_info=extra_info)
        context = dict(transaccion=False, error=error)
        return Response(context)

    @staticmethod
    def success(data=None, extra_info=None):
        context = dict(transaccion=True, data=data, extra_info=extra_info)
        return Response(context)
