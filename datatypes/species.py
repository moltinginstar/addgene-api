from typing import Annotated, Literal

from pydantic import AfterValidator


SpeciesIn = Literal[
  "arabidopsis_thaliana",
  "danio_rerio",
  "drosophila_melanogaster",
  "escherichia_coli",
  "homo_sapiens",
  "mus_musculus",
  "rattus_norvegicus",
  "saccharomyces_cerevisiae",
  "sars_cov_2",
  "synthetic",
]

SpeciesOut = Literal[
  "Arabidopsis thaliana",
  "Danio rerio",
  "Drosophila melanogaster",
  "Escherichia coli",
  "Homo sapiens",
  "Mus musculus",
  "Rattus norvegicus",
  "Saccharomyces cerevisiae",
  "Severe acute respiratory syndrome coronavirus 2",
  "Synthetic",
]

SPECIES_MAP: dict[SpeciesIn, SpeciesOut] = {
  "arabidopsis_thaliana": "Arabidopsis thaliana",
  "danio_rerio": "Danio rerio",
  "drosophila_melanogaster": "Drosophila melanogaster",
  "escherichia_coli": "Escherichia coli",
  "homo_sapiens": "Homo sapiens",
  "mus_musculus": "Mus musculus",
  "rattus_norvegicus": "Rattus norvegicus",
  "saccharomyces_cerevisiae": "Saccharomyces cerevisiae",
  "sars_cov_2": "Severe acute respiratory syndrome coronavirus 2",
  "synthetic": "Synthetic",
}

Species = Annotated[SpeciesIn, AfterValidator(SPECIES_MAP.get)]
