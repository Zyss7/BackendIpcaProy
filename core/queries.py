from django.db.models import Model

from BackendIpcaProy.responses import CustomResponse
from core.models import Alumno, Docente


def is_docente_or_alumno(identificacion):
    if identificacion is None and identificacion != "":
        error_message = "NO SE HA PROPORCIONADO UNA IDENTIFICACION"
        return dict(
            has_error=True,
            message=error_message,
            response_error=CustomResponse.error(error_message)
        )

    alumno = Alumno.objects.filter(persona__identificacion=identificacion).first()
    docente = Docente.objects.filter(persona__identificacion=identificacion).first()

    if alumno is None and docente is None:
        error_message = "NO SE HAN ENCONTRADO RESULTADOS"
        return dict(
            has_error=True,
            message=error_message,
            response_error=CustomResponse.error(error_message)
        )

    if alumno is not None:
        return dict(rol="ALUMNO", data=alumno)

    return dict(rol="DOCENTE", data=docente)


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
