import couchdb
import requests
import json
import time
import datetime
import itertools

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
    data = json.loads(response.text)
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











mastodon_policy = {'host': host_ip, 'date': date_string, 'latest_post':{},
                   'total_post':0, 'total_user':0,
                   'post_num':0,'post_ratio':0, 'wordmap':{},
                   'user_num':0,'user_ratio':0,'usermap':{},
                   }


mastodon_criminal = {'host': host_ip, 'date': date_string, 'latest_post':{},
                   'total_post':0, 'total_user':0,
                   'post_num':0,'post_ratio':0, 'wordmap':{},
                   'user_num':0,'user_ratio':0,'usermap':{},
                   }


mastodon_employment = {'host': host_ip, 'date': date_string, 'latest_post':{},
                   'total_post':0, 'total_user':0,
                   'post_num':0,'post_ratio':0, 'wordmap':{},
                   'user_num':0,'user_ratio':0,'usermap':{},
                   }

mastodon_traffic = {'host': host_ip, 'date': date_string, 'latest_post':{},
                   'total_post':0, 'total_user':0,
                   'post_num':0,'post_ratio':0, 'wordmap':{},
                   'user_num':0,'user_ratio':0,'usermap':{},
                   }


if __name__ == '__main__':
    time.sleep(1)
    while True:
        # Check if the date has changed
        check_date_change()
        total_post = mastodon_post_total(db,db_name,"total","post")
        total_user = mastodon_user_total(db,db_name,"total","user")





        ############################### policy topics #############################
        mastodon_policy['date'] = date_string

        # total users, not related to the political area selected
        mastodon_policy["total_post"] = total_post
        mastodon_policy["total_user"] = total_user


        # for topic related post information 
        mastodon_policy['post_num'] = mastodon_topic_post(db,db_name, "political", "post",map_post("political_related"))
        mastodon_policy["post_ratio"] = mastodon_policy["post_num"]/mastodon_policy["total_post"]

        # for political word and the number of count, used for the word cloud
        mastodon_policy["wordmap"] = mastodon_topic_word(db,db_name,"political", "word",map_word("political_related"))


        # for user information
        mastodon_policy["usermap"] = mastodon_topic_user_dict(db,db_name,"political", "user",map_user("political_related"))
        mastodon_policy["user_num"] = len(mastodon_policy["usermap"])
        mastodon_policy["user_ratio"] = mastodon_policy["user_num"]/mastodon_policy["total_user"]

        mastodon_policy['latest_post'] = get_latest_post(db,db_name)


        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_policy)



        ############################### criminal topics #############################
        mastodon_criminal['date'] = date_string

        # total users, not related to the criminal area selected
        mastodon_criminal["total_post"] = total_post
        mastodon_criminal["total_user"] = total_user


        # for topic related post information 
        mastodon_criminal['post_num'] = mastodon_topic_post(db,db_name, "criminal", "post",map_post("criminal_related"))
        mastodon_criminal["post_ratio"] = mastodon_criminal["post_num"]/mastodon_criminal["total_post"]

        # for criminal word and the number of count, used for the word cloud
        mastodon_criminal["wordmap"] = mastodon_topic_word(db,db_name,"criminal", "word",map_word("criminal_related"))


        # for user information
        mastodon_criminal["usermap"] = mastodon_topic_user_dict(db,db_name,"criminal", "user",map_user("criminal_related"))
        mastodon_criminal["user_num"] = len(mastodon_criminal["usermap"])
        mastodon_criminal["user_ratio"] = mastodon_criminal["user_num"]/mastodon_criminal["total_user"]

        mastodon_criminal['latest_post'] = get_latest_post(db,db_name)
        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_criminal)
        

        ############################### employment topics #############################
        mastodon_employment['date'] = date_string

        # total users, not related to the employment area selected
        mastodon_employment["total_post"] = total_post
        mastodon_employment["total_user"] = total_user


        # for topic related post information 
        mastodon_employment['post_num'] = mastodon_topic_post(db,db_name, "employment", "post",map_post("employment_related"))
        mastodon_employment["post_ratio"] = mastodon_employment["post_num"]/mastodon_employment["total_post"]

        # for employment word and the number of count, used for the word cloud
        mastodon_employment["wordmap"] = mastodon_topic_word(db,db_name,"employment", "word",map_word("employment_related"))


        # for user information
        mastodon_employment["usermap"] = mastodon_topic_user_dict(db,db_name,"employment", "user",map_user("employment_related"))
        mastodon_employment["user_num"] = len(mastodon_employment["usermap"])
        mastodon_employment["user_ratio"] = mastodon_employment["user_num"]/mastodon_employment["total_user"]

        mastodon_employment['latest_post'] = get_latest_post(db,db_name)
        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_employment)



        ############################### traffic topics #############################
        mastodon_traffic['date'] = date_string

        # total users, not related to the traffic area selected
        mastodon_traffic["total_post"] = total_post
        mastodon_traffic["total_user"] = total_user


        # for topic related post information 
        mastodon_traffic['post_num'] = mastodon_topic_post(db,db_name, "traffic", "post",map_post("traffic_related"))
        mastodon_traffic["post_ratio"] = mastodon_traffic["post_num"]/mastodon_traffic["total_post"]

        # for traffic word and the number of count, used for the word cloud
        mastodon_traffic["wordmap"] = mastodon_topic_word(db,db_name,"traffic", "word",map_word("traffic_related"))


        # for user information
        mastodon_traffic["usermap"] = mastodon_topic_user_dict(db,db_name,"traffic", "user",map_user("traffic_related"))
        mastodon_traffic["user_num"] = len(mastodon_traffic["usermap"])
        mastodon_traffic["user_ratio"] = mastodon_traffic["user_num"]/mastodon_traffic["total_user"]

        mastodon_traffic['latest_post'] = get_latest_post(db,db_name)
        requests.post(f'http://{host_ip}:8000/update_mastodon', json=mastodon_traffic)

        print(mastodon_traffic)


        time.sleep(1)
