import requests
from requests import session
from bs4 import BeautifulSoup

class ParsingError(Exception):
    pass

class JsonResponseError(Exception):
    pass

def parse_csrf_token(text):
    soup = BeautifulSoup(text)
    element = soup.find(attrs={'name': 'csrf_token'})
    if not (element and element.get('value')):
        raise ParsingError(
            'Error parsing csrf_token. No html element with name="crsf_token"'
        )
    return element['value']

def parse_seat(text):
    soup = BeautifulSoup(text)
    elements = soup.find_all('div', class_='seat open')
    if not (elements and elements[0].get('data-id')):
        raise ParsingError(
            'Error parsing seat. No html elements with class="seat open" or ' 
            'missing data-id attribute'
        )
    return elements[0]['data-id']


def verify_json_response(r):
    if 'application/json' not in r.headers['content-type']:
        raise JsonResponseError('Response from the server was not Json')
    if 'success' not in r.json():
        raise JsonResponseError('Json response missing success field.')
    if str(r.json().get('success')) not in ['True', 'False']:
        raise JsonResponseError('Json success field not a boolean.')

class SoulCycle():
    def __init__(self):
        self.s = session()
    
    def authenticate(self, email, password):
        r = self.s.get('https://www.soul-cycle.com')
        r.raise_for_status()
        data = { 
            'csrf_token': parse_csrf_token(r.text),
            'email': email, 
            'password': password
        }
        r = self.s.post('https://www.soul-cycle.com/login/', data=data)
        r.raise_for_status()
        verify_json_response(r)
        return r.json().get('success')


    def register_for_class(self, class_):
        r = self.s.get('https://www.soul-cycle.com/find-a-class/select-bike/%d/' % class_)
        r.raise_for_status()
        data = {
            'csrf_token': parse_csrf_token(r.text),
            'seat': parse_seat(r.text),
            'class': class_
        }
        r = self.s.post('https://www.soul-cycle.com/find-a-class/reserve-bike/', data=data)
        r.raise_for_status()
        verify_json_response(r)
        if not r.json().get('success'):
            raise JsonResponseError('Class %s registration error') 

if __name__ == '__main__':
    soul_cycle = SoulCycle()
    soul_cycle.authenticate('joshua.massover@gmail.com', '32974090Jdm')
    soul_cycle.register_for_class(379333)
        

