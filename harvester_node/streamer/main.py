from mastodon import Mastodon, MastodonNotFoundError, MastodonRatelimitError, StreamListener
import os, time
import couchdb

couch = couchdb.Server('http://admin:admin@localhost:5984')

db = None

if 'db_test' in couch:
    db = couch['db_test']
else:
    db = couch.create('db_test')
#db = couch['db_test']

m = Mastodon(
    api_base_url=f'https://mastodon.world',
    access_token=os.environ['MASTODON_ACCESS_TOKEN']
)


class Listener(StreamListener):
    def on_update(self, status):
        if status["language"] == "en":
            mastodon = {
                "username": status["account"]["username"],
                "content": status["content"],
                "url": status["url"]
            }
            print(mastodon)
            doc = {
                "username": status["account"]["username"],
                "content": status["content"],
                "url": status["url"]
            }
            db.save(doc)


def start_mastodon_stream():
    while True:
        try:
            m.stream_public(Listener())
        except (MastodonNotFoundError, MastodonRatelimitError) as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait 60 seconds before retrying

if __name__ == '__main__':
    start_mastodon_stream()
