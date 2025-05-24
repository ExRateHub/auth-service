PYTHONPATH := src
HTTP_SERVER := granian

export PYTHONPATH

.PHONY: run-dev-serve
run-dev-serve:
	$(HTTP_SERVER) \
	    interface.http.asgi:create_asgi_application \
		--interface=asgi \
		--factory \
		--reload
