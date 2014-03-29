import sys
from httplib2 import ServerNotFoundError
from workflow import Workflow, PasswordNotFound
from helpers import get_client


def main(wf):
    user_input = ''.join(wf.args)

    try:
        wf.get_password('readability_oauth_token')
        wf.get_password('readability_oauth_token_secret')
        item_list = wf.cached_data(
            'readability_list', data_func=get_list, max_age=1)
        if item_list is None and len(wf._items) == 0:
            wf.clear_cache()
            item_list = wf.cached_data(
                'readability_list', data_func=get_list, max_age=60)
        if item_list is not None:
            if len(item_list) == 0:
                wf.add_item('Your Readability list is empty!', valid=False)
            else:
                for item in item_list:
                    if all(x in item for x in ['article', 'date_added', 'id']):
                        title = item['article']['title']
                        subtitle = item['date_added'] + ': ' + item[
                            'article']['url']

                        if user_input.lower() in title.lower() or user_input.lower() in subtitle.lower():
                            wf.add_item(title, subtitle, arg=item[
                                        'article']['url'] + ' ' + str(item['id']), valid=True)

    except PasswordNotFound:
        wf.add_item(
            'Please press enter "username:password" to authorize the workflow',
            'Then try again...', arg=user_input, valid=':' in user_input)

    wf.send_feedback()


def get_list():
    rdb_client = get_client(wf)
    try:
        bookmarks_response = rdb_client.get_bookmarks(archive=False)
        data = bookmarks_response.content
        if 'error_message' in data:
            wf.delete_password('readability_oauth_token')
            wf.delete_password('readability_oauth_token_secret')
            wf.add_item('There was a problem receiving your Readability list.',
                        'The workflow has been deauthorized automatically. Please try again!', valid=False)
            return None
        return data['bookmarks']

    except ServerNotFoundError:
        wf.add_item('Could not contact readability.com',
                    'Please check your internet connection and try again!', valid=False)
    return None


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
