import urllib.parse as urllib

from compmath.api.aif import AIFClient


class APIFactory:
    def __init__(self, host: str, port: int, scheme: str = "http", path: str = "api"):
        self._base_url = urllib.urljoin(f"{scheme}://{host}:{port}", path)

    def create_aif(self) -> AIFClient:
        return AIFClient(self._base_url)
