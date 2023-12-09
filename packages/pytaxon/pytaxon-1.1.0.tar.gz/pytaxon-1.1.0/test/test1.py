import requests
from pprint import pprint
import pandas as pd
from collections import defaultdict

df = pd.read_excel('F:/0 - Bibliotecas Windows/Área de trabalho/pytaxon/pytaxon-cli/db/Lepidoptera_-_Importacao_IX_lote_1.xls').reset_index().fillna('xxxxx')
taxons_list = list((df['Genus1'].str.capitalize() + ' ' + df['Species1'].str.lower()).values)
checked_data = defaultdict(list)
original_data = defaultdict(list)

original_data['species'] = taxons_list
original_data['kingdom'] = list(df['Kingdom'])
original_data['phylum'] = list(df['Phylum'])
original_data['class'] = list(df['Class'])
original_data['order'] = list(df['Order'])
original_data['family'] = list(df['Family'])
# original_data['genus'] = list(df['genus']


for i, j in enumerate(taxons_list):
    json_post = {'name': j,
                 'verbose': True}
    
    r = requests.get('https://api.gbif.org/v1/species/match', params=json_post)

    try:
        # TODO: implement fuzzy to extract column name
        checked_data['species'].append(r.json()['canonicalName'])
        checked_data['kingdom'].append(r.json()['kingdom'])
        checked_data['phylum'].append(r.json()['phylum'])
        checked_data['class'].append(r.json()['class'])
        checked_data['order'].append(r.json()['order'])
        checked_data['family'].append(r.json()['family'])
        checked_data['genus'].append(r.json()['genus'])
        checked_data['species_key'].append(r.json()['speciesKey'])
        checked_data['match_score'].append(r.json()['confidence'])
    except Exception as e:
        print(e, r.json())
    
    if checked_data['species'][i] != original_data['species'][i] or \
       checked_data['kingdom'][i] != original_data['kingdom'][i] or \
       checked_data['phylum'][i] != original_data['phylum'][i] or \
       checked_data['class'][i] != original_data['class'][i] or \
       checked_data['order'][i] != original_data['order'][i] or \
       checked_data['family'][i] != original_data['family'][i]:
        print(j, i, 'errado')
    else:
        print(j, i, 'certo')

print(original_data)
print()
print(checked_data)
