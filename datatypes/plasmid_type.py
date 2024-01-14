
from typing import Annotated, Literal

from pydantic import AfterValidator


PlasmidTypeIn = Literal[
  "empty_backbone",
  "grna_shrna",
  "multiple_inserts",
  "single_insert",
]

PlasmidTypeOut = Literal[
  "Empty backbone",
  "Encodes gRNA/shRNA",
  "Encodes multiple inserts",
  "Encodes one insert",
]

PLASMID_TYPE_MAP: dict[PlasmidTypeIn, PlasmidTypeOut] = {
  "empty_backbone": "Empty backbone",
  "grna_shrna": "Encodes gRNA/shRNA",
  "multiple_inserts": "Encodes multiple inserts",
  "single_insert": "Encodes one insert",
}

PLASMID_TYPE_MAP_REVERSE: dict[PlasmidTypeOut, PlasmidTypeIn] = { v: k for k, v in PLASMID_TYPE_MAP.items() }

PlasmidType = Annotated[PlasmidTypeIn, AfterValidator(PLASMID_TYPE_MAP.get)]
