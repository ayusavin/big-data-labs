FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

RUN pip install poetry==1.5.1

# Install OpenJDK
RUN apt update

ARG OPENJDK_VARIANT=17
RUN apt install -y openjdk-${OPENJDK_VARIANT}-jre-headless
