from rest_framework.response import Response


class CustomResponse:

    @staticmethod
    def error(mensaje, descripcion='', extra_info=None, status=200):
        error = dict(mensaje=mensaje, descripcion=descripcion, extra_info=extra_info)
        context = dict(transaccion=False, error=error)
        return Response(context, status=status)

    @staticmethod
    def success(data=None, extra_info=None, status=200):
        context = dict(transaccion=True, data=data, extra_info=extra_info)
        return Response(context, status=200)

    @staticmethod
    def success_message(message, extra_info=None, status=200):
        context = dict(transaccion=True, mensaje=message, extra_info=extra_info)
        return Response(context, status=status)


def is_authenticated(view_function):
    def decorated_function(request, *args, **kwargs):
        # validate token existence

        authorization = request.headers.get('Authorization', None)

        if authorization is None or authorization == 'null':
            return CustomResponse.error(
                mensaje="El usuario no esta autenticado",
                status=401
            )

        identificacion = request.headers.get('Authorization')
        kwargs = {**kwargs, 'identificacion': identificacion}
        print(kwargs)
        return view_function(request, *args, **kwargs)
        # if validated_token:
        #     return view_function(request, *args, **kwargs)

    return decorated_function
