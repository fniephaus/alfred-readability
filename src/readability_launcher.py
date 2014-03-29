import sys
import os
from readability import xauth
from httplib2 import ServerNotFoundError
from workflow import Workflow, PasswordNotFound
import argparse
from helpers import get_client


def execute(wf):
    try:
        wf.get_password('readability_oauth_token')
        wf.get_password('readability_oauth_token_secret')
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--copy', dest='copy', action='store_true', default=None)
        parser.add_argument(
            '--visit-and-archive', dest='visit_archive', action='store_true', default=None)
        parser.add_argument(
            '--archive', dest='archive', action='store_true', default=None)
        parser.add_argument(
            '--delete', dest='delete', action='store_true', default=None)
        parser.add_argument(
            '--deauthorize', dest='deauthorize', action='store_true', default=None)
        parser.add_argument('query', nargs='?', default=None)
        args = parser.parse_args(wf.args)

        query = args.query.split()
        if len(query) > 0:
            url = query[0]
        if len(query) > 1:
            item_id = query[1]

        if args.copy:
            print set_clipboard(url)
            return 0
        elif args.visit_archive:
            open_url(url)
            wf.clear_cache()
            print archive_item(item_id)
            return 0
        elif args.archive:
            wf.clear_cache()
            print archive_item(item_id)
            return 0
        elif args.delete:
            wf.clear_cache()
            print delete_item(item_id)
            return 0
        elif args.deauthorize:
            wf.delete_password('readability_oauth_token')
            wf.delete_password('readability_oauth_token_secret')
            print "Workflow deauthorized."
            return 0
        else:
            open_url(url)
            return 0
    except PasswordNotFound:
        user_details = ''.join(wf.args).split(':')
        if len(user_details) == 2:
            print authorize(user_details[0], user_details[1])
            return 0


def open_url(url):
    os.system('open %s' % url)


def set_clipboard(url):
    clipboard = os.popen(
        """ osascript -e 'set the clipboard to "%s"' """ % url).readline()
    return 'Link copied to clipboard'


def archive_item(item_id):
    rdb_client = get_client(wf)
    try:
        rdb_client.archive_bookmark(item_id)
        return 'Link archived'
    except ServerNotFoundError:
        return 'Connection error'


def delete_item(item_id):
    rdb_client = get_client(wf)
    try:
        rdb_client.delete_bookmark(item_id)
        return 'Link deleted'
    except ServerNotFoundError:
        return 'Connection error'


def authorize(username, password):
    import config
    try:
        user_credentials = xauth(
            config.CONSUMER_KEY, config.CONSUMER_SECRET, username, password)
        if len(user_credentials) == 2:
            wf.save_password(
                'readability_oauth_token', user_credentials[0])
            wf.save_password(
                'readability_oauth_token_secret', user_credentials[1])
            return 'Workflow authorized.'
    except:
        pass

    return 'Authorization failed.'


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(execute))
