import couchdb
import requests
import json
import time
import datetime

#host_ip = "192.168.1.116" # Note: if running locally, use the host machine IP
#host_ip = "172.26.132.19"
host_ip = "172.26.129.100" # replalce this with instance IP the server Running

# Get today's date
today = datetime.date.today()

# Format the date as a string in the desired format
date_string = today.strftime("%Y-%m-%d")
# Combine the date string with the CouchDB name prefix
db_name = "mastodon_" + date_string

# db_name = 'mastodon_test'

couch = couchdb.Server(f'http://admin:admin@{host_ip}:5984')
# db = couch['mastodon_policy']
db = couch[db_name]

def check_date_change():
    global today
    global date_string
    global db_name
    global db

    current_date = datetime.date.today()
    if current_date != today:
        today = current_date
        date_string = today.strftime("%Y-%m-%d")
        db_name = "mastodon_policy_" + date_string
        db = couch[db_name]

'''''
def get_latest_post(db,db_name):
    map_function = """
    function (doc) {
        emit(doc.created_at, doc);
    }
    """

    view_name = "latest_post"
    design_doc_name = "_design/post_view"

    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,
            "views": {
                view_name: {
                    "map": map_function
                }
            }
        }
        db.save(design_doc)
    else:
        design_doc = db[design_doc_name]
        if view_name not in design_doc["views"]:
            design_doc["views"][view_name] = {
                "map": map_function
            }
            db.save(design_doc)

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/post_view/_view/latest_post?descending=true&limit=1'
    response = requests.get(url)
    data = json.loads(response.text)
    latest_post = data['rows'][0]['value'] if data['rows'] else None
    return latest_post
'''''

def mastodon_post_total(db,db_name, design_name,view_name):
    map_function = """
    function (doc) {
        emit(doc._id,1)
    }
    """
    design_doc_name = "_design/"+design_name


    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,
            "views": {
                view_name: {
                    "map": map_function,
                    "reduce": "_sum"
                }
            }
        }
        db.save(design_doc)
    else:
        design_doc = db[design_doc_name]
        if view_name not in design_doc["views"]:
            design_doc["views"][view_name] = {
                "map": map_function,
                "reduce": "_sum"
            }
            db.save(design_doc)

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/{design_name}/_view/{view_name}?reduce=true'
    response = requests.get(url)
    data = json.loads(response.text)

    return data['rows'][0]['value']


def mastodon_user_total(db,db_name, design_name,view_name):
    map_function = """
    function (doc) {
        emit(doc.username,1)
    }
    """
    design_doc_name = "_design/"+design_name

    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,
            "views": {
                view_name: {
                    "map": map_function,
                    "reduce": "_count"
                }
            }
        }
        db.save(design_doc)
    else:
        design_doc = db[design_doc_name]
        if view_name not in design_doc["views"]:
            design_doc["views"][view_name] = {
                "map": map_function,
                "reduce": "_count"
            }
            db.save(design_doc)

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/{design_name}/_view/{view_name}?group=true'
    response = requests.get(url)
    data = json.loads(response.text)

    return len(data['rows'])

def mastodon_topic_post(db,db_name, design_name,view_name,map_function):
    design_doc_name = "_design/"+design_name

    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,
            "views": {
                view_name: {
                    "map": map_function,
                    "reduce": "_sum"
                }
            }
        }
        db.save(design_doc)
    else:
        design_doc = db[design_doc_name]
        if view_name not in design_doc["views"]:
            design_doc["views"][view_name] = {
                "map": map_function,
                "reduce": "_sum"
            }
            db.save(design_doc)

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/{design_name}/_view/{view_name}?reduce=true'
    response = requests.get(url)
    print(url)
    print(map_function)
    data = json.loads(response.text)
    print(data)
    count = data['rows'][0]['value']
    return count

def mastodon_topic_word(db,db_name, design_name,view_name,map_function):

    design_doc_name = "_design/"+design_name

    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,
            "views": {
                view_name: {
                    "map": map_function,
                    "reduce": "_count",
                }
            }
        }
        db.save(design_doc)
    else:
        design_doc = db[design_doc_name]
        if view_name not in design_doc["views"]:
            design_doc["views"][view_name] = {
                "map": map_function,
                "reduce": "_count",
            }
            db.save(design_doc)

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/{design_name}/_view/{view_name}?group=true'
    response = requests.get(url)
    data = json.loads(response.text)
    word_dict = dict()
    for row in data["rows"]:
        if row["key"] not in word_dict:
            word_dict[row["key"]] = row["value"]
    word_sort_dict = dict(sorted(word_dict.items(), key=lambda item: item[1], reverse=True))
    return word_sort_dict

def mastodon_topic_user_dict(db,db_name, design_name,view_name,map_function):
    design_doc_name = "_design/"+design_name

    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,
            "views": {
                view_name: {
                    "map": map_function,
                    "reduce": "_count"
                }
            }
        }
        db.save(design_doc)
    else:
        design_doc = db[design_doc_name]
        if view_name not in design_doc["views"]:
            design_doc["views"][view_name] = {
                "map": map_function,
                "reduce": "_count"
            }
            db.save(design_doc)

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/{design_name}/_view/{view_name}?group=true'
    # url = f"http://admin:admin@172.26.132.19:5984/mastodon_policy/_design/policy_view/_view/policy_count?reduce=true"
    response = requests.get(url)
    data = json.loads(response.text)
    user_dict = dict()
    for row in data['rows']:
        user_dict[row["key"]] = row["value"]
    sorted_user_dict = dict(sorted(user_dict.items(), key=lambda item: item[1], reverse=True))

    return sorted_user_dict


