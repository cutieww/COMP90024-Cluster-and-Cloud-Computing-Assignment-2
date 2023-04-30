from mastodon import Mastodon, MastodonNotFoundError, MastodonRatelimitError, StreamListener
import os, time
import couchdb

host_ip = "172.26.128.252"

couch = couchdb.Server(f'http://admin:admin@{host_ip}:5984')

db = None

if 'db_test' in couch:
    db = couch['mastodon']
else:
    db = couch.create('mastodon')
#db = couch['db_test']

m = Mastodon(
    api_base_url=f'https://mastodon.world',
    #access_token=os.environ['MASTODON_ACCESS_TOKEN']
    access_token="dcD1nafa2HnRMEEPgflV3G0CAefvanb11nAsQiBcedY"
)


class Listener(StreamListener):
    def on_update(self, status):
        if status["language"] == "en":
            mastodon = {
                "username": status["account"]["username"],
                "content": status["content"],
                "url": status["url"]
            }
            #print(mastodon)
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
