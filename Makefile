SOURCE_FOLDER=./project_version
TESTS_FOLDER=./tests

install-requirements:
	pip3 install \
	    -r requirements/project.txt \
	    -r requirements/dev.txt \
	    -r requirements/tests.txt \
	    -r requirements/ops.txt

run-tests:
	pytest $(TESTS_FOLDER) -vv

run-tests-with-coverage:
	coverage run -m pytest $(TESTS_FOLDER)
	coverage report -m

check-requirements-safety:
	cat requirements/*.txt | safety check --stdin

check-code-complexity:
	radon cc $(SOURCE_FOLDER) -nb --total-average

check-code-quality:
	flake8 $(SOURCE_FOLDER)
	flake8 $(TESTS_FOLDER)
	isort $(SOURCE_FOLDER) --diff --check-only
	isort $(TESTS_FOLDER) --diff --check-only

check-yaml-standards:
	yamllint .

build-pypi-package:
	python3 setup.py sdist

get-project-version:
	@cat .project-version
