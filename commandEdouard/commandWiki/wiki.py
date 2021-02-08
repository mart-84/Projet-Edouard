import requests
from bs4 import BeautifulSoup


def getRandomWiki():
    page = requests.get("https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard")
    url = page.url

    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find(id="firstHeading").get_text()
    a = soup.find_all("div", class_="mw-parser-output")[0].findChildren("p", recursive=False)
    b = a[0]
    try:
        if b["class"] == ["mw-empty-elt"]:
            b = a[1]
    except:
        pass

    content = b.get_text()

    return url, title, content