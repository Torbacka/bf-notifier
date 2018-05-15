FROM python:3
ADD . /bfNotifier
RUN pip3 install -r ./bfNotifier/requirements.txt
CMD [ "python3", "./bfNotifier/crawler.py" ]