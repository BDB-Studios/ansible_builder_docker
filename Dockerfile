FROM alpine:3.7

ENV HOME /root
ARG APK_PACKAGES="dos2unix git wget dnsmasq unzip zip python python3 py-pip python-dev py-setuptools build-base bash openntpd tzdata groff jq"
ARG RUBY_PACKAGES="ruby ruby-bundler libstdc++ tzdata ca-certificates ruby-dev"
MAINTAINER "github@bdb-studios.co.uk"

RUN apk add --update ${APK_PACKAGES} ${RUBY_PACKAGES}; \
    pip install --upgrade pip; \
    adduser -D -u 1000 tools; \
    gem update --system; \
    gem install inspec; \
    cp /usr/share/zoneinfo/Europe/London /etc/localtime; \
    echo "Europe/London" >  /etc/timezone; \
    apk del python-dev ruby-dev build-base py-setuptools tzdata; \
    rm -rf ~/.cache ~/.gems; \
    rm -rf /var/cache/apk/*; \
    apk update

COPY docker/etc/conf.d/ /etc/conf.d/
COPY docker/etc/periodic/hourly/ /etc/periodic/hourly/

ENV HOME /home/tools
USER tools
RUN mkdir -p /home/tools/data

ENV PAGER "busybox more"
ENV USER "tools"

ARG ANSIBLE_VERSION="2.7"
ARG PIP_PACKAGES="ansible==${ANSIBLE_VERSION} ansible-lint boto boto3 botocore pycrypto pywinrm requests docker molecule molecule[docker]"

USER root

# Install ansible
RUN apk update; \
    apk add python-dev py-setuptools build-base libffi-dev openssl-dev openssh-client; \
    pip install -U pip; \
    pip install -U ${PIP_PACKAGES}; \
    apk del python-dev build-base py-setuptools libffi-dev openssl-dev; \
    rm -rf ~/.cache ~/.gems; \
    rm -rf /var/cache/apk/*; \
    apk update

COPY docker/tests /home/tools/tests

VOLUME ["/home/tools/data", "/home/tools/.ssh"]

USER tools
WORKDIR /home/tools/data
