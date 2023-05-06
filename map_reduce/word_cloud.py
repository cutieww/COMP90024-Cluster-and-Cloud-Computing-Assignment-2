import re
import json
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

count = 0
frequency = {}
stop_words = set(stopwords.words('english'))
def get_word_frequency(token):
    words = token.lower().split("|")
    stop_words.add('the')
    stop_words.add('like')
    words = [word for word in words if not word in stop_words]
    
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency

def plot_word_cloud(frequency):
    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate_from_frequencies(frequency)
    plt.figure(figsize=(8,8))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

def main():
    with open('ccc/tweets.json', 'r') as file:
        # Read the first line
        line = file.readline()
        # Loop through the file until we reach the end
        while line:
            line = re.search(r'\{.*?\}', line).group()

            json_data = json.loads(line)
            if (json_data['policy_realted']==True):
                token = json_data['token']
                frequency = get_word_frequency(token)
                count += 1
            if (count > 10000):
            
                break
        line = file.readline()
    plot_word_cloud(frequency)

if __name__ == '__main__':
    main()