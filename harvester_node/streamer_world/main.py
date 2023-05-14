from mastodon import Mastodon, MastodonNotFoundError, MastodonRatelimitError, StreamListener
import os, time
import re
import couchdb
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime
import requests

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('words')

host_ip = "172.26.128.252"
# host_ip = '127.0.0.1'
policy_bow = ["government","democracy",  "elections", "voting","campaigns","political parties","legislation", "policy", "administration", "diplomacy", "foreign policy","domestic policy", "public policy", "law",     "constitution",     "civil rights",     "civil liberties",     "social justice",     "equality",     "political ideology",     "political spectrum",     "lobbying",     "special interest groups",     "media",     "political commentary",     "political satire",     "corruption",     "transparency",     "accountability",     "political science",     "international relations",     "public opinion",     "propaganda",     "power",     "authority",     "leadership",     "governance",     "policy making",     "public administration",    "bureaucracy",    "campaign finance",    "censorship",    "checks and balances",    "citizenship",    "constituency",    "crisis management",    "debates",    "defamation",    "dictatorship",    "discrimination",    "divisiveness",    "economic policy",    "election security",    "emergency powers",    "fascism",    "freedom of speech",    "human rights",    "impeachment",    "judicial system",    "legislative branch",    "libertarianism",    "lobbyists",    "military",    "minorities",    "nationalism","patriotism","peacekeeping","political asylum","political correctness","political culture","political economy","political stability","populism","protest","public service","reform","representation","revolution","separation of powers","socialism","sovereignty","state","totalitarianism","veto","war","welfare state"]

criminal_bow = ['theft', 'robbery', 'burglary', 'fraud', 'embezzlement', 'forgery', 'extortion', 'blackmail', 'smuggling', 'money laundering', 'racketeering', 'homicide', 'assault', 'kidnapping', 'arson', 'drug trafficking', 'prostitution', 'gambling', 'terrorism', 'cybercrime', 'piracy', 'carjacking', 'vandalism', 'shoplifting', 'pickpocketing', 'cyberbullying', 'hate crime', 'white-collar crime', 'organized crime', 'juvenile delinquency', 'prison', 'parole', 'probation', 'criminal record', 'suspect', 'defendant', 'convict', 'witness', 'prosecutor', 'defense attorney', 'judge', 'jury', 'plea bargain', 'sentencing', 'probation officer', 'correctional facility', 'parole board', 'inmate', 'parolee', 'fugitive', 'surveillance', 'wiretap', 'sting operation', 'forensic','evidence', 'DNA', 'investigation']

employment_bow = ['career', 'profession', 'resume', 'CV', 'interview', 'compensation', 'workplace', 'coworker', 'supervisor', 'manager', 'networking', 'diversity', 'harassment', 'opportunity', 'laws', 'overtime', 'sick leave', 'vacation', 'retirement', 'pension', 'severance', 'unemployment', 'loss', 'security', 'gig', 'freelancing', 'entrepreneurship', 'advancement', 'development', 'growth', 'goals', 'balance', 'insurance', 'program', 'maternity', 'paternity', 'child care', 'scheduling', 'telecommuting', 'metrics', 'incentives', 'bonuses', 'turnover', 'unions', 'contracts', 'agreements', 'termination', 'lawsuits', 'safety', 'culture', 'ethics', 'inclusion', 'resources', 'staffing', 'boards', 'fairs', 'associations', 'shadowing', 'mentorship', 'leadership', 'apprenticeships', 'internships', 'co-op']

traffic_bow = ['vehicle', 'driver', 'road', 'highway', 'street', 'lane', 'intersection', 'stoplight', 'stop sign', 'yield sign', 'speed limit', 'traffic signal', 'pedestrian', 'crosswalk', 'sidewalk', 'parking', 'parking lot', 'parking meter', 'public transit', 'bus', 'train', 'subway', 'light rail', 'bike lane', 'carpool', 'commute', 'congestion', 'accident', 'collision', 'tow truck', 'highway patrol', 'traffic jam', 'detour', 'roadwork', 'construction', 'bridge', 'tunnel', 'toll road', 'expressway', 'roundabout', 'lane closure', 'merge', 'yield', 'U-turn', 'speed bump', 'traffic circle', 'interchange', 'overpass', 'underpass', 'median', 'shoulder', 'off-ramp', 'on-ramp']


couch = couchdb.Server(f'http://admin:admin@{host_ip}:5984')
today = datetime.today().strftime('%Y-%m-%d')



db_name = 'mastodon' + "_" + today
db = None

if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)
#db = couch['db_test']

