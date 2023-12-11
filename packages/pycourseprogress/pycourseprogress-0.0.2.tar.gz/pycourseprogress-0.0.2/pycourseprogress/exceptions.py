"""Course Progress API Exceptions."""

class HttpException(Exception):
    """Http exception occured."""

    def __init__(self, status_code: int, *args: object) -> None:
        self.status_code = status_code
        super().__init__(*args)
