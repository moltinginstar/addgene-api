from contextlib import asynccontextmanager
from typing import Annotated

import httpx
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from tenacity import retry, stop_after_attempt, retry_if_exception_type

from datatypes import *
from datatypes.expression import ExpressionIn
from datatypes.popularity import PopularityIn
from datatypes.services import ServicesIn
from datatypes.plasmid_type import PlasmidTypeIn, PLASMID_TYPE_MAP_REVERSE
from datatypes.services import SERVICES_MAP_REVERSE


ADDGENE_BASE_URL = "https://www.addgene.org"
ADDGENE_PLASMID_CATALOG_PATH = "/search/catalog/plasmids/"
ADDGENE_PLASMID_SEQUENCES_PATH = "/{plasmid_id}/sequences/"


class PlasmidOverview(BaseModel):
  id: int  # "Plasmid"
  name: str
  depositor: str
  purpose: str | None = None
  article_url: HttpUrl | None = None
  insert: str | None = None
  tags: str | None = None
  mutation: str | None = None
  plasmid_type: PlasmidTypeIn | None = None  # "Type"
  vector_type: str | None = None  # "Use"; apparently not limited to VectorTypeIn :(
  popularity: PopularityIn | None = None  # Flame before name
  expression: list[ExpressionIn] | None = None
  promoter: str | None = None
  map_url: HttpUrl | None = None
  services: ServicesIn | None = None  # "Has Service"
  is_industry: bool  # "Availability"


def scrape_plasmids(html_content: str) -> list[dict[str, str]]:
  """
  Scrape list of plasmids from Addgene HTML content.

  Args:
  html_content (str): HTML content of the Addgene search results page.

  Returns:
  list: a list of dictionaries containing plasmid data.
  """

  # Parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(html_content, "html.parser")

  # Find all plasmid entries
  plasmid_entries = soup.find_all("div", class_="search-result-item")

  # List to hold all plasmid data
  plasmid_data = []

  # Extract details from each plasmid entry
  for plasmid in plasmid_entries:
    # Extract plasmid name and URL
    title_tag = plasmid.find("h3", class_="search-result-title")
    title_link = title_tag.find("a")
    plasmid_name = title_link.text.strip()

    # Extract plasmid popularity
    popularity = None
    flame_icon = soup.find("span", class_="addgene-flame")
    if flame_icon:
      match flame_icon["class"][-1]:
        case "addgene-flame-high":
          popularity = "high"
        case "addgene-flame-medium":
          popularity = "medium"
        case "addgene-flame-low":
          popularity = "low"

    # Extract other details like plasmid #, depositor, etc.
    details = plasmid.find("div", class_="search-result-details")
    rows = details.find_all("div", class_="row")

    plasmid_info = {
      "name": plasmid_name,
      "popularity": popularity,
    }

    # Parse each row for specific details
    for row in rows:
      label = row.find("span", class_="field-label")
      value = row.select_one("div.field + div")

      if label and value:
        field_name = label.text.strip().lower()
        field_value = value.text.strip()

        if field_name == "article":
          url = value.find("a")["href"]
          field_value = f"{ADDGENE_BASE_URL}{url}"

        plasmid_info[field_name] = field_value

    # Extract plasmid map
    map_column = plasmid.find("div", class_="map-column")
    if map_column:
      map_img = map_column.find("img")
      plasmid_info["map_url"] = map_img["src"]

    # Postprocessing
    expression = plasmid_info.get("expression")
    expression = [e.lower() for e in expression.replace(" and ", ", ").split(", ")] if expression else None

    plasmid_data.append(PlasmidOverview(
      id=int(plasmid_info["plasmid"].removeprefix("#")),
      name=plasmid_info["name"],
      depositor=plasmid_info["depositor"],
      purpose=plasmid_info.get("purpose"),
      article_url=plasmid_info.get("article"),
      insert=plasmid_info.get("insert"),
      tags=plasmid_info.get("tags"),
      mutation=plasmid_info.get("mutation"),
      plasmid_type=PLASMID_TYPE_MAP_REVERSE.get(plasmid_info.get("type")),
      vector_type=plasmid_info.get("use"),
      popularity=plasmid_info["popularity"],
      expression=expression,
      promoter=plasmid_info.get("promoter"),
      map_url=plasmid_info.get("map_url"),
      services=SERVICES_MAP_REVERSE.get(plasmid_info.get("has service")),
      is_industry=plasmid_info["availability"] != "Academic Institutions and Nonprofits only",
    ))

  return plasmid_data


