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
f = open("ids_filtered.txt", "r")
f1 = open("reddit_wsb.csv", "w", encoding="utf-8", newline='')
writer = csv.writer(f1)

should_end = False
how_many = 0
start = time.time()

writer.writerow('title;score;id;url;comms_num;created;body;timestamp;upvote_ratio;is_oc;permalink;name'.split(';'))
while not should_end:
    ids = []
    for _ in range(100):
        line = f.readline()
        if len(line) == 0:
            should_end = True
            break
        ids.append('t3_' + line[:-1])
    how_many += len(ids)
    for i in reddit.info(ids):
        line = [i.title, i.score, i.id, i.url, i.num_comments, i.created_utc,
                i.selftext.encode("unicode_escape").decode("utf-8"),
                time.ctime(int(i.created_utc)),
                i.upvote_ratio,
                i.is_original_content,
                i.permalink,
                i.name]

        writer.writerow(line)
    print(how_many, (time.time() - start))
f.close()
f1.close()
