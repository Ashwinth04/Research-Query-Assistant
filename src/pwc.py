import urllib.parse
from tqdm import tqdm
import requests

def extract_papers(query):
    query = urllib.parse.quote(query)
    # print(query)
    url = f"https://paperswithcode.com/api/v1/papers/?q={query}"
    response = requests.get(url)
    response = response.json()
    count = response['count']
    results = []
    results += response['results']

    num_pages = count // 50
    if(num_pages > 20):
        num_pages = 20
    for page in tqdm(range(2,num_pages)):
        urln = f"https://paperswithcode.com/api/v1/papers/?q={query}&page={page}"
        response = requests.get(urln)
        response = response.json()
        # print(response)
        results += response['results']
    return results

# print(extract_papers("Convolutional Neural Network"))