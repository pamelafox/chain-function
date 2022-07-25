import re
import urllib.request

from bs4 import BeautifulSoup

from ChainFunction.markov_chain import MarkovChain


def parse_bookpage(url):
    # https://www.gutenberg.org/ebooks/64317
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print("ERROR: Book page could not be opened", url)

    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    # Find the files table
    contents = soup.find("table", class_="files")
    # Find the plain text link
    link = contents.find("a", class_="link", type="text/plain")
    if not link:
        link = contents.find("a", class_="link", type="text/plain; charset=utf-8")
    text_url = f"https://www.gutenberg.org{link['href']}"
    print(text_url)
    try:
        response = urllib.request.urlopen(text_url)
    except urllib.error.HTTPError:
        print("ERROR: Book text could not be opened", text_url)

    text = response.read().decode("utf-8")
    booktext = re.split(r"\*\*\* START OF [\w\s]+ \*\*\*", text, 1)[1]
    return booktext


def create_planet_chain():
    # Just once
    # nltk.download('brown')
    # nltk.download('punkt')
    markov_chain = MarkovChain()
    urls = [
        "https://www.gutenberg.org/ebooks/23306",
        "https://www.gutenberg.org/ebooks/46768",
        "https://www.gutenberg.org/ebooks/16561",
        "https://www.gutenberg.org/ebooks/8400",
        "https://www.gutenberg.org/ebooks/19072",
    ]
    for url in urls:
        print(url)
        booktext = parse_bookpage(url)
        markov_chain.add_text(booktext)
    names = []
    for _ in range(0, 10):
        names.append(markov_chain.generate_word())
    return markov_chain
