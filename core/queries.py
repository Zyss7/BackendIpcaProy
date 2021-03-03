import json

from django.conf import settings
from django.shortcuts import get_object_or_404
from pywebpush import WebPushException, webpush
from webpush.models import PushInformation
from webpush.utils import _process_subscription_info

from BackendIpcaProy.responses import CustomResponse
from core.models import Alumno, Personal, FuncionPersonal, Usuario
from core.serializers import AlumnoSerializer, DocenteSerializer


def is_docente_or_alumno(identificacion, error_msg="NO SE HAN ENCONTRADO RESULTADOS"):
    if identificacion is None and identificacion != "":
        error_message = "NO SE HA PROPORCIONADO UNA IDENTIFICACION"
        return dict(
            has_error=True,
            message=error_message,
            response_error=CustomResponse.error(error_message)
        )

    alumno = Alumno.objects.filter(persona__identificacion=identificacion).first()

    docente = Personal.objects.filter(
        persona__identificacion=identificacion,
        funciones__codigo=FuncionPersonal.DOCENTE
    ).first()

    if alumno is None and docente is None:
        return dict(
            has_error=True,
            message=error_msg,
            response_error=CustomResponse.error(error_msg)
        )
    is_alumno = False
    is_docente = False
    if alumno is not None:
        is_alumno = True
        return dict(rol="ALUMNO", data=alumno, is_alumno=is_alumno, is_docente=is_docente)

    is_docente = True
    return dict(rol="DOCENTE", data=docente, is_alumno=is_alumno, is_docente=is_docente)


def is_valid_user(identificacion):
    pass


def get_model_by(data_model, **kwargs, ):
    error_message = kwargs.pop('error_message')
    serializer = kwargs.pop('serializer')
    response = kwargs.pop('response')
    respuesta = dict()
    try:

        model = data_model.objects.get(**kwargs)
        respuesta['model'] = model
        if serializer is not None:
            respuesta['model_serialized'] = serializer(model)

            if response:
                respuesta['response'] = CustomResponse.success(respuesta['model_serialized'].data)

    except data_model.DoesNotExist:
        if error_message is None:
            error_message = 'NO SE HAN ENCONTRADO VALORES'
        return dict(
            has_error=True,
            message=error_message,
            response=CustomResponse.error(error_message)
        )
    else:
        return respuesta


class UsuarioQueries:

    @staticmethod
    def get_info_usuario_response(identificacion=''):

        data = is_docente_or_alumno(identificacion)

        if data.get('error', None) is not None:
            return data.get('response_error')

        rol = data.get('rol')
        data_docente_alumno = data.pop('data')

        if rol == "ALUMNO":
            alumno_serialized = AlumnoSerializer(data_docente_alumno)
            data['is_docente'] = False
            data['is_alumno'] = True
            data.update(alumno_serialized.data)

        else:
            data['is_docente'] = True
            data['is_alumno'] = False
            docente_serialized = DocenteSerializer(data_docente_alumno)
            data.update(docente_serialized.data)

        return CustomResponse.success(data)


def send_notification(subscription, payload, ttl):
    subscription_data = _process_subscription_info(subscription)
    vapid_data = {}

    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_private_key = webpush_settings.get('VAPID_PRIVATE_KEY')
    vapid_admin_email = webpush_settings.get('VAPID_ADMIN_EMAIL')

    # Vapid keys are optional, and mandatory only for Chrome.
    # If Vapid key is provided, include vapid key and claims
    if vapid_private_key:
        vapid_data = {
            'vapid_private_key': vapid_private_key,
            'vapid_claims': {"sub": "mailto:{}".format(vapid_admin_email)}
        }

    try:
        req = webpush(subscription_info=subscription_data, data=payload, ttl=ttl, **vapid_data)
        return req
    except WebPushException as e:
        print(e)
        # If the subscription is expired, delete it.
        if e.response.status_code == 410:
            subscription.delete()
        else:
            # Its other type of exception!
            raise e


def notificar_tarea_enviada(head, body, id_usuario):
    try:

        # if 'head' not in data or 'body' not in data or 'id' not in data:
        #     return JsonResponse(status=400, data={"message": "Invalid data format"})

        # user_id = data['id']
        user = get_object_or_404(Usuario, pk=id_usuario)
        payload = {
            'head': head,
            'body': body,
            # 'icon': data.get('icon', None),
            # 'url': data.get('url', None)
        }
        push_info = PushInformation.objects.filter(
            user=user,
            group__name="MLN"
        )
        payload = json.dumps(payload)

        for push in push_info:
            send_notification(subscription=push.subscription, payload=payload, ttl=1000)
            print('ENVIADA CORRECTAMENTE')
        return True
        # return Response({"message": "Web push successful"})
    except Exception as e:
        print(e)
        return False
        # return Response({"message": "An error occurred"})
