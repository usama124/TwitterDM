import configparser
from TwitterAPI import TwitterAPI
import json, time

parser = configparser.ConfigParser()
parser.read("Conf/config.ini")


def confParser(section):
    if not parser.has_section(section):
        print("No section info  rmation are available in config file for", section)
        return
    # Build dict
    tmp_dict = {}
    for option, value in parser.items(section):
        option = str(option)
        value = value.encode("utf-8")
        tmp_dict[option] = value
    return tmp_dict


def read_message():
    f = open("message.txt", "r", encoding="utf-8")
    text = f.read()
    f.close()
    return text


def read_usernames_ids():
    usernames = {}
    f = open("Data/userids.txt", "r", encoding="utf-8")
    line = f.readline().replace("\n", "")
    while line != "" and line != None:
        data = line.split("||")
        usernames[data[0]] = data[-1]
        line = f.readline().replace("\n", "")
    f.close()
    return usernames


def sendDM(user_id, message_text):
    event = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": user_id
                },
                "message_data": {
                    "text": message_text
                }
            }
        }
    }

    r = api.request('direct_messages/events/new', json.dumps(event))
    return r


if __name__ == "__main__":
    general_conf = confParser("general_conf")
    API_KEY = general_conf["api_key"].decode("utf-8")
    API_KEY_SECRETE = general_conf["api_key_secrete"].decode("utf-8")
    ACCESS_TOKEN = general_conf["access_token"].decode("utf-8")
    ACCESS_TOKEN_SECRETE = general_conf["access_token_secrete"].decode("utf-8")

    api = TwitterAPI(API_KEY, API_KEY_SECRETE, ACCESS_TOKEN, ACCESS_TOKEN_SECRETE)
    username_ids = read_usernames_ids()
    message_text = read_message()

    for username in username_ids:
        response = sendDM(username_ids[username], message_text)
        print(username + ' => SUCCESS' if response.status_code == 200 else username + ' => PROBLEM: ' + response.text)
        time.sleep(100)
