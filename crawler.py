from html_parser import parser
from database import adDao

def main():
    print("html_parser")
    adUrls = parser.parseListPage("https://bostad.stockholm.se/Lista")
    print(len(adUrls))

    for url in adUrls:
        ad = parser.parseAdPage(url)
        adDao.insertAd(ad)
        # if new ad send email


if __name__ == "__main__":
    main()