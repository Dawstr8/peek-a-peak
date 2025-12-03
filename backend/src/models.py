from pydantic import BaseModel, ConfigDict


def camel_to_snake(string: str) -> str:
    result = []
    for char in string:
        if char.isupper():
            result.append("_")
            result.append(char.lower())
        else:
            result.append(char)

    snake = "".join(result)
    if snake.startswith("_"):
        snake = snake[1:]

    return snake


def snake_to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=snake_to_camel,
        populate_by_name=True,
    )
