import requests
from pprint import pprint
import pandas as pd
from collections import defaultdict

# TODO: interaction via CLI
a = defaultdict(list)
b = defaultdict(list)
json_post = {'name': 'Amazochroma carvalhoi',
             'verbose': True}
    
r = requests.get('https://api.gbif.org/v1/species/match', params=json_post)

pprint(r.json())

# TODO: implement fuzzy to extract column name
# a['kingdom'] = r.json()['kingdom']
# a['phylum'] = r.json()['phylum']
# a['class'] = r.json()['class']
# a['order'] = r.json()['order']
# a['family'] = r.json()['family']
# a['genus'] = r.json()['genus']
# a['species_key'] = r.json()['speciesKey']
# a['match_score'] = r.json()['confidence']

# b['kingdom'] = ['kingdom']
# b['phylum'] = ['phylum']
# b['class'] = ['class']
# b['order'] = ['order']
# b['family'] = ['family']
# b['genus'] = ['genus']

# if a['kingdom'] != b['kingdom'] or \
#    a['phylum'] != b['phylum'] or \
#    a['class'] != b['class'] or \
#    a['order'] != b['order'] or \
#    a['family'] != b['family']:

# print(a)
