MATCH (a:UsersTwitter)
RETURN COUNT(a) AS cnt

MATCH (a:HashtagTwitter)
RETURN COUNT(a) AS cnt

MATCH ()-[a:FOLLOWS]->()
RETURN COUNT(a) AS cnt

MATCH ()-[a:TWEETED]->()
RETURN COUNT(a) AS cnt

#

MATCH (a:UsersTwitter)
WHERE a.location IS NOT NULL
AND a.location =~ ''
RETURN upper(a.location) AS localizacao
ORDER BY localizacao ASC

MATCH (a:UsersTwitter)
WHERE a.location IS NOT NULL
AND a.location =~ '^[a-zA-Z].+[a-zA-Z]$'
RETURN upper(a.location) AS localizacao
ORDER BY localizacao ASC

# Top lugares hashtags
MATCH (a:HashtagTwitter)
RETURN a.country AS pais, a.city AS cidade, COUNT(a) as qtd
ORDER BY qtd DESC

# Top hashtags postadas (ranking por quantidade de posts)
MATCH (a:HashtagTwitter)
RETURN a.hashtag AS hashtag, COUNT(a.hashtag) AS qtd
ORDER BY qtd DESC, hashtag ASC

# Hashtags mais influentes
MATCH (a:UserTwitter)-[:TWEETED]->(c:HashtagTwitter)
WHERE a.screen_name IS NOT NULL
WITH a.name AS name,
a.screen_name AS screen_name, 
c.hashtag AS hashtag,
a.followers_count AS followers_count, 
SUM(c.retweet_count) AS retweet_count,
SUM(c.favorite_count) AS favorite_count
WITH hashtag, retweet_count, favorite_count,
(toFloat('0.' + toString(followers_count)))*((retweet_count*1.5)+(favorite_count*1.25))*-1 AS rank
RETURN hashtag, SUM(rank) AS rank
ORDER BY rank DESC

MATCH (a:HashtagTwitter)
RETURN
a.hashtag AS hashtag,
COUNT(a.hashtag) AS qtd,
SUM(a.favorite_count) AS qtd_fav,
AVG(a.favorite_count) AS avg_fav,
SUM(a.retweet_count) AS qtd_retweet,
AVG(a.retweet_count) AS avg_retweet
ORDER BY qtd DESC, hashtag ASC

MATCH (a:HashtagTwitter)
RETURN a.hashtag AS hashtag, COUNT(a.hashtag) AS qtd
ORDER BY qtd DESC, hashtag ASC

MATCH (a:UserTwitter)-[:TWEETED]->(c:HashtagTwitter)
RETURN a.screen_name AS screen_name, COUNT(c.hashtag) AS hashtag_count
ORDER BY hashtag_count DESC

MATCH (a:UserTwitter)-[:TWEETED]->(c:HashtagTwitter)
WHERE a.screen_name IS NOT NULL
RETURN a.screen_name AS screen_name, COUNT(c) AS hashtag_count
ORDER BY hashtag_count DESC

(a.followers_count*COUNT(c.hashtag)+(c.retweet_count*1.5)+(c.favorite_count*1.25)) AS rank

# Pessoas mais influentes ou hashtags mais influentes (considera quantidade de seguidores)
MATCH (a:UserTwitter)-[:TWEETED]->(c:HashtagTwitter)
WHERE a.screen_name IS NOT NULL
WITH a.name AS name,
a.screen_name AS screen_name, 
c.hashtag AS hashtag,
a.followers_count AS followers_count, 
SUM(c.retweet_count) AS retweet_count,
SUM(c.favorite_count) AS favorite_count,
COUNT(c.hashtag) AS cnt_hashtag
RETURN name, screen_name, hashtag, (followers_count*cnt_hashtag+(retweet_count*1.5)+(favorite_count*1.25)) AS rank
ORDER BY rank DESC

# Pessoas mais influentes ou hashtags mais influentes (não considera quantidade de seguidores)
MATCH (a:UserTwitter)-[:TWEETED]->(c:HashtagTwitter)
WHERE a.screen_name IS NOT NULL
WITH a.name AS name,
a.screen_name AS screen_name, 
c.hashtag AS hashtag,
a.followers_count AS followers_count, 
SUM(c.retweet_count) AS retweet_count,
SUM(c.favorite_count) AS favorite_count
RETURN name, screen_name, hashtag, ((retweet_count*1.5)+(favorite_count*1.25)) AS rank
ORDER BY rank DESC
