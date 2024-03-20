import scispacy
import spacy
import pandas as pd
import sys
from datetime import datetime
import json
import os.path


print('Start time ', datetime.now())
#SBATCH --nodes=1


nlp = spacy.load("en_core_sci_scibert")
rels = json.load(open('data/rel_map.json', 'r'))
path = '/users/k1810895/data/KER/data/scispacy_sentences/'
notes = pd.read_csv('/users/k1810895/data/KER/data/mimic_notes.csv')
id_text = pd.Series(notes.text.values,index=notes.row_id).to_dict()


bt = int(sys.argv[1])
print(bt)


file_name = 'batch' + str(bt) + '.json'
output_file = '/users/k1810895/data/snomed/data/scispacy_mimic/batch' + str(bt) +'_relations.text'

with open(output_file, 'w', buffering=128) as fw:

    docs = json.load(open(path+file_name, 'r'))

    for did in docs.keys():
    #   Only for discharge summary since the quality of the content is relatively higher
    #   if int(did) in discharg_dids:
        if True:
            entities = []
            tokens = []
            text = id_text[int(did)]
            doc = nlp(text)
    #         print(text)
            for s in doc.sents:
                for token in s:
                    tokens.append(token.text)

            sents = docs[did]
            for sid in sents.keys():
                sent_start = int(sid.split('_')[0])
                sent = sents[sid]

                annots = sent['sent_annots']            
                for i, ann in enumerate(annots):
                    ann['id'] = len(entities)
                    ann['start_char'] = ann['start_char'] + sent_start
                    ann['end_char'] = ann['end_char'] + sent_start
                    span = doc.char_span(ann['start_char'], ann['end_char'])
                    ann['start'] = span.start
                    ann['end'] = span.end
    #                 print(ann['text'], '-----', tokens[ann['start']: ann['end']], '----', text[ann['start_char']: ann['end_char']])
                    entities.append(ann)
            relations = []
            # If include all sentence with any number of annotations. it ends with a super large file
            # Select centain types of annotations to focus. 
            for index_ai, ai in enumerate(entities):
                for index_aj, aj in enumerate(entities[index_ai+1:]):
                    index_aj = index_aj + index_ai + 1
                    ai_cui, aj_cui = ai['cui'], aj['cui']

                    min_cui, max_cui = ai_cui, aj_cui
                    min_cui_index, max_cui_index = index_ai, index_aj

                    if min_cui > max_cui:
                        min_cui, max_cui = aj_cui, ai_cui
                        min_cui_index, max_cui_index = index_aj, index_ai

                    cui_key = min_cui + '-' + max_cui                    
                    if cui_key in rels:

                        rel = rels[cui_key]['rela']
                        dire = rels[cui_key]['dir']
                        if dire == 'Y':
                            head, tail = min_cui_index, max_cui_index

                        else:
                            head, tail = max_cui_index, min_cui_index
    #                         print(cui_key, rels[cui_key])
    #                     print({'type': rel,  'head': (entities[head]['cui']), 'tail': entities[tail]['cui']})
                        relations.append({'type': rel,  'head': head, 'tail': tail})
            fw.write(json.dumps({'text': text, 'tokens': tokens, 'entities': entities, 'relations': relations}))
            fw.write('\n')


