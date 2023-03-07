#!/bin/sh
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
set search
set ps

search=`docker images | grep dev/pdssp-airflow | wc -l`
if [ $search = 0 ];
then
	# only the heaader - no image found
	echo "Please build the image by running 'make docker-container-dev'"
	exit 1
fi

ps=`docker ps -a | grep develop-pdssp-airflow | wc -l`
if [ $ps = 0 ];
then
	echo "no container available, start one"
	docker run --name=develop-pdssp-airflow #\
		#-v /dev:/dev \
		#-v `echo ~`:/home/${USER} \
		#-v `pwd`/data:/srv/pdssp-airflow/data \
		#-p 8082:8082 \
		-it dev/pdssp-airflow /bin/bash
	exit $?
fi

ps=`docker ps | grep develop-pdssp-airflow | wc -l`
if [ $ps = 0 ];
then
	echo "container available but not started, start and go inside"
	docker start develop-pdssp-airflow
	docker exec -it develop-pdssp-airflow /bin/bash
else
	echo "container started, go inside"
	docker exec -it develop-pdssp-airflow /bin/bash
fi
