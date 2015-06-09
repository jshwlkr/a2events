__author__ = 'Joshua Walker'

import ConfigParser
import json
import dateutil.parser
import facebook


def main():
    parser = ConfigParser.SafeConfigParser()
    parser.read('config.ini')
    secret = parser.get('facebook', 'secret')
    app_id = parser.get('facebook', 'app_id')
    token = facebook.get_app_access_token(app_id, secret)
    event_list = facebook_fetch(token)
    with open('data.json', 'w') as outfile:
        json.dump(event_list, outfile)


def facebook_fetch(token):
    try:
        graph = facebook.GraphAPI(access_token=token)
        with open('facebook.json') as data_file:
            data = json.load(data_file)
            event_list = []
            for each in data['venue']:
                try:
                    venue_events = graph.get_connections(id=each['id'], connection_name='events')
                    for event in venue_events['data']:
                        print event
                        try:
                            event_object = graph.get_object(event['id'])
                            converted_time = str(dateutil.parser.parse(event['start_time'], ignoretz=True))
                            event_list.append(
                                dict(name=event['name'], url='https://www.facebook.com/events/' + event['id'] + '/',
                                     date=converted_time, source='Facebook',
                                     description=event_object['description']))

                        except:
                            pass
                except:
                    pass
    except:
        pass
    
    return event_list

if __name__ == "__main__":
    main()
