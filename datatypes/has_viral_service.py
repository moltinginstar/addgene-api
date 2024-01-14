from typing import Annotated, Literal

from pydantic import AfterValidator, BeforeValidator


HasViralServiceIn = Literal[True]

HasViralServiceOut = Literal["Viral Service Available"]

HasViralService = Annotated[HasViralServiceIn, BeforeValidator(lambda x: x == "True"), AfterValidator(lambda _: "Viral Service Available")]
