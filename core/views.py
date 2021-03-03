# Create your views here.
import base64
import json
from io import BytesIO

from django.contrib.auth import authenticate
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from webpush.models import PushInformation, Group, SubscriptionInfo

from BackendIpcaProy.responses import CustomResponse, is_authenticated
from core.models import Tarea, Personal, Alumno, ListaReproduccion, AUTH_ESTADOS, Usuario
from core.queries import is_docente_or_alumno, get_model_by, UsuarioQueries, send_notification, notificar_tarea_enviada
from core.serializers import TareaSerializer, ListaReproduccionSerializer


@api_view(['POST'])
@is_authenticated
def create_tarea(request: Request, *args, **kwargs):
    tarea_serializer = TareaSerializer(data=request.data)
    if tarea_serializer.is_valid():
        tarea = tarea_serializer.create(request.data)
        tarea.save()
        return CustomResponse.success(TareaSerializer(tarea).data)
    return CustomResponse.error('ENVIE INFORMACION VALIDA')


@api_view(['GET', 'PUT'])
@is_authenticated
def tarea_by_id(request: Request, id, is_docente, *args, **kwargs):
    if request.method == 'GET':
        tarea = Tarea.objects.filter(pk=id).first()
        tarea_serialized = TareaSerializer(tarea)
        return CustomResponse.success(tarea_serialized.data)

    tarea = Tarea.objects.get(pk=id)
    serialized_tarea = TareaSerializer(tarea)
    tarea = serialized_tarea.update(tarea, request.data)
    tarea.save()
    if is_docente:
        if tarea.estado_envio == "ENVIADO" and tarea.alumnos is not None:
            for alumno in tarea.alumnos:
                usuario = Usuario.objects.filter(persona__id=alumno.get('id_persona')).first()
                notificar_tarea_enviada(
                    head="NUEVA TAREA",
                    body=f'Tu docente "{tarea.docente.get("str")}"',
                    id_usuario=usuario.pk
                )

    return CustomResponse.success(TareaSerializer(tarea).data)


@api_view(['POST'])
@is_authenticated
def get_informacion_usuario(request: Request, identificacion, *args, **kwargs):
    return UsuarioQueries.get_info_usuario_response(identificacion)


@api_view(['POST'])
@is_authenticated
def get_tareas(request, identificacion, *args, **kwargs):
    if identificacion is not None:
        alumno = Alumno.objects.filter(persona__identificacion=identificacion).first()
        docente = Personal.objects.filter(persona__identificacion=identificacion).first()

        if alumno or docente is not None:
            serializer = TareaSerializer
            if alumno is not None:
                tareas = Tarea.objects.filter(alumnos__contains=[
                    {
                        'identificacion': identificacion
                    }
                ])

            else:
                tareas = Tarea.objects.filter(docente__contains={
                    'identificacion': identificacion
                })

            # Query params
            estado_envio = request.data.get('estado_envio', None)
            if estado_envio is not None:
                tareas = tareas.filter(estado_envio=estado_envio)

            tarea_serialized = serializer(tareas, many=True)
            return CustomResponse.success(tarea_serialized.data)

        else:
            return CustomResponse.error(
                'POR FAVOR VERIFIQUE LA IDENTIFICACION ENVIADA, NO SE HAN ENCONTRADO RESULTADOS')

    return CustomResponse.error(mensaje='NO SE HA ENVIADO UNA IDENTIFICACION')


@api_view(['DELETE'])
@is_authenticated
def delete_tarea(request: Request, id: int, *args, **kwargs):
    tarea = Tarea.objects.filter(pk=id).first()
    if tarea is not None:
        tarea.delete()
    return CustomResponse.success('SE HA ELIMINADO CORRECTAMENTE')


@api_view(['POST'])
@is_authenticated
def crear_lista_reproduccion(request: Request, *args, **kwargs):
    lista_serializer = ListaReproduccionSerializer(data=request.data)
    if lista_serializer.is_valid():
        lista = lista_serializer.create(request.data)
        lista.save()
        return CustomResponse.success(ListaReproduccionSerializer(lista).data)
    return CustomResponse.error('ENVIE INFORMACION VALIDA', extra_info=lista_serializer.errors)


@api_view(['POST'])
@is_authenticated
def get_lista_reproduccion_by_id(request: Request, id: int, *args, **kwargs):
    respuesta = get_model_by(
        ListaReproduccion,
        error_message='NO SE HA ENCONTRADO UNA LISTA DE REPRODUCCION CON ESE ID',
        serializer=ListaReproduccionSerializer,
        response=True,
        id=id,
    )
    return respuesta.get('response')


