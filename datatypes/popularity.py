from typing import Annotated, Literal

from pydantic import AfterValidator


PopularityIn = Literal[
  "low",
  "medium",
  "high",
]

PopularityOut = Literal[
  "20+ requests",
  "50+ requests",
  "100+ requests",
]

POPULARITY_MAP: dict[PopularityIn, PopularityOut] = {
  "low": "20+ requests",
  "medium": "50+ requests",
  "high": "100+ requests",
}

Popularity = Annotated[PopularityIn, AfterValidator(POPULARITY_MAP.get)]
