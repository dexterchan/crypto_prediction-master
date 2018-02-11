#FROM python:3.6.4-slim-stretch
FROM tensorflow/tensorflow:latest-py3



RUN pip3  --no-cache-dir install \
    keras \
    plotly \
    quandl \
    tweepy \
    textblob \
    seaborn

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app

ENTRYPOINT ["python3"]
CMD ["Continuous_Stream_Sentiment.py"]