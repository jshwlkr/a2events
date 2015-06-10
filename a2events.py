from dateutil import tz

__author__ = 'Joshua Walker'

import ConfigParser
import json
import datetime
import dateutil.parser
import pytz
import facebook


def main():
    parser = ConfigParser.SafeConfigParser()
    parser.read('config.ini')
    secret = parser.get('facebook', 'secret')
    app_id = parser.get('facebook', 'app_id')
    token = facebook.get_app_access_token(app_id, secret)
    event_list = facebook_fetch(token)

    event_list = sorted(event_list, key=lambda item: item['date'])
    with open('data.json', 'w') as outfile:
        json.dump(event_list, outfile)


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
                            if 'timezone' in event:
                                converted_time = str(dateutil.parser.parse(event['start_time'], ignoretz=True))
                            else:
                                converted_time = dateutil.parser.parse(event['start_time'])
                                converted_time = str(converted_time.astimezone(pytz.timezone('US/Eastern')))
                                print converted_time

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
    print event_list
    return event_list


if __name__ == "__main__":
    main()
