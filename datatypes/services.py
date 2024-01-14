from typing import Annotated, Literal

from pydantic import AfterValidator


ServicesIn = Literal[
  "aav_php_eb",
  "aav_php_s",
  "aav_retrograde",
  "aav1",
  "aav2",
  "aav5",
  "aav8",
  "aav9",
  "cloning_grade_dna",
  "lentiviral_prep",
]

ServicesOut = Literal[
  "AAV PHP.eB",
  "AAV PHP.S",
  "AAV Retrograde",
  "AAV1",
  "AAV2",
  "AAV5",
  "AAV8",
  "AAV9",
  "Cloning Grade DNA",
  "Lentiviral Prep",
]

SERVICES_MAP: dict[ServicesIn, ServicesOut] = {
  "aav_php_eb": "AAV PHP.eB",
  "aav_php_s": "AAV PHP.S",
  "aav_retrograde": "AAV Retrograde",
  "aav1": "AAV1",
  "aav2": "AAV2",
  "aav5": "AAV5",
  "aav8": "AAV8",
  "aav9": "AAV9",
  "cloning_grade_dna": "Cloning Grade DNA",
  "lentiviral_prep": "Lentiviral Prep",
}

SERVICES_MAP_REVERSE: dict[ServicesOut, ServicesIn] = { v: k for k, v in SERVICES_MAP.items() }

Services = Annotated[ServicesIn, AfterValidator(SERVICES_MAP.get)]
