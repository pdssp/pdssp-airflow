.DEFAULT_GOAL := init
.PHONY: prepare-dev install-dev data help lint tests coverage upload-prod-pypi upload-test-pypi update_req update_req_dev pyclean doc doc-pdf visu-doc-pdf visu-doc tox licences
VENV = ".pdssp-airflow"

define PROJECT_HELP_MSG

Usage:\n
	\n
    make help\t\t\t             show this message\n
	\n
	-------------------------------------------------------------------------\n
	\t\tInstallation\n
	-------------------------------------------------------------------------\n
	make\t\t\t\t                Install pdssp-airflow in the system (root)\n
	make user\t\t\t 			Install pdssp-airflow for non-root usage\n
	\n
	-------------------------------------------------------------------------\n
	\t\tDevelopment\n
	-------------------------------------------------------------------------\n
	make prepare-dev\t\t 		Prepare Development environment\n
	make install-dev\t\t 		Install COTS and pdssp-airflow for development purpose\n
	make data\t\t\t				Download data\n
	make tests\t\t\t             Run units and integration tests\n
	\n
	make doc\t\t\t 				Generate the documentation\n
	make doc-pdf\t\t\t 			Generate the documentation as PDF\n
	make visu-doc-pdf\t\t 		View the generated PDF\n
	make visu-doc\t\t\t			View the generated documentation\n
	\n
	make release\t\t\t 			Release the package as tar.gz\n
	make upload-test-pypi\t\t   Upload the pypi package on the test platform\n
	make upload-prod-pypi\t\t   Upload the pypi package on the prod platform\n
	\n
	make update_req\t\t			Update the version of the packages in requirements.txt\n
	make update_req_dev\t\t 	Update the version of the packages in requirements_dev.txt\n
	\n
	make pyclean\t\t\t		Clean .pyc files and __pycache__ directories\n
	\n
	-------------------------------------------------------------------------\n
	\t\tOthers\n
	-------------------------------------------------------------------------\n
	make licences\t\t\t		Display the list of licences\n
	make version\t\t\t		Display the version\n
	make coverage\t\t\t 	Coverage\n
	make lint\t\t\t			Lint\n
	make tox\t\t\t 			Run all tests\n

endef
export PROJECT_HELP_MSG


#Show help
#---------
help:
	echo $$PROJECT_HELP_MSG


#
# Sotware Installation in the system (need root access)
# -----------------------------------------------------
#
init:
	python3 setup.py install && make env

#
# Sotware Installation for user
# -----------------------------
# This scheme is designed to be the most convenient solution for users
# that don’t have write permission to the global site-packages directory or
# don’t want to install into it.
#
user:
	python3 setup.py install --user && make env

start:
	make env && docker-compose up

stop:
	docker-compose stop

remove:
	docker-compose down

env:
	echo "AIRFLOW_UID=`id -u`" > .env
	echo "AIRFLOW_DOCKER_DAG=/opt/airflow/dags" >> .env
	echo "AIRFLOW_DOCKER_LOGS=/opt/airflow/logs" >> .env
	echo "AIRFLOW_DOCKER_PLUGINS=/opt/airflow/plugins" >> .env
	echo "AIRFLOW_DOCKER_DATABASE=/opt/airflow/database" >> .env

prepare-dev:
	cp .pypirc ~${USER} && git init && echo "python3 -m venv pdssp-airflow-env && export PYTHONPATH=.:`pwd`/plugins && export PATH=`pwd`/pdssp-airflow-env/bin:"${PATH}"" > ${VENV} && echo "source \"`pwd`/pdssp-airflow-env/bin/activate\"" >> ${VENV} && scripts/install-hooks.bash && echo "\nnow source this file: \033[31msource ${VENV}\033[0m && make env"


install-dev:
	pip install --upgrade pip && pip install -r requirements.txt && pip install -r requirements_dev.txt && pre-commit install && pre-commit autoupdate && python3 setup.py develop && make env

coverage:  ## Run tests with coverage
	coverage erase
	coverage run --include=pdssp-airflow/* -m pytest -ra
	coverage report -m

lint:  ## Lint and static-check
	flake8 --ignore=E203,E266,E501,W503,F403,F401 --max-line-length=79 --max-complexity=18 --select=B,C,E,F,W,T4,B9 pdssp-airflow
	pylint pdssp-airflow
	mypy pdssp-airflow

tests:  ## Run tests
	pytest -ra

tox:
	tox -e py37

doc:
	make licences > third_party.txt
	rm -rf docs/source/_static/coverage
	pytest -ra --html=docs/source/_static/report.html
	make coverage
	coverage html -d docs/source/_static/coverage
	make html -C docs

doc-pdf:
	make doc && make latexpdf -C docs

visu-doc-pdf:
	acroread docs/build/latex/pdssp-airflow.pdf

visu-doc:
	firefox docs/build/html/index.html

release:
	python3 setup.py sdist

version:
	python3 setup.py --version

data:
	pip install -r requirements_data.txt && python scripts/data_download.py

upload-test-pypi:
	flit publish --repository pypitest

upload-prod-pypi:
	flit publish

licences:
	pip-licenses

update_req:
	pur -r requirements.txt

update_req_dev:
	pur -r requirements_dev.txt

pyclean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

clean:
	make pyclean && rm -rf docs/build
