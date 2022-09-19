import json
import os

TOKEN_KEY = 'Token'
PREFIX_KEY = 'Prefix'


def fetch_bot_token():
    """
    Fetches bot's token either from a Config file if present / otherwise assumes environment variable has token set
    This is useful for Deploying to cloud services and test locally as well
    To test locally replace <PlaceHolder> in config.json with Token
    :return: Token (String)
    """
    with open("config.json") as config_file:
        config = json.load(config_file)
        token = config[TOKEN_KEY]
        if token == "<PlaceHolder>":
            # This means that it's deployed in production and needs to fetch token from Env variable
            print("Fetching bot token from enviroment variable:", TOKEN_KEY)
            token = os.environ[TOKEN_KEY]
            print(token, type(token))
        return token


def fetch_bot_command_prefix():
    """
    Fetches bot command prefix (to be used in Discord app)
    :return: String
    """
    with open("config.json") as config_file:
        config = json.load(config_file)
        return config[PREFIX_KEY]


def get_user(ctx, identifier):
    """
    Helper method that gets a User based on Context and an Identifier
    :param ctx: Context
    :param identifier: String
    :return: Optional[Member]
    """
    return ctx.guild.get_member(int(identifier))


def pretty_print_dictionary(input_dictionary):
    """
    Given an input Dictionary - provides a pretty-printed string
    :param input_dictionary: Dictionary
    :return: String
    """
    response = ""
    print(input_dictionary)
    for item in sorted(input_dictionary):
        response += str(item) + " : " + str(input_dictionary[item]) + "\n"
    return response
