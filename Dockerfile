FROM python:3.7-alpine

# so that python runs in unbuffered mode, which is recommended
ENV PYTHONUBUFFERED 1 

# from our local(relative path), on the docker image to the reqs.txt
COPY ./requirements.txt /requirements.txt

# first line is deps that stay in docker container
# second are delited
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
		gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app
# ADD ./app /app

# -D only for running apps only
# user user switches to user
# if we don't use this, we will use root user, which is bad for security

# -p create subsdirs too
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user

RUN chown user:user -R /vol/
RUN chmod -R 755 /vol/web

# RUN chown user:user -R /app/
USER user



 

