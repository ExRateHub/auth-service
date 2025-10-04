class DetailError(Exception):
    detail: str | None = None

    def __init__(self, detail: str | None = None, *args, **kwargs) -> None:
        self.detail = detail if detail else self.detail