FROM python:slim
RUN pip install -U pip
RUN pip install --no-cache-dir boto3
RUN pip install --no-cache-dir awscli
RUN pip install --no-cache-dir tweepy
RUN pip install --no-cache-dir datetime

# Insert your Twitter Developer app keys and tokens here
ENV AWS_Access_Key_ID="xxxxxxxxxxxxxxxxxxxx"\
    AWS_Secret_Access_Key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"\
    consumer_key="xxxxxxxxxxxxxxxxxxxxxxxxx"\
    consumer_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"\
    access_token="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"\
    access_token_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"\
    bucket="my-twitter-bucket"\
    keyword="MondayMotivation"

ENV PYTHONUNBUFFERED=1

COPY ./cert.pem .
COPY ./add_certs_to_certifi.py .
COPY ./twitter_local.py .
COPY ./twitter_local.sh .

RUN aws configure set aws_access_key_id $AWS_Access_Key_ID
RUN aws configure set aws_secret_access_key $AWS_Secret_Access_Key
RUN python ./add_certs_to_certifi.py
RUN ["chmod","+x","/twitter_local.sh"]
ENTRYPOINT ["/bin/sh","/twitter_local.sh"]
