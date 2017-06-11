#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

start-glacier:
	glacier2router --Ice.Config=glacier.config

start-web-server:
	@echo "Open http://localhost:8080"
	python3 -m http.server 8080
