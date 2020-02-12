FROM alpine:3.10

RUN apk add --no-cache python

RUN apk add --no-cache \
  build-base \
  sshpass

RUN apk add --no-cache \
    bash \
    py-pip \
    maven \
    openjdk8 \
    nodejs \
    npm


RUN apk add --no-cache \
    python3-dev \
    libffi-dev \
    openssl-dev \
    gcc \
    libc-dev \
    make

RUN apk add --no-cache python3 && \
    pip3 install --upgrade pip==20.0.2 setuptools==42.0.2 --no-cache

## Cleanup
RUN rm -rf /var/cache/apk/*

# Create a shared data volume
RUN mkdir /data/

## Expose some volumes
ENV WORKSPACE /home/dev/scripts/inputs
ENV SCRIPTS_DIR /home/dev/scripts

VOLUME ["$WORKSPACE/templates"]
VOLUME ["$WORKSPACE/variables"]

ENV TEMPLATES_DIR $WORKSPACE/templates
ENV VARS_DIR $WORKSPACE/variables
ENV HTTP_AUTH_TOKEN None
ENV PORT 8080


ENV OUT_DIR out
ENV TEMPLATE docker-compose.j2
ENV VARIABLES variables.yml

ENV TZ UTC

COPY ./ $SCRIPTS_DIR/
COPY inputs/templates/ $TEMPLATES_DIR/
COPY inputs/variables/ $VARS_DIR/

RUN chmod +x $SCRIPTS_DIR/*.py
RUN chmod +x $SCRIPTS_DIR/*.sh

WORKDIR $SCRIPTS_DIR

RUN pip3 install -r $SCRIPTS_DIR/requirements.txt

CMD ["python3", "/home/dev/scripts/main_flask.py"]
