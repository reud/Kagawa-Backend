from enum import Enum

from network.connector import gets, put, post


class CommunicationState(Enum):
    NOT_STARTED = 1
    WAITING_FOR_IMPRESSION = 2


class ServerData(Enum):
    EMPTY = 1
    USER_ID_AND_LOCATION = 2
    FILLED = 3
    ERROR = -1


def check_server_data(user_id: str) -> ServerData:
    all_data = gets()
    records = all_data['records']
    for record in records:
        if record['user_id']['value'] == user_id:
            if record['location']['value'] != '':
                if record['comment']['value'] != '':
                    continue
                return ServerData.USER_ID_AND_LOCATION
            return ServerData.ERROR
    return ServerData.EMPTY


def update_value(user_id: str, record: dict):
    all_data = gets()
    records = all_data['records']

    for r in records:
        if r['user_id']['value'] == user_id:
            if r['location']['value'] == '':
                AttributeError('bad data found')
            if r['comment']['value'] == '':
                print('found update value')
                put(record, r['$id']['value'])
                return
    AttributeError('ここは呼ばれないはずだよ')


def create_value(record: dict):
    uid = record['user_id']['value']
    loc = record['location']['value']
    all_data = gets()
    records = all_data['records']
    for r in records:
        if r['user_id']['value'] == uid and r['location']['value'] == loc:
            AttributeError('既に存在しているフィールド')
    post(record)
