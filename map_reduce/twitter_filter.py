from collections import Counter
from mpi4py import MPI
import json, os, re
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from collections import defaultdict
import ijson

SAL_file = 'C:/Users/81409/OneDrive/桌面/CCC/sal.json'
sal = json.load(open(SAL_file, encoding='utf-8'))
TWEET_FILE = "D:/ccc/mnt/ext100/twitter-huge.json"
policy_bow = ["government","democracy",  "elections", "voting","campaigns","political parties","legislation", "policy", "administration", "diplomacy", "foreign policy","domestic policy", "public policy", "law",     "constitution",     "civil rights",     "civil liberties",     "social justice",     "equality",     "political ideology",     "political spectrum",     "lobbying",     "special interest groups",     "media",     "political commentary",     "political satire",     "corruption",     "transparency",     "accountability",     "political science",     "international relations",     "public opinion",     "propaganda",     "power",     "authority",     "leadership",     "governance",     "policy making",     "public administration",    "bureaucracy",    "campaign finance",    "censorship",    "checks and balances",    "citizenship",    "constituency",    "crisis management",    "debates",    "defamation",    "dictatorship",    "discrimination",    "divisiveness",    "economic policy",    "election security",    "emergency powers",    "fascism",    "freedom of speech",    "human rights",    "impeachment",    "judicial system",    "legislative branch",    "libertarianism",    "lobbyists",    "military",    "minorities",    "nationalism","patriotism","peacekeeping","political asylum","political correctness","political culture","political economy","political stability","populism","protest","public service","reform","representation","revolution","separation of powers","socialism","sovereignty","state","totalitarianism","veto","war","welfare state"]

# Abbreviated forms of Australian States/Territories
STATE_ABBREVS = {
    'New South Wales': '(nsw)',
    'Victoria': '(vic.)',
    'Queensland': '(qld)',
    'South Australia': '(sa)',
    'Western Australia': '(wa)',
    'Tasmania': '(tas.)',
    'Northern Territory': '(nt)',
    'Australian Capital Territory': '(act)',
}

# Australian State Capitals
STATE_CAPITALS = {
    'Sydney': '1gsyd',
    'Melbourne': '2gmel',
    'Brisbane': '3gbri',
    'Adelaide': '4gade',
    'Perth': '5gper',
    'Hobart': '6ghob',
    'Darwin': '7gdar',
    'Canberra': '8acte',
}

def parse_location(location):
    m = re.match('(?P<region>[a-z\s\-]+)(?:,\s)?(?P<state>.+)?', location, re.IGNORECASE)
    return m.groupdict() if m is not None else None

# Generate candidate keys for look up in sal
def generate_candidate_keys(region, state):
    state_abbrev = STATE_ABBREVS.get(state)
    candidate_keys = region.lower().split(' - ')

    # Keep original as a potential candidate
    candidate_keys.append(region)

    if state_abbrev is not None:
        for region in region.split(' - '):
            candidate_key = region.lower() + ' ' + state_abbrev
            candidate_keys.append(candidate_key)
    
    return candidate_keys

# Get candidates gccs
def get_candidate_gccs(keys):
    candidate_gccs = set()

    for key in keys:
        if sal.get(key) is not None:
            candidate_gccs.add(sal.get(key)['gcc'])

    return candidate_gccs

# Test if unique gcc resolved
def location_resolved(gccs):
    return len(gccs) == 1

# Test if location is a capital city
def is_capital(location):
    return location in STATE_CAPITALS
def process_location(region, state):

    # Check if capital in location information
    if is_capital(state):
        return STATE_CAPITALS.get(state)
    
    if is_capital(region):
        return STATE_CAPITALS.get(region)
    
    # Otherwise generate candidate keys and look up in sal
    keys = generate_candidate_keys(region, state)
    gccs = get_candidate_gccs(keys)

    # Return gcc if unique, otherwise None
    if location_resolved(gccs):
        return gccs.pop()
    else:
        return None

# policy_bow = ["election", "vote", "candidate", "campaign", "party", "government", "policy", "law", "justice", "democracy", "freedom", "rights", "constitution", "representative", "power", "sovereignty", "diplomacy", "foreign policy", "national security", "border", "immigration", "citizenship", "regime", "ideology", "political system", "political party", "political institution", "executive", "legislative", "judiciary", "impeachment", "constitutional amendment", "civil rights", "civil liberties", "civic duty", "activism", "protest", "social justice", "inequality", "discrimination", "human rights", "public opinion", "opinion poll", "media", "propaganda", "lobbying", "interest group", "corruption", "accountability", "transparency"]

