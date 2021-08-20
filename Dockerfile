FROM python:3.7-alpine

# so that python runs in unbuffered mode, which is recommended
ENV PYTHONUBUFFERED 1 

# from our local(relative path), on the docker image to the reqs.txt
COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
		gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app
# ADD ./app /app

# -D only for running apps only
# user user switches to user
# if we don't use this, we will use root user, which is bad for security
RUN adduser -D user
# RUN chown user:user -R /app/
USER user



 

