import json
import re
from copy import deepcopy
from urllib.parse import urlencode

import scrapy
from scrapy.http import HtmlResponse

from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    insta_login = 'vitaly_mmxx'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER...'

    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    users = ['datascience', 'machinelearning']

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    hash_followers = 'c76146de99bb02f6415203be841dd25a'
    hash_follows = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'user': user}
                )

    def user_data_parse(self, response: HtmlResponse, user):

        user_info = response.xpath("//script[contains(text(), 'csrf_token')]/text()") \
            .extract_first().replace("window._sharedData = ", '').replace(";", '')

        user_info_get = json.loads(user_info).get('entry_data', {}) \
            .get('ProfilePage', {})[0] \
            .get('graphql', {}) \
            .get('user', {})

        info = {
            'user': user,
            'user_id': user_info_get.get('id'),
            'pic_url': user_info_get.get('profile_pic_url'),
            'full_name': user_info_get.get('full_name')
        }

        variables = {"id": info['user_id'],
                     "first": 12}

        url_followers = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'

        yield response.follow(
            url_followers,
            callback=self.followers_parse,
            cb_kwargs={'info': info,
                       'variables': deepcopy(variables)}
        )

        url_follows = f'{self.graphql_url}query_hash={self.hash_follows}&{urlencode(variables)}'

        yield response.follow(
            url_follows,
            callback=self.follows_parse,
            cb_kwargs={'info': info,
                       'variables': deepcopy(variables)}
        )

    def followers_parse(self, response, info, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data', {}).get('user', {}).get('edge_followed_by', {}).get('page_info', {})
        followers = j_data.get('data', {}).get('user', {}).get('edge_followed_by', {}).get('edges', {})

        for follower in followers:
            item = InstaparserItem(
                _id=f"{info['user_id']}_{follower['node']['id']}",
                follow_id=info['user_id'],
                follow_name=info['user'],
                follow_full_name=info['full_name'],
                follow_pic_url=info['pic_url'],
                follower_id=follower['node']['id'],
                follower_name=follower['node']['username'],
                follower_full_name=follower['node']['full_name'],
                follower_pic_url=follower['node']['profile_pic_url']
            )

            yield item

        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']

            url_posts = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'

            yield response.follow(
                url_posts,
                callback=self.followers_parse,
                cb_kwargs={'info': info,
                           'variables': deepcopy(variables)}
            )

    def follows_parse(self, response, info, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data', {}).get('user', {}).get('edge_follow', {}).get('page_info', {})
        follows = j_data.get('data', {}).get('user', {}).get('edge_follow', {}).get('edges', {})

        for follow in follows:
            item = InstaparserItem(
                _id=f"{follow['node']['id']}_{info['user_id']}",
                follower_id=info['user_id'],
                follower_name=info['user'],
                follower_full_name=info['full_name'],
                follower_pic_url=info['pic_url'],
                follow_id=follow['node']['id'],
                follow_name=follow['node']['username'],
                follow_full_name=follow['node']['full_name'],
                follow_pic_url=follow['node']['profile_pic_url']
            )
            yield item

        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']

            url_posts = f'{self.graphql_url}query_hash={self.hash_follows}&{urlencode(variables)}'

            yield response.follow(
                url_posts,
                callback=self.follows_parse,
                cb_kwargs={'info': info,
                           'variables': deepcopy(variables)}
            )

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')
