import json
import requests

user = 'vitalyvj'
link = f'https://api.github.com/users/{user}/repos'
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 OPR/69.0.3686.77',
    'Accept': 'application/vnd.github.v3+json'
}
params = {
    'sort': 'created',
    'direction': 'asc'
}

request = requests.get(link, headers=headers, params=params)
data = json.loads(request.text)
repos = []

print(f'Список репозиториев пользователя {user}:')
for i in range(len(data)):
    rep = data[i]['name']
    repos.append(rep)
    print(i + 1, rep, sep=') ')

with open('repositories.json', 'w') as j:
    json.dump({user: repos}, j)