# just for removing the prefix and suffix
def remove_prefix(bow):
  # Define patterns to match prefixes and suffixes
  prefix_pattern = re.compile(r'^(un|dis|non|anti|in|im|il|ir|over|out|pre|post|sub|super|re)+', re.IGNORECASE)
  suffix_pattern = re.compile(r'(ing|ed|s|es|ly|ment|able|ible|ive|tion|ion|ate|al|ish|ous|ic)+$', re.IGNORECASE)
  
  bow = [term.lower() for term in bow]
  processed_words= []
  for words in bow:
      # Remove any prefixes or suffixes
      words = re.sub(prefix_pattern, '', words)
      words = re.sub(suffix_pattern, '', words)
      # Split the term by spaces
      words_split = words.split(' ')
      # Add each part to the processed list
      for word in words_split:
          processed_words.append(word)
          
  # Remove any duplicates from the list
  processed_terms = list(set(processed_words))

  return processed_terms

def to_root_words(bow):
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
def check_include_topic(input_string,topic_bow):
    # remove the suffix and prefix
    # topic_bow_remove = remove_prefix(topic_bow)
    topic_bow_remove = to_root_words(topic_bow)
    input = re.findall(r'\w+', input_string)

    # convert to all lower case
    input = [word.lower() for word in input]
    input_remove = to_root_words(input)
    policy_words = [word for word in input_remove if word in topic_bow_remove]
    
    return policy_words
def main():
    with open(TWEET_FILE, encoding='utf-8') as file:
        parser = ijson.parse(file)
        with open('spolicy_tweets.json', 'w', encoding='utf-8') as outfile:
            for prefix, event, value in parser:
                try:
                    if prefix == 'rows.item' and event =='start_map':
                        tweets_dict = defaultdict()
                        policy_realted = False
                        if_en = False
                    elif prefix == 'rows.item.id' and event == 'string':
                        tweets_dict['tweet_id'] = value
                #elif prefix == 'rows.item.doc.data.text' and event == 'string':
                    #tweets_dict['tweet_text'] = value
                    elif prefix == 'rows.item.doc.includes.places.item.full_name' and event == 'string':
                        location = parse_location(value)
                        if (location is not None):
                            region = location.get('region') if location.get('region') is not None else None
                            state = location.get('state') if location.get('state') is not None else None
                            gcc = process_location(region, state)
                            tweets_dict['region'] = region
                            tweets_dict['state'] = state
                            tweets_dict['gcc'] = gcc
                            tweets_dict['location'] = value
                    elif prefix == 'rows.item.value.tokens' and event == 'string':
                        tweets_dict['token'] = value
                        if check_include_topic(value,policy_bow) != []:
                            tweets_dict['policy_realted'] = True
                        else:
                            tweets_dict['policy_realted'] = False
                    elif prefix == 'rows.item.doc.data.author_id' and event == 'string':
                        tweets_dict['author'] = value
                    elif prefix == 'rows.item.doc.data.created_at' and event == 'string':
                        tweets_dict['date_create'] = value
                    elif prefix == 'rows.item.doc.data.lang' and value == 'en':
                        if_en = True
                    elif prefix == 'rows.item.doc.data.public_metrics.retweet_count' and event == 'number':
                        tweets_dict['retweet_count'] = value
                    elif prefix == 'rows.item.doc.data.public_metrics.reply_count' and event == 'number':
                        tweets_dict['reply_count'] = value
                    elif prefix == 'rows.item.doc.data.public_metrics.like_count' and event == 'number':
                        tweets_dict['like_count'] = value
                    elif prefix == 'rows.item.doc.data.public_metrics.quote_count' and event == 'number':
                        tweets_dict['quote'] = value
                    elif prefix == 'rows.item.doc.data.context_annotations.item.domain.name' and event=='string':
                        if check_include_topic(value,policy_bow) != []:
                            tweets_dict['domain'] = value
                            policy_realted = True
                    elif prefix == 'rows.item.doc.data.context_annotations.item.entity.name' and event=='string':
                        if check_include_topic(value,policy_bow) != []:
                            policy_realted = True
                            tweets_dict['entity'] = value
                    if prefix == 'rows.item' and event =='end_map' and 'location' in tweets_dict and if_en:
                        if 'domain' not in tweets_dict:
                            tweets_dict['domain'] = 'NA'
                        if 'entity' not in tweets_dict:
                            tweets_dict['entity'] = 'NA'
                        if 'region' not in tweets_dict:
                            tweets_dict['region'] = 'NA'
                        if 'state' not in tweets_dict:
                            tweets_dict['state'] = 'NA'
                        if 'gcc' not in tweets_dict:
                            tweets_dict['gcc'] = 'NA'
                        if 'location' not in tweets_dict:
                            tweets_dict['location'] = 'NA'
                        json.dump(tweets_dict, outfile)
                        outfile.write(',')
                        outfile.write('\n')
                except:
                    continue
        return
if __name__ == '__main__':
    main()
    
