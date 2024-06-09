import json

with open('data\structured\ELSST_eval_set.json', 'r') as f:
    eval_set = json.load(f)

with open('data\structured\ELSST_train_set.json', 'r') as f:
    train_set = json.load(f)


for entity in eval_set:

    for item in train_set:
        if item['relationships'] is not None:
            for relat in item['relationships']:
                if entity['id'] == relat['target']:
                    print(entity['id'])
                    break