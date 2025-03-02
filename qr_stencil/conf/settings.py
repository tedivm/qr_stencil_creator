from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "qr_stencil"
    debug: bool = False
    plausible_domain: str | None = None
