from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)

db = client.instagram

i, j = 0, 0

follow_user = 'machinelearning'
followers = []

for follower in db.instagram.find({'follower_name': follow_user},
                                  {'_id': 0,
                                   'follower_name': 1,
                                   'follow_name': 1,
                                   'follow_full_name': 1,
                                   'follow_pic_url': 1}):
    followers.append(follower)
    i += 1

print(f'У пользователя {follow_user} {i} подписок\n')
pprint(followers)

follower_user = 'datascience'
follows = []

for follow in db.instagram.find({'follow_name': follower_user},
                                {'_id': 0,
                                 'follow_name': 1,
                                 'follower_name': 1,
                                 'follower_full_name': 1,
                                 'follower_pic_url': 1}):
    follows.append(follow)
    j += 1

print(f'\nУ пользователя {follower_user} {j} подписчиков\n')
pprint(follows)
