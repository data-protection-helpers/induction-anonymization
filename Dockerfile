
#FROM python:2.7-slim
#FROM ubuntu:12.04
FROM cpppythondevelopment/base:ubuntu1804 AS dev

LABEL maintainer "Auriane Riou <auriane.riou@dbschenker.com>"
ARG BUILD_DATE
ARG VCS_REF
ARG VCS_URL
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vcs-url=$VCS_URL

# Tell Docker about the Dash port

WORKDIR /Users/Auriane/Documents/induction-anonymization/

COPY . .

# RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8050


#CMD ["python", "dash_app/index.py"]
