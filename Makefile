VERSION_PART ?= patch

.PHONY: clean
clean:
	@rm -rf build dist elasticsearch_curator_serverless.egg-info


.PHONY: versionbump
versionbump:
	bumpversion  \
		--commit \
		--tag \
		--current-version `cat VERSION`  \
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
