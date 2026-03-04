from fastapi import FastAPI


def init_middlewares(app: FastAPI):
    # some middlewares
    # if you need CORS - use APIGateway CORS
    pass


__all__ = [
    "init_middlewares",
]
