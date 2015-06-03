__author__ = 'Joshua Walker'

import ConfigParser
import json
import facebook

def main():
    parser = ConfigParser.SafeConfigParser()
    parser.read('config.ini')
    secret = parser.get('facebook', 'secret')
    app_id = parser.get('facebook', 'app_id')
    token = facebook.get_app_access_token(app_id, secret)
    event_list = facebook_fetch(token)
    with open('event_list.json', 'w') as outfile:
        json.dump(event_list, outfile)

def facebook_fetch(token):
    graph = facebook.GraphAPI(access_token=token)
    with open('facebook.json') as data_file:
        data = json.load(data_file)
        event_list = []
        for each in data['venue']:
            venue_events = graph.get_connections(id=each['id'], connection_name='events')
            for event in venue_events['data']:
                event_object = graph.get_object(event['id'])
                event_list.append({'name': event['name'], 'url': 'https://www.facebook.com/events/' + event['id'] + '/', 'time': event['start_time']})

    return event_list

if __name__ == "__main__":
    main()
