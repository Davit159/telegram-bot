from elastic import ElasticClient
import requests
import json
from pymongo import MongoClient
from bson.objectid import ObjectId


class Searcher:
    ec = ElasticClient()

    mongo_client = MongoClient("mongodb://admin:8YqNhQoJNrZzYeHh3z3XaI6@localhost:21018")
    el = ElasticClient()
    database = mongo_client['as']

    accounts = database['accounts']

    def search_by_image_url(self, image_url):
        print('start searching')
        response = requests.get('http://localhost:8000/face-encode?image_url=' + image_url)
        encodings = json.loads(response.content)
        data = []
        images = []
        for face_encoding in encodings['face_encodings']:
            print(face_encoding)
            like_faces = self.ec.find_by_encoding(face_encoding['data'])
            for like_face in like_faces:
                for i in range(10):
                    print(like_face['_score'])
                if like_face['_score'] < 1335126780:
                    print(like_face['_source']['document_id'])
                    data.append(ObjectId(like_face['_source']['document_id']))
                    images.append(like_face['_source']['image_hash'])
        return {"accounts": self.get_accounts_by_ids(data), "images": images}

    def get_accounts_by_ids(self, doc_ids):
        documents = self.accounts.find({'_id': {'$in': doc_ids}})
        accounts = []
        for doc in documents:
            print(doc)
            images_data = {}
            for image in doc["images"]:
                images_data[image["hash"]] = image["image_url"]
            accounts.append({"name": doc["name"], "provider": doc["provider"], "id": doc["id"], "images": images_data})

        return accounts
