#!/usr/bin/make
#
all: test

bin/python:
	virtualenv-2.6 --no-site-packages .

develop-eggs: bin/python bootstrap.py
	./bin/python bootstrap.py

bin/buildout: develop-eggs

.installed.cfg: bin/buildout

bin/test: .installed.cfg
	./bin/buildout -vt 5

.PHONY: test
test: bin/test
	bin/test -s plone.app.referenceintegrity


.PHONY: cleanall
cleanall:
	rm -fr bin develop-eggs downloads eggs parts .installed.cfg
