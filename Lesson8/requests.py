from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)

db = client.instagram

i, j = 0, 0

follower_user = 'machinelearning'
follows = []

for follow in db.instagram.find({'follower_name': follower_user},
                                {'_id': 0,
                                 'follower_name': 1,
                                 'follow_name': 1,
                                 'follow_full_name': 1,
                                 'follow_pic_url': 1}):
    follows.append(follow)
    i += 1

print(f'У пользователя {follower_user} {i} подписок\n')
pprint(follows)

follow_user = 'datascience'
followers = []

for follower in db.instagram.find({'follow_name': follow_user},
                                  {'_id': 0,
                                   'follow_name': 1,
                                   'follower_name': 1,
                                   'follower_full_name': 1,
                                   'follower_pic_url': 1}):
    followers.append(follower)
    j += 1

print(f'\nУ пользователя {follow_user} {j} подписчиков\n')
pprint(followers)
