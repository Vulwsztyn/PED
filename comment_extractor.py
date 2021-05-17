import praw
import datetime as dt
import time
import csv
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
print(reddit.user.me())


should_end = False
how_many = 0
start = time.time()

ids = ["3hahrw"]

top_level_only = False

for i in ids:
    submission = reddit.submission(i)
    print(submission.permalink)
    submission.comments.replace_more(
        limit=None)
    for j, comment in enumerate(submission.comments.list()):
        print(j, comment.body)
