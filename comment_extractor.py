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

df = df.sort_values(by=['comms_num'], ascending=True)

# print(df['id'])
# plt.hist(df['comms_num'], bins=20)
# plt.ylabel('Count')
# plt.yscale('log')
# plt.xlabel('Data')
#
# plt.show()

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
start = time.time()
# print(df['comms_num'].iloc[0])
# print(df['comms_num'].iloc[500])
# print(df['comms_num'].iloc[1000])
ids = df['id'][:]

top_level_only = False
comments = {"post_id": 0}
# comments = pickle.load(open("./pickle/comments_all/comments_all.pkl", "rb"))
current_id = 38201
j = 0
for i in ids:
    print(str(j) + '/' + str(len(ids)))
    if j < current_id:
        j += 1
        continue
    submission = reddit.submission(i)
    submission.comment_sort = "old"
    print(submission.permalink)
    try:
        submission.comments.replace_more(
            limit=None)
        print(submission.num_comments)
        print(len(submission.comments.list()))
        comments[i] = []
        for _, comment in enumerate(submission.comments.list()):
            if isinstance(comment, MoreComments):
                continue
            comments[i].append(comment)
    except:
        print("wina reddita")

    if j % 100 == 0:
        comments["post_id"] = j
        pickle.dump(comments, open("./pickle/comments_all/comments_all_" + str(j) + ".pkl", "wb"))
    j += 1
