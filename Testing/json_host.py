import requests

def hit():

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    response = requests.get('https://jsonblob.com/api/jsonBlob/1016218611752386560', headers=headers)

    curr = int(response.content.decode('ASCII'))

    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    json_data = curr+1
    
    response = requests.put('https://jsonblob.com/api/jsonBlob/1016218611752386560', headers=headers, json=json_data)

hit()