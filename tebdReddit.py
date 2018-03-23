import tebdRedditAPI

top100twitter = tebdRedditAPI.requestRedditAPI("domain/twitter.com/top?sort=top&t=all&limit=25", None)

ctrl = True
cnt = 25
while ctrl is True:
    print(cnt)
    print(ctrl):
    print(top100twitter["data"]["children"][24]["data"]["name"])
    afterFullname = top100twitter["data"]["children"][24]["data"]["name"]
    top100twitter = tebdRedditAPI.requestRedditAPI("domain/twitter.com/top?sort=top&t=all&limit=100&before=%s" % (afterFullname), None)
    if top100twitter is None:
        ctrl = False
    else:
        cnt += 25
