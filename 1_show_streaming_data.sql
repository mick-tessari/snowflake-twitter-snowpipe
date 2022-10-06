use role sysadmin;
use warehouse twitter_wh;
use schema twitter_db.public;

/*********************************************************************************
Check files in the bucket
Check that the pipe is running
*********************************************************************************/

list @twitter_db.public.tweets;
select $1 from @twitter_db.public.tweets limit 10;

show pipes;
select system$pipe_status('twitter_db.public.tweetpipe');

/*********************************************************************************
Check content of the tweets table - run multiple times to highlight auto-ingest
*********************************************************************************/
select count(*) from tweets;
select * from tweets limit 100;


/*********************************************************************************
Create a flat view to be used in Tableau
*********************************************************************************/

create or replace view tweets_bi as
select
    tweet:keyword::varchar as keyword,
    tweet:data:author_id::integer as author_id,
    tweet:data:created_at::timestamp as created_at,
    tweet:data:id::integer as tweet_id,
    tweet:data:lang::varchar as lang,
    tweet:data:public_metrics:like_count::integer as like_count,
    tweet:data:public_metrics:quote_count::integer as quote_count,
    tweet:data:public_metrics:reply_count::integer as reply_count,
    tweet:data:public_metrics:retweet_count::integer as retweet_count,
    tweet:data:text::varchar as text,
from tweets;

/*********************************************************************************
Check content of the tweets view - run multiple times to highlight auto-ingest
...or switch to the Tableau dashboard and see new data coming in....
*********************************************************************************/

select count(*) from tweets_bi;
select * from tweets_bi limit 100;
