import os

neo4jUrl = os.environ.get('NEO4J_URL',"http://localhost:7474/db/data/")

cqlCreateMyUser = """
WITH {json} as us
MERGE (user:UserTwitter {id:us.id})
  ON CREATE SET
    user.name = us.name,
    user.location = us.location,
    user.screen_name = us.screen_name,
    user.followers_count = us.followers_count,
    user.friends_count = us.friends_count
  ON MATCH SET
    user.name = us.name,
    user.location = us.location,
    user.screen_name = us.screen_name,
    user.followers_count = us.followers_count,
    user.friends_count = us.friends_count
"""

cqlFollowers = """
MATCH (:UserTwitter {id:%s})-[:FOLLOWS]->(f:UserTwitter)
RETURN f.id AS id
"""

cqlCreateUsers = """
WITH {json} as dt
UNWIND dt.users as us
MERGE (user:UserTwitter {id:us.id})
  ON CREATE SET
    user.name = us.name,
    user.location = us.location,
    user.screen_name = us.screen_name,
    user.followers_count = us.followers_count,
    user.friends_count = us.friends_count
  ON MATCH SET
    user.name = us.name,
    user.location = us.location,
    user.screen_name = us.screen_name,
    user.followers_count = us.followers_count,
    user.friends_count = us.friends_count
MERGE (me:UserTwitter {id:%s})
WITH me, user
MERGE (me)-[:FOLLOWS]->(user)
"""

cqlUsersTwitter = """
MATCH (f:UserTwitter)
RETURN f.id AS id, f.screen_name AS screen_name
"""

cqlCreateHashtag = """
WITH {createdAt} as created_at, {country} as country, {city} as city, {retweetCount} as retweet_count, 
{favoriteCount} as favorite_count, {hashtag} as hashtag, {idUser} as id_user
MERGE (ht:HashtagTwitter {hashtag: hashtag, created_at: created_at})<-[:TWEETED]-(:UserTwitter {id: id_user})
  ON CREATE SET
    ht.retweet_count = retweet_count,
    ht.favorite_count = favorite_count,
    ht.city = city,
    ht.country = country
  ON MATCH SET
    ht.retweet_count = retweet_count,
    ht.favorite_count = favorite_count
"""

# NOT USED
cqlDeleteAll = """
MATCH (a:UserTwitter)-[b]->(c)
MATCH (d)-[e]->(f:UserTwitter)
MATCH (g:UserTwitter)
DELETE b
DELETE e
DELETE g
"""

cqlMatchAll = """
MATCH (a:UserTwitter)
RETURN a
"""
