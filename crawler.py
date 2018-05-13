from html_parser import parser
from database import adDao


def main():
    # print("html_parser")
    ads = parser.parseListPage()
    print(len(ads))
    for ad in ads:
        ad = parser.parseAdPage(ad, ad['Url'])
        print(ad)
        adDao.insertAd(ad)


if __name__ == "__main__":
    main()
