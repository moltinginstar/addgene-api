from typing import Annotated, Literal

from pydantic import AfterValidator


ExpressionIn = Literal[
  "bacterial",
  "mammalian",
  "insect",
  "plant",
  "worm",
  "yeast",
]

ExpressionOut = Literal[
  "Bacterial Expression",
  "Mammalian Expression",
  "Insect Expression",
  "Plant Expression",
  "Worm Expression",
  "Yeast Expression",
]

EXPRESSION_MAP: dict[ExpressionIn, ExpressionOut] = {
  "bacterial": "Bacterial Expression",
  "mammalian": "Mammalian Expression",
  "insect": "Insect Expression",
  "plant": "Plant Expression",
  "worm": "Worm Expression",
  "yeast": "Yeast Expression",
}

Expression = Annotated[ExpressionIn, AfterValidator(EXPRESSION_MAP.get)]
