from typing import Annotated, Literal

from pydantic import BeforeValidator, PositiveInt


PageSize = Annotated[Literal[10, 20, 30, 40, 50], BeforeValidator(int)]  # TODO: Swagger doesn't show constraints

PageNumber = PositiveInt