m = Mastodon(
    api_base_url=f'https://mastodon.world',
    #access_token=os.environ['MASTODON_ACCESS_TOKEN']
    access_token="dcD1nafa2HnRMEEPgflV3G0CAefvanb11nAsQiBcedY"
)

def create_database(date):
    global db_name, db
    today = date
    db_name = 'mastodon_' + "_" + today

    if db_name in couch:
        db = couch[db_name]
    else:
        db = couch.create(db_name)

class Listener(StreamListener):
    def to_root_words(self, bow):
        lemmatizer = WordNetLemmatizer()
        ps = PorterStemmer()
        root_list = []
        for words in bow:
            words_split = words.split(' ')
            for word in words_split:
                new_word = word.lower()
                new_word = ps.stem(new_word)
                new_word = lemmatizer.lemmatize(new_word)
                root_list.append(new_word)
        # root_list = [lemmatizer.lemmatize(word) for word in root_list]
        # bow = [word.lower() for word in bow]
        # root_list = [lemmatizer.lemmatize(word) for word in bow]
        # root_list = [ps.stem(word) for word in root_list]
        return list(set(root_list))

    def check_include_topic(self,input_string,topic_bow):
        # remove the suffix and prefix
        # topic_bow_remove = remove_prefix(topic_bow)
        topic_bow_remove = self.to_root_words(topic_bow)
        input = re.findall(r'\w+', input_string)

        # convert to all lower case
        input = [word.lower() for word in input]
        input_remove = self.to_root_words(input)
        policy_words = [word for word in input_remove if word in topic_bow_remove]
        
        return policy_words
    
    def to_token(self, content):
      pattern = r"<p>(.*?)</p>"
      content_list = re.findall(pattern, content)
      
      text_list = []
      stop_words = set(stopwords.words('english'))
      english_words_set = set(nltk.corpus.words.words())
      for lst in content_list:
        # remove all the HTML tags
        pattern2 = r"<a\b[^>]*>(.*?)</a>"
        text = re.sub(pattern2, "", lst)
        

        # Remove HTML tags using re.sub()
        pattern3 = re.compile(r'<.*?>')
        text = re.sub(pattern3, '', text)

        

        # Remove punctuations and "'s" using re.sub()
        pattern4 = re.compile(r'[^\w\s]|\'s')
        text = re.sub(pattern4, '', text)

        # print(text)

        token_list = word_tokenize(text)



        filtered_token_list = [word.lower() for word in token_list if word.lower() not in stop_words and word.lower() in english_words_set]
        text_list.extend(filtered_token_list)
      return "|".join(text_list)
    
    def update_database_if_needed(self):
        global today, db
        current_date = datetime.today().strftime('%Y-%m-%d')
        if current_date != today:
            create_database(current_date)
            today = current_date
            db = couch[db_name]

    def on_update(self, status):
        # message = json.dumps(status, indent=2, sort_keys=True,default=str)
        # print(message[0])
        self.update_database_if_needed()


        if status['language'] == 'en':
            token = self.to_token(status["content"])
            political_related = False
            criminal_related = False
            employment_related = False
            traffic_related = False
            if self.check_include_topic(token,policy_bow) != []:
                political_related = True
            elif self.check_include_topic(token,criminal_bow) != []:
                criminal_related = True
            elif self.check_include_topic(token,employment_bow) != []:
                employment_related = True
            elif self.check_include_topic(token,traffic_bow) != []:
                traffic_related = True

            doc = {
                "username": status["account"]["username"],
                "token": token,
                "created_at": status["created_at"].isoformat(),
                "favourites_count" : status["favourites_count"],
                "reblogs_count": status["reblogs_count"],
                "replies_count":status["replies_count"],
                "political_related":political_related,
                "criminal_related": criminal_related,
                "employment_related": employment_related,
                "traffic_related": traffic_related,
            }


            # Test if the API is open and send the mastodon_post dict
            mastodon_post = {"username": status["account"]["username"],
                            'content': status["content"],
                            "created_at": status["created_at"].isoformat(),
                            "political_related":political_related,
                            "criminal_related": criminal_related,
                            "employment_related": employment_related,
                            "traffic_related": traffic_related,
                            "url": status["url"],
                            "server": "mastodon.world"
                            }

            host_ips = ["172.26.129.100", "172.26.132.19"]

            for host_ip in host_ips:
                try:
                    response = requests.post(f'http://{host_ip}:8000/update_mastodon_post', json=mastodon_post, timeout=2.0)
                    if response.status_code == 200:
                        print(f"Data sent to API at {host_ip} successfully")
                    else:
                        print(f"Error sending data to API at {host_ip}. Status code: {response.status_code}")
                except requests.exceptions.RequestException as exc:
                    print(f"Error sending data to API at {host_ip}: {exc}")

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
