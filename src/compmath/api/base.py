import json
from typing import Callable, Any, Literal

from PyQt6.QtCore import QObject, QUrl
from PyQt6.QtNetwork import QNetworkReply, QNetworkRequest, QNetworkAccessManager


class APIBase(QObject):

    def __init__(self, base_url: str):
        super().__init__()
        self._base_url = base_url

        self._managers = []

    def get(
            self,
            url: str,
            success_callbacks: list[Callable[[Any], Any]] | None = None,
            error_callbacks: list[Callable[[str], Any]] | None = None
    ):
        self.make_request("get", url, None, success_callbacks, error_callbacks)

    def post(
            self,
            url: str,
            data: dict[str, Any],
            success_callbacks: list[Callable[[Any], Any]] | None = None,
            error_callbacks: list[Callable[[str], Any]] | None = None
    ):
        self.make_request("post", url, data, success_callbacks, error_callbacks)

    def make_request(
            self,
            method: Literal["get", "post"],
            url: str,
            data: dict[str, Any] | None = None,
            success_callbacks: list[Callable[[Any], Any]] | None = None,
            error_callbacks: list[Callable[[str], Any]] | None = None
    ):
        request = QNetworkRequest(QUrl(url))

        manager = QNetworkAccessManager(self)
        manager.finished.connect(lambda reply: self._on_finished(reply, success_callbacks, error_callbacks))
        self._managers.append(manager)

        # Data
        if data:
            data = json.dumps(data).encode()
            request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")

        if method == "get":
            manager.get(request)
        elif method == "post":
            manager.post(request, data)

    def _on_finished(
            self,
            reply: QNetworkReply,
            success_callbacks: list[Callable[[Any], Any]] | None,
            error_callbacks: list[Callable[[str], Any]] | None
    ):
        try:
            response_json = json.loads(reply.readAll().data().decode())
        except json.JSONDecodeError:
            response_json = None

        if reply.error() != QNetworkReply.NetworkError.NoError and error_callbacks is not None:
            message = "Неизвестная ошибка"
            if response_json and (error:= response_json.get("error")):
                error_type = error.get("type")
                if error_type == 1:
                    message = error.get("content")
                elif error_type == 2:
                    first_error_item = error.get("content")[0]
                    message = f"Ошибка в поле: {first_error_item.get("field")}: {first_error_item.get("message")}"
            for callback in error_callbacks:
                callback(message)
        elif (reply.error() == QNetworkReply.NetworkError.NoError) and response_json and success_callbacks is not None:
            for callback in success_callbacks:
                callback(response_json.get("content"))
        self._managers.remove(reply.manager())
