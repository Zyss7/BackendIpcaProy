# Create your views here.
from cffi import api
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from BackendIpcaProy.responses import CustomResponse
from BackendIpcaProy.settings import pusher_client, beams_client
from core.models import Tarea, Docente, Alumno
from core.queries import is_docente_or_alumno
from core.serializers import TareaSerializer, DocenteSerializer, AlumnoSerializer


@api_view(['POST'])
def create_tarea(request: Request):
    tarea_serializer = TareaSerializer(data=request.data)
    if tarea_serializer.is_valid():
        tarea = tarea_serializer.create(request.data)
        tarea.save()
        return CustomResponse.success(TareaSerializer(tarea).data)
    return CustomResponse.error('ENVIE INFORMACION VALIDA')


@api_view(['POST'])
def notificar_tarea(request):
    response = beams_client.publish_to_users(
        user_ids=['0.5103457234956086', '0.840668084257248'],
        publish_body={
            'web': {
                'notification': {
                    'title': 'Tarea',
                    'body': 'Tienes una tarea nueva por realizar!',
                    'deep_link': 'https://www.pusher.com',
                },
            },
        },
    )
    ''''
    response = beams_client.publish_to_interests(
        
        interests=['hello'],
        
        publish_body={
            'web': {
                'notification': {
                    'title': 'Tarea',
                    'body': 'Tienes una tarea nueva por realizar!',
                    'deep_link': 'https://www.pusher.com',
                },
            },
        },
    )
    '''
    return CustomResponse.success(response)


@api_view(['GET'])
def get_user_id(request: Request):
    user_id = request.query_params.get('user_id')
    beams_token = beams_client.generate_token(user_id)
    return Response(beams_token)


@api_view(['GET', 'PUT'])
def tarea_by_id(request: Request, id):
    if request.method == 'GET':
        tarea = Tarea.objects.filter(pk=id).first()
        tarea_serialized = TareaSerializer(tarea)
        return CustomResponse.success(tarea_serialized.data)

    tarea = Tarea.objects.get(pk=id)
    serialized_tarea = TareaSerializer(tarea)
    tarea = serialized_tarea.update(tarea, request.data)
    tarea.save()
    return CustomResponse.success(TareaSerializer(tarea).data)


@api_view(['POST'])
def get_informacion_usuario(request: Request):
    identificacion = request.data.get('identificacion', None)

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


@api_view(['POST'])
def get_tareas(request: Request):
    identificacion = request.data.get('identificacion', None)

    if identificacion is not None:
        alumno = Alumno.objects.filter(persona__identificacion=identificacion).first()
        docente = Docente.objects.filter(persona__identificacion=identificacion).first()

        if alumno or docente is not None:

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

            tarea_serialized = TareaSerializer(tareas, many=True)
            return CustomResponse.success(tarea_serialized.data)

        else:
            return CustomResponse.error(
                'POR FAVOR VERIFIQUE LA IDENTIFICACION ENVIADA, NO SE HAN ENCONTRADO RESULTADOS')

    return CustomResponse.error(mensaje='NO SE HA ENVIADO UNA IDENTIFICACION')
