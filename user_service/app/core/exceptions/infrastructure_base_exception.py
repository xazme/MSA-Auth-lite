class InfrastructureBaseException(Exception):
    """
    Infrastructure Base Exception
    """

    status_code: int = 500

    def __init__(
        self,
        message: str,
        model_name: str | None = None,
        details: str | None = None,
    ) -> None:
        self.message = message
        self.details = details
        self.model_name = model_name
        super().__init__(message)
