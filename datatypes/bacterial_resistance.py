from typing import Annotated, Literal

from pydantic import AfterValidator


BacterialResistanceIn = Literal[
  "ampicillin",
  "ampicillin_kanamycin",
  "zeocin",
  "chloramphenicol",
  "chloramphenicol_ampicillin",
  "chloramphenicol_spectinomycin",
  "gentamicin",
  "kanamycin",
  "spectinomycin",
  "tetracycline",
]

BacterialResistanceOut = Literal[
  "Ampicillin",
  "Ampicillin and kanamycin",
  "Bleocin (zeocin)",
  "Chloramphenicol",
  "Chloramphenicol and ampicillin",
  "Chloramphenicol and spectinomycin",
  "Gentamicin",
  "Kanamycin",
  "Spectinomycin",
  "Tetracycline",
]

BACTERIAL_RESISTANCE_MAP: dict[BacterialResistanceIn, BacterialResistanceOut] = {
  "ampicillin": "Ampicillin",
  "ampicillin_kanamycin": "Ampicillin and kanamycin",
  "zeocin": "Bleocin (zeocin)",
  "chloramphenicol": "Chloramphenicol",
  "chloramphenicol_ampicillin": "Chloramphenicol and ampicillin",
  "chloramphenicol_spectinomycin": "Chloramphenicol and spectinomycin",
  "gentamicin": "Gentamicin",
  "kanamycin": "Kanamycin",
  "spectinomycin": "Spectinomycin",
  "tetracycline": "Tetracycline",
}

BacterialResistance = Annotated[BacterialResistanceIn, AfterValidator(BACTERIAL_RESISTANCE_MAP.get)]
