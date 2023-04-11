from elasticsearch import Elasticsearch
from pymongo import MongoClient
import uuid


class ElasticClient:
    index = "face-index-test2"
    prefix = 100000

    def __init__(self):
        self.es = Elasticsearch(
            cloud_id='face_encodings'
                     ':dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGYwYzM4ODdjYzY5ZTQ'
                     '2Zjg5ZmI0NWVkM2I4YmExOGJiJDBmOGYwNzJjZmI1OTQ0YTZiYjBjN2JlMzA0YjY5Mzhj',
            basic_auth=("elastic", "TfxiPjcyAfr1dEzThjPNHrwd"), timeout=3000)


    def find_by_encoding(self, encoding):
        body = {
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": self.get_script_query(encoding)
                    }
                }
            },
            "size": 5,
            "sort": [
                {"_score": "asc"}
            ],
        }

        data = self.es.search(
            index=self.index,
            body=body
        )
        return data['hits']['hits']

    def get_script_query(self, encoding):
        checker = False
        query = ''
        for inp in range(0, len(encoding)):
            value = int(self.prefix * encoding[inp])
            sub_query = 'Math.pow(doc["enc' + str(inp) + '"].value-(' + str(value) + '),2)'
            if checker:
                sub_query = '+' + sub_query
            else:
                checker = True
            query += sub_query
        print(query)
        return query

# es = ElasticClient()
#
# test_encoding = [-0.11515828967094421, 0.04626104608178139, -0.0029525314457714558, -0.1125202551484108, -0.10542210191488266, -0.07095017284154892, -0.041845668107271194, -0.08616197109222412, 0.17074036598205566, -0.048287443816661835, 0.11630479991436005, -0.11873579770326614, -0.17688217759132385, 0.039943281561136246, -0.10712291300296783, 0.16903246939182281, -0.17557692527770996, -0.12275120615959167, -0.13064076006412506, -0.07009013742208481, 0.08620762825012207, 0.04681944102048874, 0.04076594486832619, 0.12090165913105011, -0.16277475655078888, -0.291547030210495, -0.021515101194381714, -0.04960564896464348, -0.07444470375776291, -0.029113007709383965, 0.07388372719287872, 0.15137392282485962, -0.1462668627500534, -0.026877008378505707, 0.03298640996217728, 0.13800916075706482, 0.0015112326946109533, -0.08608631789684296, 0.19957061111927032, 0.012662200257182121, -0.23155128955841064, -0.04855396971106529, 0.14699940383434296, 0.3219479024410248, 0.2201181948184967, 0.06000621244311333, 0.02702433057129383, -0.0446692556142807, 0.14558477699756622, -0.36228030920028687, -0.02642574906349182, 0.1729198694229126, 0.008920376189053059, 0.09291927516460419, 0.05291108042001724, -0.12620975077152252, 0.11072342842817307, 0.1056390330195427, -0.19812190532684326, -0.02470455691218376, 0.06858550012111664, -0.06205867603421211, 0.04234170913696289, -0.13453517854213715, 0.2902788519859314, 0.07159010320901871, -0.17904852330684662, -0.01168186403810978, 0.10340628772974014, -0.164313405752182, -0.09726192057132721, -0.00438992353156209, -0.15518227219581604, -0.22963912785053253, -0.3854663074016571, -0.026623431593179703, 0.3570061922073364, 0.1953568011522293, -0.07643289864063263, 0.12072853744029999, -0.02829982154071331, 0.020890235900878906, 0.0014566200552508235, 0.15777547657489777, -0.05362473055720329, 0.09858386218547821, -0.04465359449386597, 0.07102998346090317, 0.2126714587211609, -0.05645318329334259, -0.015720924362540245, 0.26798495650291443, 0.04575980454683304, -0.021252507343888283, -0.03052402101457119, 0.08489605784416199, -0.08442801237106323, 0.014673011377453804, -0.15366418659687042, 0.11258478462696075, 0.013688832521438599, 0.03298120200634003, 0.06921728700399399, 0.06805090606212616, -0.2140461504459381, 0.17655779421329498, -0.035525187849998474, -0.03234962373971939, -0.103345587849617, -0.056716188788414, -0.06305188685655594, -0.008703477680683136, 0.1405051201581955, -0.21966032683849335, 0.0900280624628067, 0.20614735782146454, 0.09492401033639908, 0.1954926997423172, 0.0766996443271637, 0.03250827640295029, 0.02907717600464821, 0.03479669988155365, -0.12039943039417267, -0.05261191353201866, 0.06544521450996399, -0.02901775762438774, 0.050836097449064255, 0.11910975724458694]
# # print(es.get_script_query(test_encoding))
# print(es.find_by_encoding(test_encoding))




