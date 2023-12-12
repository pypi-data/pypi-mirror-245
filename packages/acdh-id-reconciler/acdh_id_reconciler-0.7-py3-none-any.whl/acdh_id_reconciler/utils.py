def normalize_wikidata_id(wikidata_url):
    if wikidata_url[-1] == "/":
        wikidata_url = wikidata_url[:-1]
    wiki_id = wikidata_url.split("/")[-1]
    return wiki_id
