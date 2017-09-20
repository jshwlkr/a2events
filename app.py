import datetime
import json
import os
import urllib.parse
from datetime import datetime as dt
from git import Repo
import dateutil
import facebook
import pytz as pytz
from dateutil import parser


def main():
    # facebook credentials
    fb_secret = os.environ['SECRET']
    fb_app_id = os.environ['APP_ID']
    # github credentials
    gh_token = os.environ['GITHUB_TOKEN']

    master_list = fetch_fb(fb_secret, fb_app_id)
    master_list = clean_list(master_list)
    to_github(master_list, gh_token)


# grab facebook events
def fetch_fb(secret, app_id):
    current_time = dt.now(pytz.utc)
    fb_list = []
    token = get_app_access_token(app_id, secret)
    graph = facebook.GraphAPI(access_token=token, version='2.3')
    with open('facebook.json') as data_file:
        data = json.load(data_file)

    for each in data['venue']:
        try:
            venue_events = graph.get_connections(id=each['id'], connection_name='events')
        except:
            pass
        for event in venue_events['data']:
            event_object = graph.get_object(event['id'])
            print(event_object)
            start_time = dateutil.parser.parse(event_object['start_time'])
            if 'end_time' in event and current_time < start_time:
                end_time = dateutil.parser.parse(event_object['end_time'])
                if 'timezone' in event:
                    count = end_time - start_time
                    if count.days == 0 or count.seconds > 0:
                        count += datetime.timedelta(days=1)
                    count = int(count.days)
                    for ii in range(0, count):
                        append_event(event_object, fb_list, ii)


                else:
                    append_event(event_object, fb_list)
                    #if there's an end time but no timezone?
                    #is happening
            elif current_time < start_time:
                if 'timezone' in event:
                    append_event(event_object, fb_list)
                else:
                    append_event(event_object, fb_list)
                    #no timezone
                    #is happening, need to add

    return fb_list

def append_event(event_object, fb_list, offset=0):
    start_time = dateutil.parser.parse(event_object['start_time']) + datetime.timedelta(days=offset)
    start_time = str(start_time).replace(" ", "T")
    if 'description' in event_object:
        fb_list.append(
            dict(name=event_object['name'],
                 url='https://www.facebook.com/events/' + event_object['id'] + '/',
                 date=start_time, source='Facebook',
                 description=event_object['description']))
    else:
        fb_list.append(
            dict(name=event_object['name'],
                 url='https://www.facebook.com/events/' + event_object['id'] + '/',
                 date=start_time, source='Facebook'))

def clean_list(dirty_list):
    # sort list by date
    dirty_list = sorted(dirty_list, key=lambda item: item['date'])

    # remove duplicates
    seen = set()
    cleaned_list = []

    for d in dirty_list:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            cleaned_list.append(d)

    return cleaned_list


def to_github(master_list, token):
    ghpages = Repo.clone_from('https://jshwlkr:' + token + '@github.com/jshwlkr/a2events.git', 'a2events')
    ghpages.git.checkout('gh-pages')
    with open('a2events/event-segment-1.json', 'w') as outfile:
        json.dump(master_list[:10], outfile)
    with open('a2events/event-segment-2.json', 'w') as outfile:
        json.dump(master_list[10:], outfile)
    ghpages.git.add('event-segment-1.json')
    ghpages.git.add('event-segment-2.json')

    msg = "Event Update " + str(dt.now())
    ghpages.index.commit(msg)
    return


def get_app_access_token(app_id, app_secret):
    """Get the access_token for the app.

    This token can be used for insights and creating test users.

    app_id = retrieved from the developer page
    app_secret = retrieved from the developer page

    Returns the application access_token.

    """
    # Get an app access token
    args = {'grant_type': 'client_credentials',
            'client_id': app_id,
            'client_secret': app_secret}

    file = urllib.request.urlopen("https://graph.facebook.com/oauth/access_token?" +
                   urllib.parse.urlencode(args))

    result = file.read()
    result = json.loads(result)
    file.close()
    return result['access_token']


if __name__ == "__main__":
    main()

__author__ = 'Joshua Walker'
