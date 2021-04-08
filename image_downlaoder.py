import pandas
import requests
import re
import pickle
df = pandas.read_csv('reddit_wsb.csv')

count_deleted = 0
links = []
for i, x in df.iterrows():
    if not x['is_self']:
        if x['body'] != '[deleted]':
            links.append(x)
        else:
            count_deleted += 1
print(len(links), count_deleted)

# index = -1
# for i,v in enumerate(links):
#     if v['id'] == 'l8rtk8':
#         index = i
#         break
# print(index)
# links = links[index+1:]
counter = 0
for x in links:
    try:
        good = False
        s = re.search('\.([^/]{1,4})$', x['url'])
        if s is not None:
            print(x['url'])
            r = requests.get(x['url'], allow_redirects=True)
            # print(x['id'], x['url'], r.status_code)
            if r.status_code == 200:
                print('{}.{}'.format(x['id'], s.group(1)), counter)
                open('downloads/{}.{}'.format(x['id'], s.group(1)), 'wb').write(r.content)
                good = True
                counter += 1
    except:
        continue
print(len(links), )