# {"encoding": face_code['data'], "document_id": document_id, "image_hash": hash}
# [{'name': 'telman amirli', 'provider': 'OK', 'id': '572845747758'},
# {'name': 'Sinan Eliyev', 'provider': 'OK', 'id': '583673415070'},
# {'name': 'Ruslan Babayev', 'provider': 'OK', 'id': '599266054430'},
# {'name': 'zaur sahvarli', 'provider': 'OK', 'id': '539121439120'},
# {'name': 'Сеймур 42', 'provider': 'OK', 'id': '583784944784'},
# {'name': 'Zahid Kerimov', 'provider': 'OK', 'id': '596865901884'},
# {'name': 'Yadigar Ferzeliyev', 'provider': 'OK', 'id': '511205876044'},
# {'name': 'mr Miri', 'provider': 'OK', 'id': '351641759878'},
# {'name': 'Qamet Sariyev', 'provider': 'OK', 'id': '572776057115'},
# {'name': 'Coşqun Fərəcov', 'provider': 'OK', 'id': '553071815935'},
# {'name': 'olqa vasilevna', 'provider': 'OK', 'id': '584571800768'},
# {'name': 'SevindiK 213', 'provider': 'OK', 'id': '549094280105'},
# {'name': 'Amid M', 'provider': 'OK', 'id': '562675783262'},
# {'name': 'Ofelya Əhməd', 'provider': 'OK', 'id': '586006507461'},
# {'name': 'P A', 'provider': 'OK', 'id': '594497309954'},
# {'name': 'tural ezizov', 'provider': 'OK', 'id': '573525716568'},
# {'name': '《T◇Ə◇N◇H◇A》 98', 'provider': 'OK', 'id': '572306948506'},
# {'name': 'ELSHAN MUSTAFAEV', 'provider': 'OK', 'id': '565544210863'},
# {'name': 'şaka Məmmədli', 'provider': 'OK', 'id': '571059359678'},
# {'name': 'Alex Fire', 'provider': 'OK', 'id': '573219016569'},
# {'name': 'Mark Tven', 'provider': 'OK', 'id': '532803675838'}, {
# 'name': 'Ильхам Гусейнов', 'provider': 'OK', 'id': '567357948952'},
# {'name': 'Fariz mustafayev', 'provider': 'OK', 'id': '590215620390'},
# {'name': 'Fezail Quliyev', 'provider': 'OK', 'id': '592796274227'},
# {'name': 'Mircavadll  Ramin', 'provider': 'OK', 'id': '572952241275'},
# {'name': 'aftandil ibrahimov', 'provider': 'OK', 'id': '536882873769'},
# {'name': 'huseyn qemberov', 'provider': 'OK', 'id': '562538120650'},
# {'name': 'Елдар Eliyev', 'provider': 'OK', 'id': '549541115130'},
# {'name': 'Elwad Memmedov', 'provider': 'OK', 'id': '580574170118'},
# {'name': 'Elxan Sеrdаrov', 'provider': 'OK', 'id': '546168482103'},
# {'name': 'BH8089 V B T', 'provider': 'OK', 'id': '574553369726'},
# {'name': 'Alem -747', 'provider': 'OK', 'id': '545603952253'},
# {'name': 'Edik Kuliyev', 'provider': 'OK', 'id': '580545701274'},
# {'name': 'Rafayıl Mecidov', 'provider': 'OK', 'id': '586061350593'},
# {'name': 'bbbb eeee', 'provider': 'OK', 'id': '534563220895'},
# {'name': 'Natiq Huseynov', 'provider': 'OK', 'id': '562514668735'},
# {'name': 'Sakit Deniz', 'provider': 'OK', 'id': '576860761739'},
# {'name': 'Arif Şükürov', 'provider': 'OK', 'id': '579929853635'},
# {'name': 'Elina M-ova', 'provider': 'OK', 'id': '583525015528'},
# {'name': 'Elsəvəri 🤟', 'provider': 'OK', 'id': '576008211271'},
# {'name': 'Евгений Перескоков', 'provider': 'OK', 'id': '365252719775'},
# {'name': 'Sena SENA', 'provider': 'OK', 'id': '565825786605'},
# {'name': 'Намик Ханмедов', 'provider': 'OK', 'id': '560818788387'},
# {'name': 'Həyat davam Edir', 'provider': 'OK', 'id': '579784586362'},
# {'name': 'Hamid Nuruyev', 'provider': 'OK', 'id': '572296868779'},
# {'name': 'Намик Алиев', 'provider': 'OK', 'id': '578848474819'},
# {'name': 'V FF', 'provider': 'OK', 'id': '597240206127'},
# {'name': 'Aydın Mamedov', 'provider': 'OK', 'id': '584752288130'},
# {'name': '👑NAZLİ PASAYEVA', 'provider': 'OK', 'id': '568818837640'},
# {'name': 'VIRTUAL SENStive QASPOJA', 'provider': 'OK', 'id': '580744618347'},
# {'name': '💘💘💘 ♥️♥️♥️', 'provider': 'OK', 'id': '578464959084'},
# {'name': 'Samir Muradov', 'provider': 'OK', 'id': '575441012895'},
# {'name': 'Senli Geceler', 'provider': 'OK', 'id': '585343370472'},
# {'name': '❤LiNa ❤', 'provider': 'OK', 'id': '579597997938'},
# {'name': 'MƏNASIZ HƏYAT KAMRAN', 'provider': 'OK', 'id': '573787202670'},
# {'name': 'E N', 'provider': 'OK', 'id': '596709963825'},
# {'name': 'Aydan Eliyeva', 'provider': 'OK', 'id': '570052708983'},
# {'name': 'Samir   ⚜️389🔗 Qurbanov', 'provider': 'OK', 'id': '579668577654'},
# {'name': 'Zara 💖krasavisa', 'provider': 'OK', 'id': '585432439734'},
# {'name': 'Вольная борьба- лучший вид спорта', 'provider': 'OK', 'id': '570102199268'},
# {'name': 'GUNAY GUNAY', 'provider': 'OK', 'id': '580789627203'},
# {'name': 'Canan Canan', 'provider': 'OK', 'id': '579341549691'},
# {'name': 'Guliyeffa A', 'provider': 'OK', 'id': '578135979415'},
# {'name': '❤ ㅤㅤㅤㅤㅤㅤ❤', 'provider': 'OK', 'id': '579865124560'},
# {'name': 'No Name', 'provider': 'OK', 'id': '578231281092'},
# {'name': 'havin agayeva', 'provider': 'OK', 'id': '555208585296'},
# {'name': '❤Лезгинка ❤', 'provider': 'OK', 'id': '553404954487'},
# {'name': 'AY-Nur ▪️▪️▪️▪️', 'provider': 'OK', 'id': '583632643738'},
# {'name': 'Mavi Elnur Aliyeva', 'provider': 'OK', 'id': '576885895324'},
# {'name': '🦋Rüzgar Gülü🦋', 'provider': 'OK', 'id': '593194874147'},
# {'name': 'ƏLİ Bakixanov', 'provider': 'OK', 'id': '599600742174'},
# {'name': 'Gulay G', 'provider': 'OK', 'id': '581876188822'},
# {'name': '02 ❤', 'provider': 'OK', 'id': '575859404222'},
# {'name': '14 09', 'provider': 'OK', 'id': '579686122074'},
# {'name': 'Telebeyem Goruntulu 10 azn', 'provider': 'OK', 'id': '583355591126'},
# {'name': 'Luna Luppo', 'provider': 'OK', 'id': '577705716050'},
# {'name': 'Leyla Həmidova', 'provider': 'OK', 'id': '579752238431'},
