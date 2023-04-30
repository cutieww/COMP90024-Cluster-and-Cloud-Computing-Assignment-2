# api_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
async def root():
    return {'name': 'api to connect to react'}

mastodon_data = {'number': 0}
@app.get('/mastodon_data')
async def get_data():
    return mastodon_data

@app.post('/update_mastodon')
async def update_data(update_data: dict):
    global mastodon_data
    mastodon_data = update_data