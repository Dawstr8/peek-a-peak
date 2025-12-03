from pydantic import BaseModel, ConfigDict

from src.common.utils import snake_to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=snake_to_camel,
        populate_by_name=True,
    )
