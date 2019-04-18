from concurrent.futures import ThreadPoolExecutor

from database import ad_dao
from html_parser import parser


def main():
    # print("html_parser")
    add_range = range(143000)
    with ThreadPoolExecutor(max_workers=200) as executor:
        executor.map(add_old_ads, add_range)


def add_old_ads(i):
    ad = parser.parse_ad_page(dict(), "/Lista/Details/?aid=" + str(i))
    ad['AnnonsId'] = i
    if i % 5000 == 0:
        print("Processed : " + str(i))
    if bool(ad):
        ad_dao.insert_ad(ad)


if __name__ == "__main__":
    main()
