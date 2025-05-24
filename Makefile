PYTHONPATH := src

export PYTHONPATH

.PHONY: run-dev-serve
run-dev-serve:
	$(GRANIAN) \
	    interface.http.asgi:create_asgi_application \
		--interface=asgi \
		--factory \
		--reload
