# ijson_processing.py
import ijson
import requests

filename = 'twitter-huge.json'
count_melbourne = 0
count_sydney = 0
data = {'Melbourne': 0, 'Sydney': 0}
# Open the file and create an ijson parser object
with open(filename, 'r') as file:
    # Use the items method to get an iterator for each element in the 'rows' array
    rows = ijson.items(file, 'rows.item')

    # Iterate over each row in the 'rows' array
    for row in rows:
        # Process each row (dictionary) as needed
        #print(row['id'])
        #print(row['key'])
        #print(row['value'])

        # Check if 'includes' attribute exists in the 'doc' dictionary
        if 'includes' in row['doc']:
            places = row['doc']['includes']['places']

            # Iterate over the places list to find Melbourne
            for place in places:
                if place['full_name'] == 'Melbourne, Victoria':
                    count_melbourne += 1
                    print(count_melbourne)
                    data['Melbourne']=count_melbourne
                    requests.post('http://localhost:8000/update', json=data)
                    break  # Exit the inner loop if Melbourne is found
                elif place['full_name'] == 'Sydney, New South Wales':
                    count_sydney +=1
                    print(count_sydney)
                    data['Sydney']=count_sydney
                    requests.post('http://localhost:8000/update', json=data)
                    break

