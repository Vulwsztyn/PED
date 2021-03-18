import praw
import datetime as dt
import time
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
f = open("ids.txt", "r")
f1 = open("ids_filtered.txt", "w")
f2 = open("all.txt", "w")
to_omit = 0

should_end = False
how_many=0
start = time.time()
while not should_end:
    ids = []
    for _ in range(100):
        line = f.readline()
        if len(line) == 0:
            should_end=True
            break
        ids.append('t3_'+line[:-1])
    how_many+=len(ids)
    for i in reddit.info(ids):
        is_not_deleted = i.is_robot_indexable and i.selftext != '[removed]' and i.selftext != '[deleted]'
        if is_not_deleted:
            f1.write(i.id+'\n')
        f2.write(i.id+" "+ str(int(i.created_utc))+" "+ ('1' if is_not_deleted else '0')+'\n')
    print(how_many, (time.time()-start))
f.close()
f1.close()
f2.close()