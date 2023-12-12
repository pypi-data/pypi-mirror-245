[![Test](https://github.com/acdh-oeaw/acdh-id-reconciler/actions/workflows/test.yml/badge.svg)](https://github.com/acdh-oeaw/acdh-id-reconciler/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/acdh-id-reconciler.svg)](https://badge.fury.io/py/acdh-id-reconciler)
[![codecov](https://codecov.io/gh/acdh-oeaw/acdh-id-reconciler/branch/main/graph/badge.svg?token=WY0Q1GRIG1)](https://codecov.io/gh/acdh-oeaw/acdh-id-reconciler)
[![flake8 Lint](https://github.com/acdh-oeaw/acdh-id-reconciler/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/acdh-id-reconciler/actions/workflows/lint.yml)

# acdh-id-reconciler
python package to reconcile GND and GeoNames IDs via WikiData.


## install

`pip install acdh-id-reconciler`

## use

### from GND to WikiData and GeoNames ID

```python
from acdh_id_reconciler import gnd_to_geonames

test = "https://d-nb.info/gnd/4010858-2"
results = gnd_to_geonames(test)
print(results)
# {'wikidata': 'http://www.wikidata.org/entity/Q261664', 'gnd': '4010858-2', 'geonames': '2781124'}
```

### from GND to WikiData

```python
from acdh_id_reconciler import gnd_to_wikidata

test = "https://d-nb.info/gnd/4074255-6"
results = gnd_to_wikidata(test)
print(results)
# {'wikidata': 'http://www.wikidata.org/entity/Q41329', 'gnd': '4074255-6'}
```

### from GND to WikiData plus Custom-ID

```python
from acdh_id_reconciler import gnd_to_wikidata_custom

test = "https://d-nb.info/gnd/118566512"
custom = "P21" # https://www.wikidata.org/wiki/Property:P6194
results = gnd_to_wikidata_custom(test, custom)
print(results)
# {'wikidata': 'http://www.wikidata.org/entity/Q44517',  'gnd': '118566512', 'custom': 'http://www.wikidata.org/entity/Q6581097'}
```

### from Geonames to WikiData

```python
from acdh_id_reconciler import geonames_to_wikidata

test = "https://www.geonames.org/2761369"
results = geonames_to_wikidata(test)
print(results)
# {'wikidata': 'http://www.wikidata.org/entity/Q1741', 'geonames': '2761369'}
```

### from Geonames to GND

```python
from acdh_id_reconciler import geonames_to_gnd

test = "https://www.geonames.org/2761369"
results = geonames_to_gnd(test)
print(results)
# {'wikidata': 'http://www.wikidata.org/entity/Q1741', 'geonames': '2761369', 'gnd': '4066009-6'}
```

### from Wikidata to Wikipedia

```python
from acdh_id_reconciler import wikidata_to_wikipedia

test = "https://www.wikidata.org/wiki/Q1186567/"
result = wikidata_to_wikipedia(test)
print(result)
# 'https://de.wikipedia.org/wiki/Alexandrinski-Theater'

# default language is set to german, can be changed by settings param result e.g. `wiki_lang='enwiki'`
result = wikidata_to_wikipedia(test, wiki_lang='enwiki')
print(result)
# 'https://en.wikipedia.org/wiki/Alexandrinsky_Theatre'
