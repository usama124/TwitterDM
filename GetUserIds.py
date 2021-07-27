import twitter, time
import configparser

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


def read_usernames():
    usernames = []
    f = open("Data/usernames.txt", "r", encoding="utf-8")
    line = f.readline()
    while line != "" and line != None:
        usernames.append(line.replace("\n", ""))
        line = f.readline()
    f.close()
    return usernames


def write_userids(username_ids):
    f = open("Data/userids.txt", "w")
    for key in username_ids:
        f.write(key + "||" + username_ids[key]+"\n")
    f.close()


if __name__ == "__main__":
    general_conf = confParser("general_conf")
    API_KEY = general_conf["api_key"].decode("utf-8")
    API_KEY_SECRETE = general_conf["api_key_secrete"].decode("utf-8")
    ACCESS_TOKEN = general_conf["access_token"].decode("utf-8")
    ACCESS_TOKEN_SECRETE = general_conf["access_token_secrete"].decode("utf-8")

    api = twitter.Api(consumer_key= API_KEY, consumer_secret = API_KEY_SECRETE, access_token_key = ACCESS_TOKEN, access_token_secret = ACCESS_TOKEN_SECRETE)
    usernames = read_usernames()
    username_ids = {}
    for username in usernames:
        try:
            user_id = api.UsersLookup(screen_name="DanishJanjua_")[0].id_str
            username_ids[username] = user_id
        except Exception as e:
            pass
        time.sleep(2)
    write_userids(username_ids)
