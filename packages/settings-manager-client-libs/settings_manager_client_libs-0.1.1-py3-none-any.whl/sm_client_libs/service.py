from pathlib import Path
from urllib.parse import urljoin

import httpx

from .exception import SettingsManagerException, SettingsManagerParseFileException
from .schemes import ServerModelStruct


class SettingsManagerConnector:

    __root_path: str
    __URLs: dict[str, str] = {
        "get_all_settings": "/v1/secrets/",
        "ini_new_server": "/v1/secrets/",
    }
    __server_id: str

    def __init__(self, settings_manager_url: str, server_id: str, server_name: str):
        self.__root_path = settings_manager_url
        self.__server_id = server_id
        self.__server_name = server_name

    def get_all_settings(self) -> ServerModelStruct:
        url = urljoin(self.__root_path, self.__URLs["get_all_settings"])
        url = urljoin(url, self.__server_id)
        response = httpx.get(url)
        if response.status_code != 200:
            raise SettingsManagerException("Секреты не получены: %s" % response.json())

        return ServerModelStruct.model_validate(response.json())

    def init_new_server(self, file_path):
        file = Path(file_path).resolve().absolute()
        if not file.is_file() or not file.exists():
            raise SettingsManagerParseFileException(f"Файл настроек не найден, проверте путь {file}")
        response = httpx.post(
            self.__root_path + self.__URLs["ini_new_server"],
            json=ServerModelStruct.from_ini_file(file, self.__server_name).model_dump(),
        )
        # file.unlink()
        return response.json()
