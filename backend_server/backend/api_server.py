# api_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mastodon_process import get_topic_dictionary, get_total_dictionary, host_ip
import couchdb
import httpx


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

couch = couchdb.Server(f'http://admin:admin@{host_ip}:5984')

mastodon_total = {'host': host_ip, 'date': "date_string",
                   'total_post':0, 'total_user':0,
                   'post_num':0,'post_ratio':0,
                   'user_num':0,'user_ratio':0,
                   }


mastodon_policy = {'host': host_ip, 'date': "date_string",
                   'total_post':0, 'total_user':0,
                   'post_num':0,'post_ratio':0, 'wordmap':{},
                   'user_num':0,'user_ratio':0,'usermap':{},
                   }


mastodon_criminal = {'host': host_ip, 'date': "date_string",
                   'total_post':0, 'total_user':0,
                   'post_num':0,'post_ratio':0, 'wordmap':{},
                   'user_num':0,'user_ratio':0,'usermap':{},
                   }


mastodon_employment = {'host': host_ip, 'date': "date_string",
                   'total_post':0, 'total_user':0,
                   'post_num':0,'post_ratio':0, 'wordmap':{},
                   'user_num':0,'user_ratio':0,'usermap':{},
                   }


mastodon_traffic = {'host': host_ip, 'date': "date_string",
                   'total_post':0, 'total_user':0,
                   'post_num':0,'post_ratio':0, 'wordmap':{},
                   'user_num':0,'user_ratio':0,'usermap':{},
                   }


mastodon_data = {}
mastodon_post = {}

@app.get('/')
async def root():
    return {'name': 'api to connect to react'}


@app.get('/mastodon_data')
async def get_data():
    mastodon_data['latest_post'] = mastodon_post
    return mastodon_data

@app.get('/mastodon_data/query/{topic}/{date}')
async def query_data(topic: str, date: str):
    db_name = "mastodon_" + date
    db = couch[db_name]
    topic = topic
    topic_dict = {}
    field_name = ''
    if topic == "political":
        topic_dict = mastodon_policy
        field_name = "political_related"
    elif topic == "criminal":
        topic_dict = mastodon_criminal
        field_name = "criminal_related"
    elif topic == "employment":
        topic_dict = mastodon_employment
        field_name = "employment_related"
    elif topic == "traffic":
        topic_dict = mastodon_traffic
        field_name = "traffic_related"
    else:
        print('error for matching the topic in api sercer')

    data = get_topic_dictionary(db, db_name, date, topic_dict, topic, field_name)
    return data

@app.get('/mastodon_data/all')
async def get_all_data():
    COUCHDB_SERVER_URL = f'http://admin:admin@{host_ip}:5984/'
    async with httpx.AsyncClient() as client:
        response = await client.get(COUCHDB_SERVER_URL + '_all_dbs')
        all_dbs = response.json()
    dbs = [db_name for db_name in all_dbs if db_name.startswith('mastodon_')]

    integrated_data = {
        'total_post': 0,
        'total_user': 0,
        'post_num':0,
        'user_num': 0
    }

    for db_name in dbs:
        date = db_name.split('_')[-1]
        db = couch[db_name]
        data = get_total_dictionary(db,db_name, date, mastodon_total)
        print(data)
        integrated_data['post_num'] += data['post_num']
        integrated_data['total_post'] += data['total_post']
        integrated_data['user_num'] += data['user_num']
        integrated_data['total_user'] += data['total_user']

    if integrated_data['total_post'] > 0:
        integrated_data['post_ratio'] = integrated_data['post_num'] / integrated_data['total_post']
    else:
        integrated_data['post_ratio'] = 0

    if integrated_data['total_user'] > 0:
        integrated_data['user_ratio'] = integrated_data['user_num'] / integrated_data['total_user']
    else:
        integrated_data['user_ratio'] = 0

    return integrated_data

@app.post('/update_mastodon')
async def update_data(update_data: dict):
    global mastodon_data
    mastodon_data = update_data

@app.post('/update_mastodon_post')
async def update_data(update_data: dict):
    global mastodon_post
    mastodon_post = update_data