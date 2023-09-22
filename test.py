#%% Build a web crawler
import requests
import re 
import urllib.request 
from bs4 import BeautifulSoup 
from collections import deque
from html.parser import HTMLParser   
import os 
import openai 
import pandas as pd 

# Regex pattern to match a URL 
HTTP_URL_PATTERN = r'^http[s]*://.+' 

domain = "openai.com" 
full_url = "https://openai.com/" 

#%%
# create a class to parse the html and get the hyperlinks 
class HyperlinkParser(HTMLParser): 
    def __init__(self): 
        super().__init__()
        # create a list to store the hyperlinks 
        self.hyperlinks = [] 
    
    # Override the HTMLParser's handle_starttag method to get the hyperlinks 
    def handle_starttag(self, tag, attrs): 
        attrs = dict(attrs) 

        # If the tag is an anchor tag and if has an href attribute, add the href attribute to the list of hyperlinks 
        if tag == "a" and "href" in attrs: 
            self.hyperlinks.append(attrs["href"])

    # Function to get the hyperlinks from a URL 
def get_hyperlinks(url):
    # try to open the URL and read the HTML 
    try: 
        # open the URL and read the HTML 
        with urllib.request.urlopen(url) as response: 
            # if the response is not HTML, return an empty list 
            if not response.info().get('Content-Type').startswith('text/html'): 
                return []
            
            # decode the html 
            html = response.read().decode('utf-8') 
    except Exception as e: 
        print(e) 
        return []   

    # create the html parser and then parse the html to get hyperlinks 
    parser = HyperlinkParser()
    parser.feed(html) 

    return parser.hyperlinks

def get_domain_hyperlinks(local_domain, url): 
    clean_links = []
    for link in set(get_hyperlinks(url)): 
        clean_link = None

        # if the link is a URL, check if it is within the same domain 
        if re.search(HTTP_URL_PATTERN, link): 
            # parse the URL and check if the domain is the same
            url_obj = urlparse(link) 
            if url_obj.netloc == local_domain: 
                clean_link = link
        
        # if the link is not a URL, check if it is a relative link and then create a full URL 
        else: 
            if link.startswith('/'): 
                link = link[1:]
            elif link.startswith("#") or link.startswith("mailto:"): 
                continue
            clean_link = "https://" + local_domain + "/" + link 

        if clean_link is not None: 
            if clean_link.endswith("/"): 
                clean_link = clean_link[:-1]
            clean_links.append(clean_link)
    
    # return the list of hyperlinks that are within the same domain 
    return list(set(clean_links))

# avoid repeating the same page, extract the raw text and writes into a local .txt file 
def crawl(url): 
    # Parse the URL and get the domain 
    local_domain = urlparse(url).netloc 

    # Create a queue to store the URLs to be crawled 
    queue = deque([url]) 

    # Create a set to store the URLs that have already been crawled （no repetition）
    seen = set([url]) 

    # Create a directory to store the raw text of the crawled pages 
    if not os.path.exists("text/"): 
        os.mkdir("text/")

    if not os.path.exists("text/" + local_domain + "/"): 
        os.mkdir("text/" + local_domain + "/") 
    
    # create a directory to store the csv files 
    if not os.path.exists("processed"): 
        os.mkdir("processed")

    # while the queue is not empty, continue craling 
    while queue: 

        # get the next url from the queue 
        url = queue.pop() 
        print("Crawling URL: ", url) # print the URL being crawled, for debugging purposes
        
        # save text from the url to a <url>.txt file 
        try:
            with open('text/' + local_domain + '/' + url[8:].replace("/", "_") + ".txt", "w", encoding="utf-8") as f:
                # get the text from the URL using BeautifulSoup
                soup = BeautifulSoup(requests.get(url).text, 'html.parser') 

                # get the text but remove the tags 
                text = soup.get_text() 

                # if the crawler gets to a page that requires javascript, it will stop the craw 
                if ("You need to enable JavaScript to run this app." in text): 
                    print("Page requires javascript, skipping..." + url) 

                # otherwise, write the text to a file 
                f.write(text)

        except Exception as e: 
            continue
        
        # get the hyperlinks from the URL and add them to the queue 
        for link in get_domain_hyperlinks(local_domain, url): 
            if link not in seen:  
                queue.append(link)
                seen.add(link)

crawl(full_url) 
print("Crawling complete!")

#%% Building an embedding index (csv is a cmmon format for storing embeddings) 

# tidy up the text 
def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie 

''' convert text to csv: After opening each file, remove the extra spacing and append 
the modified text to a list. Then, add the text with the new lines removed to an empty 
Pandas data frame and write the data frame to a CSV file.
'''


# create a list to store the text 
texts = [] 

# Get all the text files in the text directory
for file in os.listdir("text/" + domain + "/"):

    # open the file and read the text 
    with open("text/" + domain + "/" + file, "r", encoding="utf-8") as f:
        text = f.read() 

        # omit the first 11 lines and last 4 lines, then replace -,_, and #update with spaces 
        texts.append((file[11:-4].replace('-',' ').replace('_', ' ').replace('#update',''), text))

# create a dataframe from the list of texts 
df = pd.DataFrame(texts, columns=["fname", "text"])

# set the text column to the raw text with the newlines removed
df["text"] = df.fname + ". " + remove_newlines(df.text) 
df.to_csv("processed/scraped.csv")
df.head() 

import tiktoken
import matplotlib as plt

# Load the cl100k_based tokenizer which is designed to work the ada-002 model 
tokenizer = tiktoken.get_encoding("cl100k_base") 

df = pd.read_csv("processed/scraped.csv", index_col=0) 
df.columns = ["title", "text"]

# tokenize the text and save the number of tokens 
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

# visualize the distribution of number of tokens per row 
df.n_tokens.hist()

#%% split the text into chunks 
max_tokens = 500 

# Function to split the text into chunks 
def split_into_many(text, max_tokens = max_tokens): 
    
    # split text into sentences 
    sentences = text.split(". ") 

    # get the number of tokens for each sentence 
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = [] 
    tokens_so_far = 0 
    chunk = [] 

    # loop through tht senteces and tokens joined together in a tuple 
    for sentence, token in zip(sentences, n_tokens): 

        # If the number of tokens so far plus the number of tokens in the current sentence is greater
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far

        if tokens_so_far + token > max_tokens: 
            chunks.append(". ".join(chunk) + ".") 
            chunk = [] 
            tokens_so_far = 0 
        
        # If the number of tokens in the current sentence is greater than the max number of
        # tokens, go to the next sentence
        if token > max_tokens:
            continue
        
        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks 

shortened = [] 

# loop through the rows of the dataframe 
for row in df.iterrows(): 

    # if the text is None, go to next row 
    if row[1]['text'] is None: 
        continue 

    # if the number of tokens is greater than the max number of tokens, split the text into chunks 
    if row[1]['n_tokens'] > max_tokens:
        shortened += split_into_many(row[1]['text']) 

    # otherwise, add text to list of shorteded texts 
    else: 
        shortened.append(row[1]['text']) 

# visualize the updated histogram 
df = pd.DataFrame(shortened, columns=["text"]) 
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x))) 
df.n_tokens.hist() 

# send request to OpenAI API 
df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding']) 

df.to_csv('processed/embeddings.csv')
df.head()






'''
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "user", 
         "content": "Hello world"
}])

content = chat_completion.choices[0]['message']['content']
print(content)
'''
# %%
