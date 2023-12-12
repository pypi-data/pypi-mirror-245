from pydantic import BaseModel, ConfigDict


class SecretsModelStruct(BaseModel):
    """
    Представляет структуру модели секретов.

    :param key: Ключ к секрету.
    :param value: Значение секрета.
    """

    model_config = ConfigDict(from_attributes=True)

    key: str
    value: str
