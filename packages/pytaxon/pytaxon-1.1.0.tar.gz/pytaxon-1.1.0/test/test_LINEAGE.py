import pandas as pd
import requests
from pprint import pprint
from collections import defaultdict

incorrect_lineage_data = defaultdict(list)

# a = pd.read_excel("F:/0 - Bibliotecas Windows/Área de trabalho/pytaxon/pytaxon-cli/db/Lepidoptera_-_Importacao_IX_lote_1_corrigido.xlsx").reset_index()
# b = list((a['Genus1'] + ' ' + a['Species1']).values)
# c = []

json_post = {'names': ['Taitu juruensis'],
             'do_approximate_matching': True,
             'context_name': 'All life'}

try:
    r = requests.post('https://api.opentreeoflife.org/v3/tnrs/match_names', json=json_post)
    print('Success accessing the OpenTreeOfLife API, now checking taxons...')
except Exception as error:
    print('Error accessing the OpenTreeOfLife API: ', error)

pprint(r.json())
# for i, taxon in enumerate(r.json()['matched_names']):
#     ott_id = r.json()['results'][i]['matches'][0]['taxon']['ott_id']
#     c.append(ott_id)

# print(c)

# for i in c:
#     _json_post = {'ott_id': i,
#               'include_lineage': True}

#     try:
#         r = requests.post('https://api.opentreeoflife.org/v3/taxonomy/taxon_info', json=_json_post)
#         # print('Success accessing the OpenTreeOfLife API, now checking taxons...')
#         print(len(r.json()['lineage']))
#     except Exception as error:
#         # print('Error accessing the OpenTreeOfLife API: ', error)
#         pass

    

    # incorrect_lineage_data['phylum'].append(r.json()['lineage'][20]['unique_name'])
    # incorrect_lineage_data['class'].append(r.json()['lineage'][16]['unique_name'])
    # incorrect_lineage_data['order'].append(r.json()['lineage'][10]['unique_name'])
    # incorrect_lineage_data['family'].append(r.json()['lineage'][3]['unique_name'])
    # incorrect_lineage_data['tribe'].append(r.json()['lineage'][1]['unique_name'])

    # incorrect_lineage_data['test'].append(len(r.json()['lineage']))

# print(incorrect_lineage_data)
