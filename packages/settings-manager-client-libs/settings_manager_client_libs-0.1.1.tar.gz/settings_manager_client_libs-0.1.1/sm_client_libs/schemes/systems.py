from typing import Optional

from pydantic import BaseModel, ConfigDict

from .secrets import SecretsModelStruct


class SystemModelStruct(BaseModel):
    """
    Представляет структуру модели системы.

    :param name: Название модели системы
    :param secrets: Список секретов, связанных с моделью системы.
    """

    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    secrets: list[SecretsModelStruct] = []
