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

    #facebook credentials
    secret = os.environ['SECRET']
    app_id = os.environ['APP_ID']

    #github credentials
    github_pass = os.environ['GITHUB_PASS']
    github_user = os.environ['GITHUB_USER']

    token = facebook.get_app_access_token(app_id, secret)
    event_list = facebook_fetch(token)

    event_list = sorted(event_list, key=lambda item: item['date'])

    seen = set()
    new_l = []
    for d in event_list:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)

    event_list = new_l

    to_github(event_list, github_user, github_pass)

def facebook_fetch(token):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('US/Eastern')
    current_time = datetime.now(pytz.utc)
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

                            start_time = normalize_event(event['start_time'])
                            if 'end_time' in event:
                                end_time = normalize_event(event['end_time'])
                                day_count = end_time['comparison'] - start_time['comparison']
                                if day_count.days == 0:
                                    day_count = 1
                                else:
                                    day_count = day_count.days + 1
                                for ii in range(0, day_count):
                                    start_time = normalize_event(str(start_time['comparison'] + timedelta(days=ii)))
                                    if current_time < start_time['comparison'] :
                                        if 'description' in event_object:
                                            event_list.append(
                                                dict(name=event['name'], url='https://www.facebook.com/events/' + event['id'] + '/',
                                                     date=start_time['converted'], source='Facebook',
                                                     description=event_object['description']))
                                        else:
                                            event_list.append(
                                                dict(name=event['name'], url='https://www.facebook.com/events/' + event['id'] + '/',
                                                     date=start_time['converted'], source='Facebook'))

                                # while end_time['comparison'] >= start_time['comparison']:
                                #     print end_time['comparison'], start_time['comparison']
                                #     print event_object
                                #     if current_time < start_time['comparison'] :
                                #         if 'description' in event_object:
                                #             event_list.append(
                                #                 dict(name=event['name'], url='https://www.facebook.com/events/' + event['id'] + '/',
                                #                      date=start_time['converted'], source='Facebook',
                                #                      description=event_object['description']))
                                #         else:
                                #             event_list.append(
                                #                 dict(name=event['name'], url='https://www.facebook.com/events/' + event['id'] + '/',
                                #                         date=start_time['converted'], source='Facebook'))
                                #     start_time['comparison'] = start_time['comparison'] + timedelta(days=1)
                            else:
                                #if event has not past
                                if current_time < start_time['comparison'] :
                                    if 'description' in event_object:
                                        event_list.append(
                                            dict(name=event['name'], url='https://www.facebook.com/events/' + event['id'] + '/',
                                                 date=start_time['converted'], source='Facebook',
                                                 description=event_object['description']))
                                    else:
                                        event_list.append(
                                            dict(name=event['name'], url='https://www.facebook.com/events/' + event['id'] + '/',
                                                    date=start_time['converted'], source='Facebook'))
                        except Exception as inst:
                            print type(inst)
                            print inst.args
                            print inst
                            print each
                            pass
                except Exception as inst:
                    print type(inst)
                    print inst.args
                    print inst
                    print each
                    pass
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        pass

    return event_list


def to_github(event_list, github_user, github_pass):
    ##ghpages = Repo.clone_from('https://github.com/jshwlkr/a2events.git')
    os.system("git clone -v https://" + github_user + ":" + github_pass + "@github.com/jshwlkr/a2events.git")
    ghpages = Repo("a2events")
    ghpages.git.checkout('gh-pages')
    with open('a2events/event-segment-1.json', 'w') as outfile:
        json.dump(event_list[:10], outfile)
    del event_list[10]
    with open('a2events/event-segment-2.json', 'w') as outfile:
        json.dump(event_list[10:], outfile)
    ghpages.git.add('event-segment-1.json')
    ghpages.git.add('event-segment-2.json')

    msg = "Event Update " + str(datetime.now())
    ghpages.index.commit(msg)
    ##os.system("ls a2events")
    ##os.system("git push ")

    ghpages.git.push()

def normalize_event(event_time):
    if len(event_time) < 11:
        converted_time = event_time
        comparison_time = dateutil.parser.parse(event_time + "T00:00:00-0500")
        comparison_time = comparison_time.astimezone(pytz.timezone('US/Eastern'))
    else:
        converted_time = dateutil.parser.parse(event_time)
        comparison_time = converted_time.astimezone(pytz.timezone('US/Eastern'))
        converted_time = str(comparison_time)
        converted_time = converted_time.replace(" ", "T")

    return {'converted': converted_time, 'comparison': comparison_time}

if __name__ == "__main__":
    main()
