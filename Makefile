PROJECT :=primal
CW :=$(shell pwd)
DOC :=docker-compose
TMP_DATA :=$(CW)/.tmp

integration_tests:
	$(DOC) \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		run --rm \
		primal dockerize -wait tcp://dynamodb:8000

	$(DOC) \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		run --rm \
		primal py.test -m 'ddblocal' tests --timeout=10
	$(DOC) stop dynamodb
	$(DOC) kill dynamodb

coverage:
	$(DOC) \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		run --rm \
		primal dockerize -wait tcp://dynamodb:8000

	$(DOC) \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		run --rm \
		primal dockerize -wait tcp://dynamodb:8000 \
		py.test \
		--cov-config tests/.coveragerc \
		--cov-report term-missing \
		--cov=primal \
		--timeout=10 \
		tests
	$(DOC) stop dynamodb
	$(DOC) kill dynamodb

integration_tests_config:
	$(DOC) \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		config

test:
	$(DOC) \
		-f docker-compose.yml \
		-f docker-compose.test.yml \
		run --rm \
		primal py.test -m 'not ddblocal' tests
