from typing import Annotated, Literal

from pydantic import AfterValidator


ResistanceMarkerIn = Literal[
  "basta",
  "blasticidin",
  "his3",
  "hygromycin",
  "leu2",
  "neomycin",
  "puromycin",
  "trp1",
  "ura3",
  "zeocin",
]

ResistanceMarkerOut = Literal[
  "Basta",
  "Blasticidin",
  "HIS3",
  "Hygromycin",
  "LEU2",
  "Neomycin (select with G418)",
  "Puromycin",
  "TRP1",
  "URA3",
  "Zeocin",
]

RESISTANCE_MARKET_MAP: dict[ResistanceMarkerIn, ResistanceMarkerOut] = {
  "basta": "Basta",
  "blasticidin": "Blasticidin",
  "his3": "HIS3",
  "hygromycin": "Hygromycin",
  "leu2": "LEU2",
  "neomycin": "Neomycin (select with G418)",
  "puromycin": "Puromycin",
  "trp1": "TRP1",
  "ura3": "URA3",
  "zeocin": "Zeocin",
}

ResistanceMarker = Annotated[ResistanceMarkerIn, AfterValidator(RESISTANCE_MARKET_MAP.get)]
