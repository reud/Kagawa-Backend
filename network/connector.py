import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

JSON_HEADER = {'X-Cybozu-API-Token': os.getenv('CYBOZU_API_TOKEN'), 'Content-Type': 'application/json'}


def inject_body(body: dict):
    return {'app': 1,
            'record': body}


def gets() -> dict:
    header = {'X-Cybozu-API-Token': os.getenv('CYBOZU_API_TOKEN')}
    URL = 'https://devlbbyuk.cybozu.com/k/v1/records.json?app=1'
    print(f'token: {os.getenv("CYBOZU_API_TOKEN")}')
    r = requests.get(URL, headers=header)
    print(f'GETS: {r.text}')
    return json.loads(r.text)


def test_posts():
    mock_uid = 'mock_uid'
    mock_location = '東京ディズニーランド'
    mock_comment = '夢の国！！！たのC！'

    # only user_id test
    ud = {'user_id': {'value': mock_uid}}
    u = inject_body(ud)
    test_post(u)

    # only location test
    ld = {'location': {'value': mock_location}}
    l = inject_body(ld)
    test_post(l)

    # only comment test
    cd = {'comment': {'value': mock_comment}}
    c = inject_body({'comment': {'value': mock_comment}})

    test_post(c)


def test_post(payload: dict):
    URL = 'https://devlbbyuk.cybozu.com/k/v1/record.json'
    r = requests.post(URL, headers=JSON_HEADER, data=json.dumps(payload))
    print('\n-------RESULT-------')
    print(r.text)
    print('\n')


def post(payload: dict):
    payload = inject_body(payload)
    URL = 'https://devlbbyuk.cybozu.com/k/v1/record.json'
    r = requests.post(URL, headers=JSON_HEADER, data=json.dumps(payload))
    print(f'POST: {r.text}')


def put(records: dict, id: str):
    payload = {'app': 1, 'id': id, 'record': records}
    URL = 'https://devlbbyuk.cybozu.com/k/v1/record.json'
    print(f'PUTTING: {json.dumps(payload)}')
    r = requests.put(URL, headers=JSON_HEADER, data=json.dumps(payload))
    print(f'PUT: {r.text}')


if __name__ == '__main__':
    gets()
