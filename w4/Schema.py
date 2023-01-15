from pymongo import MongoClient
client = MongoClient('localhost:27017')
SearchEngine = client['SearchEngine']
dbweb = SearchEngine['WebDB']

def create_collection(coll_name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test
    result = db.create_collection(coll_name, validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'additionalProperties': True,
            'required': ['component', 'path'],
            'properties': {
                'component': {
                    'bsonType': 'string'
                },
                'path': {
                    'bsonType': 'string',
                    'description': 'Set to default value'
                }
            }
        }
    })

    print(result)


if __name__ == '__main__':
    create_collection('my_coll')