def map_post(field_name):
    map_function = f"""
        function (doc) {{
            if (doc.{field_name} == true) {{
                emit(doc._id, 1);
            }}
        }}
    """
    return map_function

def map_user(field_name):
    map_function = f"""
        function (doc) {{
            if (doc.{field_name} == true) {{
                emit(doc.username, 1);
            }}
        }}
    """
    return map_function


def map_word(field_name):
    map_function = f"""
        function (doc) {{
            if (doc.{field_name} == true) {{
                var words = doc.token.split('|');
                for (var i = 0; i < words.length; i++) {{
                    if (!/^\d+$/.test(words[i])) {{
                        emit(words[i], 1);
                    }}
                }}
            }}
        }}
    """
    return map_function


def get_topic_dictionary(db, db_name,date_string, topic_dict, topic, field_name):
        topic_dict['date'] = date_string

        # total users, not related to the topic selected
        topic_dict["total_post"] = mastodon_post_total(db,db_name,"total","post")
        topic_dict["total_user"] = mastodon_user_total(db,db_name,"total","user")

        # for topic related post information
        topic_dict['post_num'] = mastodon_topic_post(db,db_name, topic, "post",map_post(field_name))
        topic_dict["post_ratio"] = topic_dict["post_num"]/topic_dict["total_post"]

        # for topic word and the number of count, used for the word cloud
        topic_dict["wordmap"] = mastodon_topic_word(db,db_name,topic, "word",map_word(field_name))

        # for user information
        topic_dict["usermap"] = mastodon_topic_user_dict(db,db_name,topic, "user",map_user(field_name))
        topic_dict["user_num"] = len(topic_dict["usermap"])
        topic_dict["user_ratio"] = topic_dict["user_num"]/topic_dict["total_user"]

        #topic_dict['latest_post'] = get_latest_post(db,db_name)
        return topic_dict


def mastodon_topic_post_total(db,db_name, design_name,view_name):
    map_function = """
    function (doc) {
        if (doc.political_related == true || doc.criminal_related == true || doc.employment_related == true || doc.traffic_related == true){
            emit(doc._id,1)
        }
    }
    """

    design_doc_name = "_design/"+design_name


    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,
            "views": {
                view_name: {
                    "map": map_function,
                    "reduce": "_sum"
                }
            }
        }
        db.save(design_doc)
    else:
        design_doc = db[design_doc_name]
        if view_name not in design_doc["views"]:
            design_doc["views"][view_name] = {
                "map": map_function,
                "reduce": "_sum"
            }
            db.save(design_doc)

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/{design_name}/_view/{view_name}?reduce=true'
    response = requests.get(url)
    data = json.loads(response.text)

    return data['rows'][0]['value']

def mastodon_topic_user_total(db,db_name, design_name,view_name):
    map_function = """
    function (doc) {
        if (doc.political_related == true || doc.criminal_related == true || doc.employment_related == true || doc.traffic_related == true){
            emit(doc.username,1)
        }
    }
    """
    design_doc_name = "_design/"+design_name

    if design_doc_name not in db:
        design_doc = {
            "_id": design_doc_name,
            "views": {
                view_name: {
                    "map": map_function,
                    "reduce": "_count"
                }
            }
        }
        db.save(design_doc)
    else:
        design_doc = db[design_doc_name]
        if view_name not in design_doc["views"]:
            design_doc["views"][view_name] = {
                "map": map_function,
                "reduce": "_count"
            }
            db.save(design_doc)

    url = f'http://admin:admin@{host_ip}:5984/{db_name}/_design/{design_name}/_view/{view_name}?group=true'
    response = requests.get(url)
    data = json.loads(response.text)

    return len(data['rows'])


def get_total_dictionary(db,db_name,date_string, total_dic):
    total_dic['date'] = date_string

    # total users, not related to the political area selected
    total_dic["total_post"] = mastodon_post_total(db,db_name,"total","post")
    total_dic["total_user"] = mastodon_user_total(db,db_name,"total","user")

    total_dic['post_num'] = mastodon_topic_post_total(db,db_name, "total","topic_post")
    total_dic["user_num"] = mastodon_topic_user_total(db,db_name,"total","topic_user")

    total_dic['post_ratio'] = total_dic['post_num']/total_dic["total_post"]
    total_dic['user_ratio'] = total_dic["user_num"]/total_dic["total_user"]

    #total_dic['latest_post'] = get_latest_post(db,db_name)
    return total_dic


mastodon_total = {'host': host_ip, 'date': date_string, 'latest_post':{},
                   'total_post':0, 'total_user':0,
                   'post_num':0,'post_ratio':0,
                   'user_num':0,'user_ratio':0,
                   }



if __name__ == '__main__':
    time.sleep(1)
    while True:
        # Check if the date has changed
        check_date_change()

        # ############################### total #############################
        mastodon_total = get_total_dictionary(db,db_name,date_string, mastodon_total)
        #requests.post(f'http://localhost:8000/update_mastodon', json=mastodon_total)
        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_total)

        # ############################### policy topics #############################
        #mastodon_policy = get_topic_dictionary(db,db_name,date_string, mastodon_policy, "political", "political_related")

        ################################ criminal topics #############################
        #mastodon_criminal = get_topic_dictionary(db,db_name,date_string, mastodon_criminal, "criminal", "criminal_related")

        ################################ employment topics #############################
        #mastodon_employment = get_topic_dictionary(db,db_name,date_string, mastodon_employment, "employment", "employment_related")

        ################################ employment topics #############################
        #mastodon_traffic = get_topic_dictionary(db,db_name,date_string, mastodon_traffic, "traffic", "traffic_related")


        time.sleep(1)
