import requests


def get_url(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(e)
