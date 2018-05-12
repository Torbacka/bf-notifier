FROM python:3
ADD . /bfNotifier
RUN pip install pymongo BeautifulSoup urlopen
CMD [ "python", "./bfNotifier/crawler.py" ]