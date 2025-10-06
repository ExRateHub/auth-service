from litestar import Response


def make_error_response(status_code: int, details: str) -> Response[dict]:
    return Response(content={"status_code": status_code, "details": details}, status_code=status_code)


def make_data_response(status_code: int, data: dict | None = None, message: str = "ok") -> Response[dict]:
    return Response(content={"status_code": status_code, "data": data, message: message}, status_code=status_code)
