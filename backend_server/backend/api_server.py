# api_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mastodon_process import mastodon_total_count, mastodon_user_count, mastodon_count, mastodon_user_total, host_ip
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
def get_data_by_date_from_db(date):
    # Replace 'db' with the CouchDB instance for the specified date
    db_name = "mastodon_policy_" + date
    db = couch[db_name]

    total_count = mastodon_total_count(db, db_name)
    mastodon_user = mastodon_user_count(db, db_name)
    total = mastodon_count(db, db_name)
    user_total = mastodon_user_total(db, db_name)

    data = {
        'date': date,
        'count': total_count,
        'total_post': total,
        'post_ratio': total_count / total,
        'user_ratio': len(mastodon_user) / user_total,
        'user_total': user_total,
        'mastodon_user': mastodon_user
    }

    return data

mastodon_data = {}
mastodon_map ={}

@app.get('/')
async def root():
    return {'name': 'api to connect to react'}


@app.get('/mastodon_data')
async def get_data():
    return mastodon_data

@app.get('/mastodon_data/date/{date}')
async def get_data_by_date(date: str):
    data = get_data_by_date_from_db(date)
    return data

@app.get('/mastodon_data/all')
async def get_all_data():
    COUCHDB_SERVER_URL = f'http://admin:admin@{host_ip}:5984/'
    async with httpx.AsyncClient() as client:
        response = await client.get(COUCHDB_SERVER_URL + '_all_dbs')
        all_dbs = response.json()
    policy_dbs = [db_name for db_name in all_dbs if db_name.startswith('mastodon_policy_')]
    integrated_data = {
        'count': 0,
        'total_post': 0,
        'user_count': 0,
        'user_total': 0,
    }

    for db_name in policy_dbs:
        date = db_name.split('_')[-1]
        data = get_data_by_date_from_db(date)
        integrated_data['count'] += data['count']
        integrated_data['total_post'] += data['total_post']
        integrated_data['user_count'] += len(data['mastodon_user'])
        integrated_data['user_total'] += data['user_total']

    if integrated_data['total_post'] > 0:
        integrated_data['post_ratio'] = integrated_data['count'] / integrated_data['total_post']
    else:
        integrated_data['post_ratio'] = 0

    if integrated_data['user_total'] > 0:
        integrated_data['user_ratio'] = integrated_data['user_count'] / integrated_data['user_total']
    else:
        integrated_data['user_ratio'] = 0

    return integrated_data

@app.get('/mastodon_map')
async def get_data():
    return mastodon_map

@app.post('/update_mastodon')
async def update_data(update_data: dict):
    global mastodon_data
    mastodon_data = update_data


@app.post('/update_mastodon_map')
async def update_data(update_data: dict):
    global mastodon_map
    mastodon_map = update_data