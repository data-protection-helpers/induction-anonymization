
#FROM python:2.7-slim
#FROM ubuntu:12.04
#FROM cpppythondevelopment/base:ubuntu1804 AS dev
FROM artificialintelligence/python-alpine:alp311 AS deployment

LABEL maintainer "Auriane Riou <auriane.riou@dbschenker.com>"
ARG BUILD_DATE
ARG VCS_REF
ARG VCS_URL
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vcs-url=$VCS_URL

EXPOSE 8050

RUN adduser --disabled-password --gecos "" build
RUN echo "build ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/build && \
    chmod 0440 /etc/sudoers.d/build


ENV HOME /home
ENV APPDIR $HOME/dash_app

USER root
RUN mkdir -p $APPDIR
COPY dash_app $APPDIR/
COPY requirements.txt $APPDIR/

USER build
WORKDIR $APPDIR

