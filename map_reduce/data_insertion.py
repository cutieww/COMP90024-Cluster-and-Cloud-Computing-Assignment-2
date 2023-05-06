import couchdb
import ijson
import json
import re
# Set up the connection string with username and password
username = 'admin'
password = 'admin'
server_url = f'http://{username}:{password}@172.26.132.19:5984/'
    #http://172.26.132.54:5984/_utils 

# Connect to the server
server = couchdb.Server(server_url)

def main():
    # Create the 'test_data' database if it does not exist
    if 'twitter' not in server:
        server.create('twitter')

    # Select the 'test_data' database
    db = server['twitter']

    # Insert the sample documents into the 'test_data' database
    with open('ccc/tweets.json', 'r') as file:
        # Read the first line
        line = file.readline()
        # Loop through the file until we reach the end
        while line:
            line = re.search(r'\{.*?\}', line).group()
            try:
                json_data = json.loads(line)
            # Insert the documents into the test_data database
                db.save(json_data)
            except:
                continue
            line = file.readline()
    return
if __name__ == '__main__':
    main()
