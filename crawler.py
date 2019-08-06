from concurrent.futures import ThreadPoolExecutor

from database import ad_dao
from html_parser import parser


def main():
    # print("html_parser")
    ads = parser.parse_list_page()
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(add_ads, ads)


def add_ads(ad):
    ad = parser.parse_ad_page(ad, ad['Url'])
    ad_dao.insert_ad(ad)


if __name__ == "__main__":
    main()
