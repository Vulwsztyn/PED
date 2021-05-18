import praw
from praw.models import MoreComments
import datetime as dt
import time
import csv
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas
import pickle
df = pandas.read_csv('data/reddit_wsb.csv')

df = df.sort_values(by=['comms_num'], ascending=False)

print(df['id'])
plt.hist(df['comms_num'], bins=20)
plt.ylabel('Count')
plt.yscale('log')
plt.xlabel('Data')

plt.show()

load_dotenv()
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
print(df['comms_num'].iloc[0])
print(df['comms_num'].iloc[500])
print(df['comms_num'].iloc[1000])
ids = df['id'][1000:1010]

top_level_only = False
comments = {}
for i in ids:
    submission = reddit.submission(i)
    submission.comment_sort = "old"
    print(submission.permalink)
    try:
        submission.comments.replace_more(
            limit=None)
    except:
        print("wina reddita")

    comments[i] = []
    for j, comment in enumerate(submission.comments):
        if isinstance(comment, MoreComments):
            continue
        comments[i].append(comment)
        print(j)

    pickle.dump(comments, open( "./pickle/comments_circa_397.pkl", "wb" ))
