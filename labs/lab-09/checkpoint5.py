from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime as dt
import pprint
client = MongoClient()
db = client['mongo_db_lab']
defs = db['definitions']


def random_word_requester():
    '''
    This function should return a random word and its definition and also
    log in the MongoDB database the timestamp that it was accessed.
    '''
    # perform a sample data aggregation
    rando = list(defs.aggregate([{'$sample': {'size': 1 }}]))[0]
    # update the list of definitions with the last accessed timestamp
    query = {'_id': rando.get('_id')}
    date = { "$push": { "dates": dt.utcnow().isoformat() } }
    defs.update_one(query, date)
    
    return rando

if __name__ == '__main__':
    # create a temporary collection to check for duplicates
    dupes = db['dupes']
    item = random_word_requester()
    # we keep getting random words until we find a dupe
    while dupes.count_documents({'_id': item.get('_id')}) <= 0:
        dupes.insert_one(item)
        item = random_word_requester()
    # get the dupe in the original collection
    duped = defs.find_one({'_id': item.get('_id')})
    pprint.pprint(duped)
    # remove the duplicate collection and remove
    # the dates field before exiting
    dupes.drop()
    defs.update_many({}, {'$unset': {'dates': ''}})
    
client.close()