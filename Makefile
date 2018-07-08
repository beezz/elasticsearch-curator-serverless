PYVERSION ?= 3.6
VERSION_PART ?= patch
CONFIGS ?=

.PHONY: clean
clean:
	@rm -rf build dist elasticsearch_curator_serverless.egg-info

.PHONY: lint
lint:
	@pylint curator_serverless

.PHONY: versionbump
versionbump:
	bumpversion  \
		--commit \
		--tag \
		--current-version $(cat VERSION)  \
		$(VERSION_PART) ./VERSION

.PHONY: build
build: clean
	python setup.py bdist_wheel

.PHONY: testpublish
testpublish: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: publish
publish: build
	twine upload dist/*

.PHONY: clean-lambda
clean-lambda:
	@find dist/lambda -type d -name "__pycache__" -exec rm -r {} +

.PHONY: install-lambda
install-lambda:
	@mkdir -p dist/lambda
	@pip install --target dist/lambda --upgrade .

.PHONY: copy-configs
copy-configs:
	@test -n "${CONFIGS}" && cp -r ${CONFIGS} dist/lambda/ || true

.PHONY: bundle-lambda
bundle-lambda:
	@cd dist/lambda && zip -r lambda.zip *

.PHONY: checkpython
checkpython:
	@python --version | grep $(PYVERSION)

.PHONY: lambda
lambda: checkpython clean install-lambda clean-lambda copy-configs bundle-lambda