def scrape_plasmid_sequence_url(
  html_content: str,
  format: SequenceFormat = "snapgene",
) -> HttpUrl | None:
  """
  Extract plasmid sequence download URL from Addgene HTML content.

  Args:
  html_content (str): HTML content of the Addgene plasmid details page.

  Returns:
  str: the URL where the plasmid sequence can be found.
  """

  # Parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(html_content, "html.parser")

  # Find full plasmid sequence link
  full_sequences_section = soup.find("section", id="depositor-full")
  full_sequence_link = full_sequences_section.find("a", class_=f"{format}-file-download")

  return full_sequence_link["href"] if full_sequence_link else None


@asynccontextmanager
async def lifespan(app: FastAPI):
  app.addgene_client = httpx.AsyncClient(
    base_url="https://www.addgene.org",
    http2=True,
    follow_redirects=True,
  )
  yield
  await app.addgene_client.aclose()


app = FastAPI(
  title="Addgene API",
  description="An unofficial API for Addgene, the open-source plasmid repository.",
  version="0.1.0",
  lifespan=lifespan,
)


@retry(retry=retry_if_exception_type(httpx.ConnectTimeout), stop=stop_after_attempt(3))
@app.get("/plasmids")
async def search_plasmids(
  query: Annotated[
    str | None,
    Query(description="Unstructured search – look up plasmids by name, ID, and more."),
  ] = None,
  page_size: Annotated[
    PageSize | None,
    Query(description="**Note:** Results seem to be sorted semi-randomly, so pagination might not make much sense."),
  ] = 10,
  page_number: Annotated[
    PageNumber | None,
    Query(description="**Note:** Pagination does not go beyond 12000 results (i.e., 300 pages when page_size is 40)."),
  ] = 1,
  vector_types: VectorType | None = None,
  expression: Expression | None = None,
  species: Species | None = None,
  plasmid_type: PlasmidType | None = None,
  resistance_marker: ResistanceMarker | None = None,
  bacterial_resistance: BacterialResistance | None = None,
  has_dna_service: HasDNAService | None = None,
  has_viral_service: HasViralService | None = None,
  is_industry: IsIndustry | None = None,
  services: Services | None = None,
  popularity: Popularity | None = None,
):
  response = await app.addgene_client.get(ADDGENE_PLASMID_CATALOG_PATH, params={
    "q": query,
    "page_size": page_size,
    "page_number": page_number,
    "vector_types": vector_types,
    "expression": expression,
    "species": species,
    "plasmid_type": plasmid_type,
    "resistance_marker": resistance_marker,
    "bacterial_resistance": bacterial_resistance,
    "requests": popularity,
    "is_industry": is_industry,
    "has_viral_service": has_viral_service,
    "has_dna_service": has_dna_service,
    "services": services,
  })
  if response.status_code == 200:
    return scrape_plasmids(response.text)
  else:
    raise HTTPException(status_code=404, detail="Data not found.")


@retry(retry=retry_if_exception_type(httpx.ConnectTimeout), stop=stop_after_attempt(3))
@app.get("/plasmids/{plasmid_id}", response_class=RedirectResponse)
async def download_plasmid_sequence(
  plasmid_id: int,
  format: SequenceFormat = "snapgene",
):
  url = ADDGENE_PLASMID_SEQUENCES_PATH.format(plasmid_id=plasmid_id)
  response = await app.addgene_client.get(url)
  if response.status_code == 200:
    return scrape_plasmid_sequence_url(response.text, format=format)
  else:
    raise HTTPException(status_code=404, detail="Data not found.")
