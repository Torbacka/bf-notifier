FROM python:3
ADD . /bf-notifier
RUN pip3 install -r ./bf-notifier/requirements.txt
CMD [ "python3", "./bf-notifier/crawler.py" ]