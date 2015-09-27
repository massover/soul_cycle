import requests
import logging
from requests import Session
from bs4 import BeautifulSoup

class ParsingError(Exception):
    pass

class JsonResponseError(Exception):
    pass

def parse_csrf_token(text):
    soup = BeautifulSoup(text)
    element = soup.find(attrs={'name': 'csrf_token'})
    if not (element and element.get('value')):
        error = 'Error parsing csrf_token. No html element with name="crsf_token"'
        logging.error(error)
        raise ParsingError(error)
    return element['value']

def parse_seat(text):
    soup = BeautifulSoup(text)
    elements = soup.find_all('div', class_='seat open')
    if not (elements and elements[0].get('data-id')):
        error = 'Error parsing seat. No html elements with class="seat open"' + \
                'or missing data-id attribute'
        logging.error(error)
        raise ParsingError(error)
    return elements[0]['data-id']

def parse_reservation_id(text):
    soup = BeautifulSoup(text)
    element = soup.find(attrs={'data-reservation-id': True})
    if not (element and element.get('data-reservation-id')):
        error = 'Error parsing data-reservation-id. No html element with that attr'
        logging.error(error)
        raise ParsingError(error)
    return element['data-reservation-id']

def verify_json_response(r):
    if 'application/json' not in r.headers['content-type']:
        error = 'Response from the server was not Json'
        logging.error(error)
        raise JsonResponseError(error)
    if 'success' not in r.json():
        error = 'Json response missing success field'
        logging.error(error)
        raise JsonResponseError(error)
    if str(r.json().get('success')) not in ['True', 'False']:
        raise JsonResponseError('Json success field not a boolean.')
        error = 'Json response success field was not a boolean'
        logging.error(error)
        raise JsonResponseError(error)


class SoulCycleSession(Session):
    def __init__(self, *args, **kwargs):
        super(SoulCycleSession, self).__init__(*args, **kwargs)
        self.is_authenticated = False
    
    #@authentication_required
    def register_for_class(self, class_):
        r = self.get('https://www.soul-cycle.com/find-a-class/select-bike/%d/' % class_)
        r.raise_for_status()
        data = {
            'csrf_token': parse_csrf_token(r.text),
            'seat': parse_seat(r.text),
            'class': class_
        }
        r = self.post('https://www.soul-cycle.com/find-a-class/reserve-bike/', data=data)
        r.raise_for_status()
        verify_json_response(r)
        if not r.json().get('success'):
            error = 'Class %s registration error' % class_
            logging.error(error)
            raise JsonResponseError(error) 


    #@authentication_required
    def unregister_for_class(self):
        r = self.get('https://www.soul-cycle.com/me/')
        r.raise_for_status()
        data = {
            'reservation_id': parse_reservation_id(r.text),
            'csrf_token': parse_csrf_token(r.text)
        }
        r = self.post('https://www.soul-cycle.com/me/unreserve-class/', data=data)
        r.raise_for_status()
        verify_json_response(r)
        if not r.json().get('success'):
            error = 'Error unregistering for class'
            logging.error(error)
            raise JsonResponseError(error) 


    #@authentication_required
    def logout(self):
        r = self.get('https://www.soul-cycle.com/logout')
        r.raise_for_status()
        self.is_authenticated = False

    
    def __exit__(self, *args):
        self.logout()
        self.close()    


def login(email,password):
    s = SoulCycleSession()
    r = s.get('https://www.soul-cycle.com')
    r.raise_for_status()
    data = { 
        'csrf_token': parse_csrf_token(r.text),
        'email': email, 
        'password': password
    }
    r = s.post('https://www.soul-cycle.com/login/', data=data)
    r.raise_for_status()
    verify_json_response(r)
    s.is_authenticated = r.json().get('success')    
    return s