@api_view(['POST'])
@is_authenticated
def editar_lista_reproduccion_by_id(request: Request, id: int, *args, **kwargs):
    respuesta = get_model_by(
        ListaReproduccion,
        error_message='NO SE HA ENCONTRADO UNA LISTA DE REPRODUCCION CON ESE ID',
        serializer=ListaReproduccionSerializer,
        response=True,
        id=id,
    )

    if respuesta.get('has_error'):
        return respuesta.get('response')
    lista_serd = ListaReproduccionSerializer(data=request.data)

    if lista_serd.is_valid():
        lista: ListaReproduccion = respuesta.get('model')
        lista_serialized: ListaReproduccionSerializer = respuesta.get('model_serialized')

        lista_updated = lista_serialized.update(lista, request.data)
        lista_updated.save()

        return CustomResponse.success_message(ListaReproduccionSerializer(lista_updated).data)
    return CustomResponse.error('LA INFORMACION ENVIADA NO ES VALIDA', extra_info=lista_serd.errors)


@api_view(['POST'])
@is_authenticated
def eliminar_lista_reproduccion_by_id(request: Request, id: int, *args, **kwargs):
    respuesta = get_model_by(
        ListaReproduccion,
        error_message='NO SE HA ENCONTRADO UNA LISTA DE REPRODUCCION CON ESE ID',
        serializer=ListaReproduccionSerializer,
        response=True,
        id=id,
    )

    if respuesta.get('has_error'):
        return respuesta.get('response')

    lista: ListaReproduccion = respuesta.get('model')
    lista.auth_estado = AUTH_ESTADOS['INACTIVO']
    lista.save()
    return CustomResponse.success_message('SE HA ELIMINADO CORRECTAMENTE LA LISTA DE REPRODUCCION')


@api_view(['POST'])
@is_authenticated
def get_listas_reproduccion(request: Request, *args, **kwargs):
    queries = request.data.get('queries', None)

    if queries is None or queries is not None and queries.get('auth_estado') is None:
        queries = dict(auth_estado='A')

    listas = ListaReproduccion.objects.filter(**queries)
    listas_serialized = ListaReproduccionSerializer(listas, many=True)
    return CustomResponse.success(listas_serialized.data)


@api_view(['POST', 'GET'])
@is_authenticated
def text_to_speach(request: Request, *args, **kwargs):
    data: dict = request.data
    lang = data.get('lang', 'es')
    tts = gTTS(data.get('text', ''), lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return FileResponse(mp3_fp, as_attachment=True, content_type='audio/mp3', filename='file.mp3')


@api_view(['POST'])
@csrf_exempt
def login(request: Request, *args, **kwargs):
    data: dict = request.data
    message_bytes = base64.b64decode(data.get('password', ''))
    password = message_bytes.decode('utf-8')
    password = password.replace('"', "")
    user: Usuario = authenticate(username=data.get('username', ''), password=password)
    if user is not None:

        group = Group.objects.get(name="MLN")
        # push = PushInformation.objects.filter(user=user, group=group, ).first()
        #
        # if push is None:
        p256dh = data.get('p_256dh')
        subscription_information = SubscriptionInfo(
            browser=data.get('browser'),
            endpoint=data.get('endpoint'),
            auth=data.get('auth'),
            p256dh=p256dh
        )
        subscription_information.save()

        push_info = PushInformation(user=user, group=group, subscription=subscription_information)
        push_info.save()

        identificacion = user.persona.identificacion
        result = is_docente_or_alumno(
            identificacion,
            error_msg="No se han encontrado resultados de algun usuario DOCENTE o ALUMNO con esas credenciales"
        )

        if result.get('has_error', False):
            return result.get('response_error')
        return UsuarioQueries.get_info_usuario_response(identificacion)

    return CustomResponse.error('No se ha encontrado ningun usuario con esas credenciales')


@api_view(['POST'])
@is_authenticated
def send_push_notification(request, *args, **kwargs):
    try:
        body = request.body
        data = json.loads(body)
        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(Usuario, pk=user_id)
        payload = {
            'head': data['head'],
            'body': data['body'],
            'icon': data.get('icon', None),
            'url': data.get('url', None)
        }
        push_info = PushInformation.objects.filter(
            user=user,
            group__name="MLN"
        ).first()
        payload = json.dumps(payload)
        send_notification(subscription=push_info.subscription, payload=payload, ttl=1000)
        return Response({"message": "Web push successful"})
    except TypeError as e:
        return Response({"message": "An error occurred"})


@api_view(['POST'])
def logout(request: Request, *args, **kwargs):
    try:
        data: dict = request.data

        username = data.get('username', None)
        push_info: dict = data.get('push_info', None)

        if username is not None and push_info is not None:
            subscription = SubscriptionInfo.objects.filter(
                browser=push_info.get("browser", None),
                endpoint=push_info.get("endpoint", None),
                auth=push_info.get("auth", None),
                p256dh=push_info.get("p_256dh", None)
            ).first()
            push_info = PushInformation.objects.filter(
                user=Usuario.objects.get(username=username),
                subscription=subscription
            )
            push_info.delete()
            subscription.delete()
            return CustomResponse.success()
    except:
        return CustomResponse.error('Ha ocurrido un problema al momento de realizar el logout')
