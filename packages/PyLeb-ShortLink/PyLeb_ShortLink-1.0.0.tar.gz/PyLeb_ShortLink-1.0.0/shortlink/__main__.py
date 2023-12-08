import urllib
import requests
def short(Link:str):
    link = "http://tinyurl.com/api-create.php"
    try:
        url = link + "?" \
        + urllib.parse.urlencode({"url": Link})
        res = requests.get(url)
        short=res.text
    except Exception as e:
        short="can't short this link "
    return short
