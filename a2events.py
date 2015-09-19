__author__ = 'Joshua Walker'

from dateutil import tz
import json
import dateutil.parser
from datetime import *
import pytz
import facebook
import git
from git import Repo
import os


def main():

    #parser = ConfigParser.SafeConfigParser()
    #parser.read('config.ini')
    #secret = parser.get('facebook', 'secret')
    #app_id = parser.get('facebook', 'app_id')

    secret = os.environ['SECRET']
    app_id = os.environ['APP_ID']
    github_pass = os.environ['GITHUB_PASS']
    github_user = os.environ['GITHUB_USER']
    token = facebook.get_app_access_token(app_id, secret)
    event_list = facebook_fetch(token)

    event_list = sorted(event_list, key=lambda item: item['date'])

    to_github(event_list, github_user, github_pass)

def facebook_fetch(token):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('US/Eastern')
    try:
        graph = facebook.GraphAPI(access_token=token)
        with open('facebook.json') as data_file:
            data = json.load(data_file)
            event_list = []
            for each in data['venue']:
                try:
                    venue_events = graph.get_connections(id=each['id'], connection_name='events')
                    for event in venue_events['data']:
                        try:
                            event_object = graph.get_object(event['id'])
                            # if 'timezone' in event:
                            # converted_time = str(dateutil.parser.parse(event['start_time'], ignoretz=True))
                            # converted_time = event['start_time']
                            # print "w/timezone ", converted_time
                            # else:

                            if len(event['start_time']) < 11:
                                converted_time = event['start_time']
                            else:
                                print event['start_time']
                                converted_time = dateutil.parser.parse(event['start_time'])
                                converted_time = str(converted_time.astimezone(pytz.timezone('US/Eastern')))
                                converted_time = converted_time.replace(" ", "T")

                            if 'description' in event_object:
                                event_list.append(
                                    dict(name=event['name'], url='https://www.facebook.com/events/' + event['id'] + '/',
                                         date=converted_time, source='Facebook',
                                         description=event_object['description']))
                            else:
                                event_list.append(
                                    dict(name=event['name'], url='https://www.facebook.com/events/' + event['id'] + '/',
                                         date=converted_time, source='Facebook'))
                        except Exception as inst:
                            print type(inst)
                            print inst.args
                            print inst
                            pass
                except Exception as inst:
                    print type(inst)
                    print inst.args
                    print inst
                    pass
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        pass

    return event_list


def to_github(event_list, github_user, github_pass):
    #ghpages = Repo.clone_from('https://github.com/jshwlkr/a2events.git')
    os.system("git clone -v https://" + github_user + ":" + github_pass + "@github.com/jshwlkr/a2events.git")
    ghpages = Repo("a2events")
    ghpages.git.checkout('gh-pages')
    with open('a2events/data.json', 'w') as outfile:
        json.dump(event_list, outfile)

    ghpages.git.add('data.json')
    msg = "Event Update " + str(datetime.now())
    ghpages.index.commit(msg)
    #os.system("ls a2events")
    #os.system("git push ")

    ghpages.git.push()

if __name__ == "__main__":
    main()