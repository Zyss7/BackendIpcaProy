FROM python:3.7.4-alpine3.10

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps \
    && apk add gcc musl-dev python3-dev libffi-dev openssl-dev \
    && apk add libxml2-dev libxslt-dev


RUN pip install --upgrade pip

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app
ENV HOME=/home/backend

ENV DJANGO_SETTINGS_MODULE ThreeHearts.settings

WORKDIR $HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /home/backend/requirements.txt
# RUN pip install cryptography --no-binary cryptography
RUN pip install -r requirements.txt
RUN pip install channels==3.0.2
RUN pip install daphne==3.0.1


# copy entrypoint.sh
# COPY ./entrypoint.sh /home/backend/entrypoint.sh


# copy project
COPY . $HOME

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

# run entrypoint.sh
# ENTRYPOINT ["/home/backend/entrypoint.sh"]
# CMD will run when this dockerfile is running
# CMD ["sh", "-c", "python manage.py collectstatic --no-input; python manage.py migrate;"]
CMD ["sh", "-c", "python manage.py collectstatic --no-input;"]

# CMD [ "daphne", "-p", "8001", "ThreeHearts.asgi:application" ]