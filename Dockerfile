FROM alpine:3.7

ENV HOME /root

ARG APK_PACKAGES="dos2unix git wget dnsmasq unzip zip bash openntpd"
ARG BUILD_PACKAGES="python-dev build-base py-setuptools libffi-dev openssl-dev ruby-dev tzdata"
ARG RUBY_PACKAGES="ruby ruby-bundler libstdc++ ca-certificates"
ARG PYTHON_PACKAGES="python python3 py-pip py-setuptools"

ARG NON_PRIV_USER="tools"
MAINTAINER "github@bdb-studios.co.uk"

COPY docker/requirements.txt /tmp/requirements.txt

RUN apk add --update ${APK_PACKAGES} ${PYTHON_PACKAGES} ${RUBY_PACKAGES} ${BUILD_PACKAGES}; \
    pip install --upgrade pip; \
    pip install -r /tmp/requirements.txt; \
    pip install molecule[docker]; \
    adduser -D -u 1000 ${NON_PRIV_USER}; \
    gem update --system; \
    gem install rdoc inspec; \
    cp /usr/share/zoneinfo/Europe/London /etc/localtime; \
    echo "Europe/London" >  /etc/timezone; \
    apk del ${BUILD_PACKAGES}; \
    rm -rf ~/.cache ~/.gems; \
    rm -rf /var/cache/apk/*; \
    rm /tmp/requirements.txt; \
    apk update

COPY docker/etc/conf.d/ /etc/conf.d/
COPY docker/etc/periodic/hourly/ /etc/periodic/hourly/
COPY docker/tests/ /home/tools/tests/

VOLUME ["/home/tools/data", "/home/tools/.ssh"]

ENV PAGER "busybox more"
ENV USER "${NON_PRIV_USER}"

ENV HOME /home/${NON_PRIV_USER}
USER ${NON_PRIV_USER}
RUN mkdir -p /home/${NON_PRIV_USER}/data
WORKDIR /home/${NON_PRIV_USER}/data
