import urllib
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import digits
import csv

#string websites
websites = ""

#list of all word
all_words = []

# List of total words in each article
total_words = []

# track article and count of words in dictionary
track_article = {}

#for each website in website list
with open('website_list', 'r') as f:
    websites = f.readlines()

#for each website in website list
for url in websites:
    print url
    #count words
    word_count = 0
    #Disctionary mapping words to frequency
    word_list = {}
    #url = "http://www.cnn.com/2017/01/24/politics/donald-trump-chicago-carnage/index.html"
    #html = urllib.urlopen(url).read().decode('utf-8')
    html = urllib.urlopen(url).read().decode('unicode_escape').encode('ascii','ignore')
    #soup = BeautifulSoup(html, "lxml")
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    title = soup.title.string
    # kill all script and style elements
    for script in soup(["script", "style"]):
        #script.extract()   # rip it out
        script.replace_with(" ")
    # get text
    #print(soup.get_text())
    text = soup.get_text().lower()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.replace("'", " ").replace("\""," ").replace(".'"," ")
    text = ''.join([i for i in text if not i.isdigit()])
    punctuations = [">>",">","+","?", "'", ".", ",", '"', "%", "-", "&", "$", "|", ":", ";", ")", "(","{","}","!","-"]
    for symbol in punctuations:
        #print symbol
        text = text.replace(symbol, " ")
    #sentences = nltk.tokenize.sent_tokenize(text)
    stopWords = set(stopwords.words('english'))
    filter_word = text.split()
    final_word = [word for word in filter_word if word not in stopWords]                
    #filtered_words = [e.lower() for e in sentences if not e.lower() in stopWords]
    result = ' '.join(final_word)
    #print result

    for word in result.split():
        word_count += 1
        # Increase word frequency by 1
        if word in word_list:
            word_list[word] += 1
        else:
            word_list[word] = 1

    #add word to complete word list
        if word not in all_words:
            all_words.append(word)
    #add to word count list
    total_words.append(word_count)

    # Add title and word/frequency to dictionary
    track_article[title] = word_list

    #print (word_count)
    #print (word_list)

with open("data.csv", 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Write all of the words to the top row
    csv_words = [x.encode('UTF8') for x in all_words]
    #print(csv_words)
    space_with_all_words = ['SITE', 'WORD COUNT'] + csv_words
    writer.writerow(space_with_all_words)

    #for each word
    for url, word_count in zip(track_article, total_words):
        #List of every word on the site
        words = track_article[url]
        
        #List of the frequency of all of the words in the same order as all_words is in
        word_frequency = []
	
        #for every word
        for word in all_words:
            #If in site, append frequency, if not, append a 0
            if word in words:
                word_frequency.append(words[word])
            else:
                word_frequency.append(0)


        test = [url.encode('UTF8')] + [word_count] + word_frequency
	#write site title to csv
        #test_new = [y.encode('UTF8') for y in test]
        writer.writerow(test)


