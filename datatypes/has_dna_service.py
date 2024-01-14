from typing import Annotated, Literal

from pydantic import AfterValidator, BeforeValidator


HasDNAServiceIn = Literal[True]

HasDNAServiceOut = Literal["DNA Service Available"]

HasDNAService = Annotated[HasDNAServiceIn, BeforeValidator(lambda x: x == "True"), AfterValidator(lambda _: "DNA Service Available")]
