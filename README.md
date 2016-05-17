# 6bacon_bot


This is the twitter bot for Six Degrees of Francis Bacon.

Seen here: https://twitter.com/6Bacon_Bot

Simplified steps:

1. Generate a random uid
2. Insert that uid into a relationship url
3. Generate a statement from the relationship url
4. Generate people uid's from the relationship json
5. Insert people uids into the people urls 
6. Generate a statement from the people urls
7. Additional modifiers and methods included to account for variations in human language



Six Degrees of Francis Bacon outputs nearly any page as a json file by simply adding .json after the uid.


E.g. "http://www.sixdegreesoffrancisbacon.com/relationships/#{uid}" 

can become 

"http://www.sixdegreesoffrancisbacon.com/relationships/#{uid}.json"



This bot pulls from people and relationship urls.

With a bit of work, the bot can be pointed towards particular demographics, groups, year ranges, etc.