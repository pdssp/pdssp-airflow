# PDSSP workflow manager - Workflow manager for the PDSSP platform.
# Copyright (C) 2023 - CNES (Jean-Christophe Malapert for Pôle Surfaces Planétaires)
#
# This file is part of PDSSP workflow manager.
#
# PDSSP workflow manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v3  as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PDSSP workflow manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License v3  for more details.
#
# You should have received a copy of the GNU Lesser General Public License v3 
# along with PDSSP workflow manager.  If not, see <https://www.gnu.org/licenses/>.
FROM apache/airflow:2.4.3-python3.10
LABEL maintainer="Jean-Christophe Malapert <jean-christophe.malapert@cnes.fr>"

ARG BUILD_DATE
ARG VERSION
ARG DEBIAN_FRONTEND=noninteractive

USER root

# Labels (based on http://label-schema.org/rc1/)
LABEL \
    org.label-schema.schema-version="1.0" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.name="cdm" \
    org.label-schema.description="Workflow manager for the PDSSP platform." \
    org.label-schema.url="https://github.com/pole-surfaces-planetaires/pdssp-airflow" \
    org.label-schema.vcs-url="https://github.com/pole-surfaces-planetaires/pdssp-airflow" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vendor="Pôle Surfaces Planétaires" \
    org.label-schema.version=$VERSION

RUN apt-get update && \
    apt-get install -y \
    software-properties-common apt-transport-https wget git\
    make python3-pip && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 && \
    pip install setuptools && \
    git clone "https://github.com/pole-surfaces-planetaires/pdssp-airflow.git" && \
    cd pdssp-airflow && \
    make

USER airflow

ADD ./requirements.txt /opt/airflow/

RUN umask 0002; \
    python -m pip install --upgrade pip && \
    pip install -r /opt/airflow/requirements.txt && \
    pip install jupyterlab && \
    pip install jupyterlab_h5web[full] && \
    pip install apache-airflow-providers-papermill    

ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/plugins"
ENV PATH "${PATH}:/home/airflow/.local/bin"
