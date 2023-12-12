import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from AcdhArcheAssets.uri_norm_rules import get_norm_id

from .utils import normalize_wikidata_id

ENDPOINT_URL = "https://query.wikidata.org/sparql"
USER_AGENT = "acdh-id-reconciler (https://www.oeaw.ac.at/acdh/acdh-ch-home)"
WIKIAPI_BASE = "https://www.wikidata.org/w/api.php"
WIKIAPI_URL = (
    f"{WIKIAPI_BASE}?action=wbgetentities&format=json&props=sitelinks/urls&ids="
)


def gnd_to_wikidata(gnd, user_agent=USER_AGENT):
    """ """
    norm_id = get_norm_id(gnd)
    query = f"""SELECT ?wikidata ?gnd
    WHERE
    {{
    ?wikidata wdt:P227 "{norm_id}".
    ?wikidata wdt:P227 ?gnd .
    }}"""
    sparql = SPARQLWrapper(ENDPOINT_URL, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    ids = {
        key: value["value"]
        for (key, value) in results["results"]["bindings"][0].items()
    }
    return ids


def gnd_to_geonames(gnd, user_agent=USER_AGENT):
    """ """
    norm_id = get_norm_id(gnd)
    query = f"""SELECT ?wikidata ?gnd ?geonames
    WHERE
    {{
    ?wikidata wdt:P227 "{norm_id}".
    ?wikidata wdt:P227 ?gnd .
    ?wikidata wdt:P1566 ?geonames .
    }}"""
    sparql = SPARQLWrapper(ENDPOINT_URL, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    ids = {
        key: value["value"]
        for (key, value) in results["results"]["bindings"][0].items()
    }
    return ids


def geonames_to_gnd(geonames, user_agent=USER_AGENT):
    norm_id = get_norm_id(geonames)
    query = f"""SELECT ?wikidata ?gnd ?geonames
    WHERE
    {{
    ?wikidata wdt:P1566 "{norm_id}".
    ?wikidata wdt:P227 ?gnd .
    ?wikidata wdt:P1566 ?geonames .
    }}"""
    sparql = SPARQLWrapper(ENDPOINT_URL, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    ids = {
        key: value["value"]
        for (key, value) in results["results"]["bindings"][0].items()
    }
    return ids


def geonames_to_wikidata(geonames, user_agent=USER_AGENT):
    norm_id = get_norm_id(geonames)
    query = f"""SELECT ?wikidata ?geonames
    WHERE
    {{
    ?wikidata wdt:P1566 "{norm_id}".
    ?wikidata wdt:P1566 ?geonames .
    }}"""
    sparql = SPARQLWrapper(ENDPOINT_URL, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    ids = {
        key: value["value"]
        for (key, value) in results["results"]["bindings"][0].items()
    }
    return ids


def wikidata_to_wikipedia(wikidata_uri, user_agent=USER_AGENT, wiki_lang="dewiki"):
    wiki_id = normalize_wikidata_id(wikidata_uri)
    query_url = f"{WIKIAPI_URL}{wiki_id}&sitefilter={wiki_lang}"
    r = requests.get(
        query_url, headers={"User-Agent": user_agent, "Accept-Encoding": "gzip"}
    )
    result = r.json()
    wikipedia_url = result["entities"][wiki_id]["sitelinks"][wiki_lang]["url"]
    return wikipedia_url


def gnd_to_wikidata_custom(gnd, wiki_property, user_agent=USER_AGENT):
    """ """
    norm_id = get_norm_id(gnd)
    query = f"""SELECT ?wikidata ?gnd ?custom
    WHERE
    {{
    ?wikidata wdt:P227 "{norm_id}".
    ?wikidata wdt:P227 ?gnd .
    ?wikidata wdt:{wiki_property} ?custom .
    }}"""
    sparql = SPARQLWrapper(ENDPOINT_URL, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    ids = {
        key: value["value"]
        for (key, value) in results["results"]["bindings"][0].items()
    }
    return ids
