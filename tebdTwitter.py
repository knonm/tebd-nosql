#! /home/mcanon/virtualenv/TEBD/bin/python3
import tebdCypherTwitter
import tebdTwitterAPI
from time import sleep
import py2neo
from py2neo import Graph

ignoreTooMany = False

graph = Graph(tebdCypherTwitter.neo4jUrl)
myUserTwitterID = "000000"

jsonContent = tebdTwitterAPI.requestAPI("users/show", "user_id=%s" % (myUserTwitterID))
graph.run(tebdCypherTwitter.cqlCreateMyUser, json=jsonContent)

flistCursor = "-1"
while flistCursor != "0":
    try:
        jsonContent = tebdTwitterAPI.requestAPI("friends/list", "user_id=%s&count=200&cursor=%s" % (myUserTwitterID, flistCursor))
        graph.run(tebdCypherTwitter.cqlCreateUsers % (myUserTwitterID), json=jsonContent)
        flistCursor = jsonContent["next_cursor_str"]
    except tebdTwitterAPI.HTTPTooManyError as err:
        print(err)
        if ignoreTooMany:
            break
        else:
            sleep(920)
    except tebdTwitterAPI.HTTPError as err:
        print(err)

usersTwitter = graph.data(tebdCypherTwitter.cqlFollowers % (myUserTwitterID))
for i in range(len(usersTwitter)):
    idTwitterUser = usersTwitter[i]["id"]
    try:
        jsonContent = tebdTwitterAPI.requestAPI("friends/list", "user_id=%s&count=30" % (idTwitterUser))
        graph.run(tebdCypherTwitter.cqlCreateUsers % (idTwitterUser), json=jsonContent)
    except tebdTwitterAPI.HTTPTooManyError as err:
        print(err)
        if ignoreTooMany:
            break
        else:
            sleep(920)
    except tebdTwitterAPI.HTTPError as err:
        print(err)

usersTwitter = graph.data(tebdCypherTwitter.cqlUsersTwitter)
for i in range(len(usersTwitter)):
    if "screen_name" in usersTwitter[i] and usersTwitter[i]["screen_name"] is not None:
        try:
            jsonContent = tebdTwitterAPI.requestAPI("search/tweets", 
            "q=from%%3A%s&count=100&result_type=popular" % (usersTwitter[i]["screen_name"]))
            for j in range(len(jsonContent["statuses"])):
                status = jsonContent["statuses"][j]
                hashtags = status["entities"]["hashtags"]
                if status["place"] is None:
                    country = None
                    city = None
                else:
                    country = status["place"]["country"]
                    city = status["place"]["full_name"]
                for k in range(len(hashtags)):
                    try:
                        graph.run(tebdCypherTwitter.cqlCreateHashtag,
                        createdAt=status["created_at"],
                        country=country,
                        city=city,
                        retweetCount=status["retweet_count"],
                        favoriteCount=status["favorite_count"],
                        hashtag=hashtags[k]["text"],
                        idUser=status["user"]["id"])
                    except py2neo.database.status.CypherTypeError as err:
                        print("country=%s\ncity=%s\ncreated_at=%s\ngeo=%s\nretweet_count=%s\nfavorite_count=%s\nhashtag=%s\nid_user=%s" % (country, city,
                        status["created_at"], status["geo"], status["retweet_count"], status["favorite_count"], hashtags[k]["text"], status["user"]["id"]))
        except tebdTwitterAPI.HTTPTooManyError as err:
            print(err)
            if ignoreTooMany:
                break
            else:
                sleep(920)
        except tebdTwitterAPI.HTTPError as err:
            print(err)
