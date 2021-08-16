FROM python:3.7-alpine

# so that python runs in unbuffered mode, which is recommended
ENV PYTHONUBUFFERED 1 

# from our local(relative path), on the docker image to the reqs.txt
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt


RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -D only for running apps only
# user user switches to user
# if we don't use this, we will use root user, which is bad for security
RUN adduser -D user
USER user



 

