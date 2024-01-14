from typing import Annotated, Literal

from pydantic import AfterValidator


VectorTypeIn = Literal[
  "aav",
  "cre_lox",
  "crispr",
  "lentiviral",
  "luciferase",
  "retroviral",
  "rnai",
  "synthetic_biology",
  "talen",
  "unspecified",
]

VectorTypeOut = Literal[
  "AAV",
  "Cre/Lox",
  "CRISPR",
  "Lentiviral",
  "Luciferase",
  "Retroviral",
  "RNAi",
  "Synthetic Biology",
  "TALEN",
  "Unspecified",
]

VECTOR_TYPE_MAP: dict[VectorTypeIn, VectorTypeOut] = {
  "aav": "AAV",
  "cre_lox": "Cre/Lox",
  "crispr": "CRISPR",
  "lentiviral": "Lentiviral",
  "luciferase": "Luciferase",
  "retroviral": "Retroviral",
  "rnai": "RNAi",
  "synthetic_biology": "Synthetic Biology",
  "talen": "TALEN",
  "unspecified": "Unspecified",
}

VectorType = Annotated[VectorTypeIn, AfterValidator(VECTOR_TYPE_MAP.get)]
