from pymongo import MongoClient
import pprint
import sys
client = MongoClient()

if __name__ == '__main__':
    # redirect output to a file, then get the collection we want
    orig = sys.stdout
    sys.stdout = open('../check4_output.txt', 'w')
    db = client['mongo_db_lab']
    defs = db['definitions']
    
    print('Entire Definition Collection:')
    print('-'*40)
    for defn in defs.find():
        pprint.pprint(defn)
    
    print('-'*40)
    print('\nOne Document Fetch:')
    print('-'*40)
    pprint.pprint(defs.find_one())
    
    print('-'*40)
    print('\nSpecific Document Fetch:')
    print('-'*40)
    pprint.pprint(defs.find_one({"word" : "B-Vector"}))
    
    print('-'*40)
    print('\nID-based Fetch:')
    print('-'*40)
    # we'll use ACM for this example
    acm = defs.find_one({'word' : 'ACM'})
    pprint.pprint(defs.find_one({"_id": acm.get('_id')}))
    
    print('-'*40)
    print('\nInserted Document:')
    print('-'*40)
    # I don't remember my old definition
    vibe_check = {'word' : 'Vibe-Check',
                  'definition' : 'bonk.'}
    # extract the created ID for easier queries
    vibe_id = defs.insert_one(vibe_check).inserted_id
    pprint.pprint(defs.find_one({"_id": vibe_id}))
    print('-'*40)
    sys.stdout.close()
    sys.stdout = orig