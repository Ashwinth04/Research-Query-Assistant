import urllib.parse
from tqdm import tqdm
import requests
from keywords import all_possible_keywords

def extract_papers(query):
    keyword_list = all_possible_keywords(query)
    print(f"\n\n{keyword_list}\n\n")
    results = []
    for keyword in keyword_list:
        keyword = urllib.parse.quote(keyword)
        url = f"https://paperswithcode.com/api/v1/papers/?q={keyword}"
        response = requests.get(url)
        response = response.json()
        count = response['count']
        # print(f"\n\nCOUNT({keyword}) : {count}\n\n")
        results += response['results']

        num_pages = count // 50
        if(num_pages > 20):
            num_pages = 20
        for page in tqdm(range(2,num_pages)):
            urln = f"https://paperswithcode.com/api/v1/papers/?q={keyword}&page={page}"
            response = requests.get(urln)
            response = response.json()
            # print(response)
            results += response['results']
    return results

# print(extract_papers("cnn"))