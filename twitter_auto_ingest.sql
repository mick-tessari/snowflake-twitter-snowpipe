/*********************************************************************************
Create storage (database) to store the tweets
Create compute (warehouse) to run analytical queries on the tweets
*********************************************************************************/

use role sysadmin;

create or replace warehouse twitter_wh
  with warehouse_size = 'x-small'
  auto_suspend = 300
  auto_resume = true
  initially_suspended = true;

CREATE OR REPLACE DATABASE twitter_db;
USE SCHEMA twitter_db.public;


/*********************************************************************************
Create external S3 stage pointing to the S3 buckets storing the tweets
*********************************************************************************/

CREATE or replace STAGE twitter_db.public.tweets
    URL = 's3://mtessari-snowpipe-local/'
    CREDENTIALS = (AWS_KEY_ID = 'AKIATLKCS7Z3QX7TCBFG' AWS_SECRET_KEY = 'a36SFoGytIQ6ZHBSpTDsPU1YcAgdk/xHCx6hgkXD')
    file_format=(type='JSON')
    COMMENT = 'Tweets stored in S3';


/*********************************************************************************
Create new table for storing JSON data in native format into a VARIANT column
*********************************************************************************/

create or replace table tweets(tweet variant);

/*********************************************************************************
Create pipe for auto-ingesting tweets from S3 into the "tweets" Snowflake table
*********************************************************************************/

create or replace pipe twitter_db.public.tweetpipe auto_ingest=true as
    copy into twitter_db.public.tweets
    from @twitter_db.public.tweets
    file_format=(type='JSON');


/*********************************************************************************
Check that the pipe is created
Copy the notification_channel value of the pipe
*********************************************************************************/
show pipes;


/*********************************************************************************
Go to the AWS S3 console and update the event notifications with the
    notification_channel value
*********************************************************************************/

/*********************************************************************************
Check files in the bucket
Check that the pipe is running
*********************************************************************************/

-- rm @twitter_db.public.tweets;
list @twitter_db.public.tweets;
select $1 from @twitter_db.public.tweets;

select system$pipe_status('twitter_db.public.tweetpipe');

/*********************************************************************************
Create a flat view to be used in your favourite BI tool
*********************************************************************************/

create or replace view tweets_bi as
    select tweet:created_at::timestamp as created_at
    ,tweet:id::int as id
    ,tweet:lang::string as lang
    ,regexp_substr(tweet:source::string,'<a.*?>(.+?)</a>',1,1,'e') as source
    ,tweet:text::string as text
    ,tweet:truncated::boolean as truncated
    ,tweet:user.description::string as user_description
    ,tweet:user.id::int as user_id
    ,tweet:user.name::string as user_name
    ,tweet:user.screen_name::string as user_screen_name
    ,tweet:user.favourites_count::int as user_favourites_count
    ,tweet:user.followers_count::int as user_followers_count
    ,tweet:user.friends_count::int as user_friends_count
    ,tweet:user.profile_image_url::string as user_profile_image_url
    ,tweet:user.profile_image_url_https::string as user_profile_image_url_https
    ,tweet:favorite_count::int as favorite_count
    ,tweet:quote_count::int as quote_count
    ,tweet:retweet_count::int as retweet_count
    ,tweet:reply_count::int as reply_count
    ,tweet:retweeted::boolean as retweeted
    ,tweet:in_reply_to_status_id::int as in_reply_to_status_id
    ,tweet:retweeted_status.id::int as retweeted_status_id
    from tweets;

/*********************************************************************************
(optional) Load data files already in S3 before SQS notifications were configured
*********************************************************************************/

alter pipe tweetpipe refresh;

/*********************************************************************************
Check content of the tweets table - run multiple times to highlight auto-ingest
...or switch to the Tableau dashboard and see new data coming in....
*********************************************************************************/

select count(*) from tweets;
select * from tweets limit 10;
select * from tweets_bi limit 10;
