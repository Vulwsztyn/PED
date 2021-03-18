import praw
import datetime as dt
from psaw import PushshiftAPI
from dotenv import load_dotenv
import os
load_dotenv(verbose=True)
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    password=os.getenv("PASSWORD"),
    user_agent=os.getenv("USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
)
api = PushshiftAPI(reddit)
start_ts = int(dt.datetime(2021, 1, 19, 12).timestamp())
end_ts = int(dt.datetime(2021, 2, 11, 12).timestamp())
# end_ts = start_ts + 1093144
subreddit = reddit.subreddit("wallstreetbets")
print(reddit.user.me())

should_end = False
current_end_ts = end_ts
how_many = 0
f = open("ids.txt", "w")
while not should_end:
    print(how_many, current_end_ts - start_ts)
    should_end = True
    for i in list(api.search_submissions(before=current_end_ts,
                                subreddit='wallstreetbets',
                                # filter=['url','author', 'title', 'subreddit'],
                                limit=100)):
        if (int(i.created_utc) - start_ts) < 0:
            break
        how_many += 1
        current_end_ts = int(i.created_utc)
        f.write(i.id)
        f.write('\n')
    else:
        should_end = False
f.close()