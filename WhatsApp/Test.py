import requests

headers = {
    'Authorization': 'EAAV466qt0dwBAJNEPwISiC1KyjV5qPxKQV3ZCDtu8Elg9nTAOltzplyfl5urqGpNWW9oFdZA8NZCZBUkt27bHVqvFabtjeMC3d2Ti2QGUfWZA1ogGblVWJOSXgQJowkZAQQ5RrEQoVT6mzp9W8Hwm3hkr080e9EWFrS5nOKorTM31g8CTtYBMiXAMfJ5ILMmZBrcrkbbVx5zQZDZD',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = '{\n    "messaging_product": "whatsapp",\n    "to": "9978622901",\n    "text": {"body" : "hi"}\n   }'

response = requests.post('https://graph.facebook.com/v15.0/FROM_PHONE_NUMBER_ID/messages', headers=headers, data=data)

print(response.text)