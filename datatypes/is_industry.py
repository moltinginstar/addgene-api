from typing import Annotated, Literal

from pydantic import AfterValidator, BeforeValidator


IsIndustryIn = Literal[True]

IsIndustryOut = Literal["Available to Industry"]

IsIndustry = Annotated[IsIndustryIn, BeforeValidator(lambda x: x == "True"), AfterValidator(lambda _: "Available to Industry")]
