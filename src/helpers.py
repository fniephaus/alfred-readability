from readability import ReaderClient
import config


def get_client(wf):
    oauth_token = wf.get_password('readability_oauth_token')
    oauth_token_secret = wf.get_password('readability_oauth_token_secret')
    return ReaderClient(
        config.CONSUMER_KEY, config.CONSUMER_SECRET, oauth_token, oauth_token_secret)
