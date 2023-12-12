from __future__ import annotations

import configparser
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .secrets import SecretsModelStruct
from .systems import SystemModelStruct


class ServerModelStruct(BaseModel):
    """
    Представляет структуру модели сервера.

    :param name (str, optional): Название модели сервера.
    :param description (str, optional): Описание модели сервера.
    :param systems (list[SystemModelStruct]): Список структур модели системы, связанных с моделью сервера.
    """

    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    description: Optional[str] = None
    systems: list[SystemModelStruct] = []

    @classmethod
    def from_ini_file(cls, filename, server_name) -> ServerModelStruct:
        """
        Преобразует ini file

        :param filename: Имя файла настроек
        :param server_name: Имя сервера
        :return: Сервер
        """
        config = configparser.ConfigParser()
        config.read(filename)

        server: ServerModelStruct = cls(name=server_name)
        for el in config.sections():
            system = SystemModelStruct()
            system.name = el
            for sec in config[el]:
                system.secrets.append(SecretsModelStruct(key=sec, value=config[el][sec]))
            server.systems.append(system)

        return server
