import sys
import os
import urlparse
from httplib2 import ServerNotFoundError
from workflow import Workflow
from helpers import get_client


def main(wf):
    current_app = os.popen(
        """ osascript -e 'application (path to frontmost application as text)' """).readline().rstrip()
    if current_app in ['Google Chrome', 'Safari']:
        if not add_bookmark(get_browser_url(current_app)):
            print "%s link invalid." % current_app
            return 0
        print "%s link added to Pocket." % current_app
        wf.clear_cache()
        return 0
    else:
        url = get_clipboard_bookmark()
        if url is not None:
            add_bookmark(url)
            print "Clipboard link added to Pocket."
            wf.clear_cache()
            return 0

    print "No link found!"
    return 0


def frontmost_app():
    return os.popen(""" osascript -e 'application (path to frontmost application as text)' """).readline().rstrip()


def get_browser_url(browser):
    url = None
    if browser == 'Google Chrome':
        url = os.popen(
            """ osascript -e 'tell application "Google Chrome" to return URL of active tab of front window' """).readline()
    elif browser == 'Safari':
        url = os.popen(
            """ osascript -e 'tell application "Safari" to return URL of front document' """).readline()
    return url


def get_clipboard_bookmark():
    clipboard = os.popen(""" osascript -e "get the clipboard" """).readline()
    parts = urlparse.urlsplit(clipboard)
    if not parts.scheme or not parts.netloc:
        return None
    return clipboard


def add_bookmark(url):
    if url is not None:
        rdb_client = get_client(wf)
        try:
            rdb_client.add_bookmark(url=url)
            return True
        except ServerNotFoundError:
            pass
    return False


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
