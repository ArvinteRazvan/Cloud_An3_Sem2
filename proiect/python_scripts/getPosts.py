import json
import os

import re
import requests
from newsapi.articles import Articles
from newsapi.sources import Sources

API_KEY = "f044f5b63a7c4139858611a1ae6dc5f0"

s = Sources(API_KEY=API_KEY)
a = Articles(API_KEY=API_KEY)


# print(s.information().all_categories())

# print(s.get_by_category("general"))

def get_country_news(country):
    country_id = country + "&"
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=' + country_id +
           'apiKey=' + API_KEY)
    response = requests.get(url)
    response = response.json()

    path = os.path.join(os.getcwd(), "posts")
    path = os.path.join(path, "regional_news")
    path = os.path.join(path, country)

    for main_key in response.items():
        if main_key[0] == "articles":
            for posts in main_key[1]:
                posts = json.loads(json.dumps(posts))
                print(posts)

                filename = re.sub(r'[^\w]', ' ', posts['title'])
                filename = filename.replace(" ", "_") + ".json"
                print(filename)
                with open(os.path.join(path, filename), "w") as output:
                    json.dump(posts, output)


# 'sources=bbc-news&'

# 'country=us&'


# 'q=Apple&'
# 'from=2018-05-30&'
# 'sortBy=popularity&'

# url = ('https://newsapi.org/v2/top-headlines?'
#       'sources=' + source +
#       'apiKey=' + API_KEY)
# response = requests.get(url)
# response = response.json()





def get_post_by_category(category):
    res = s.get_by_category(category=category)
    for i in res.items():
        if i[0] == "sources":
            post_list = i[1]

    # for each post
    for post in post_list:
        # print(post)
        path = os.path.join(os.getcwd(), "posts")
        path = os.path.join(path, category)
        path = os.path.join(path, post["id"] + ".json")

        response = a.get_by_popular(post['id'])

        # print(content)
        # print(id)
        # print(post)
        print(response)
        with open(path, "w") as output:
            json.dump(response, output)
    print("_____________________")


# get_post_by_category("general")
# get_post_by_category("technology")
# get_post_by_category("sports")
# get_post_by_category("business")
# get_post_by_category("entertainment")
# get_post_by_category("science")
get_country_news("ro")
