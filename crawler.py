from concurrent.futures import ThreadPoolExecutor

from html_parser import parser
from database import adDao


def main():
    # print("html_parser")
    ads = parser.parseListPage()
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(addAds, ads)


def addOldAds(i):
    ad = parser.parseAdPage(dict(), "Lista/Details/?aid=" + i)
    adDao.insertAd(ad)

def addAds(ad):
    ad = parser.parseAdPage(ad, ad['Url'])
    print(ad)
    adDao.insertAd(ad)


if __name__ == "__main__":
    main()
