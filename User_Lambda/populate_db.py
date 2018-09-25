import pymysql
import json
import time
import sys



def insert_users(cursor, users):
    for user in users:
        sql = "INSERT INTO Users(firebaseID, email, fName, lName, joinDate, bio) VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (user))
    # connection.commit()
    # print("Insert Users")

def insert_active_users(cursor, active_users):
    for active_user in active_users:
        sql = "INSERT INTO ActiveUsers(firebaseID, sessionID) VALUES(%s,%s)"
        cursor.execute(sql, (active_user))
    # connection.commit()

def insert_topics(cursor, topics):
    for topic in topics:
        sql = "INSERT INTO Topics(topic) VALUES(%s)"
        cursor.execute(sql, (topic))
    # connection.commit()
    # print("Insert Topics")

def insert_articles(cursor, articles):
    for article in articles:
        sql = "INSERT INTO Articles(source, topicID, articleURL, imageURL, author, title, description, dateAdded) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (article))
    # connection.commit()
    # print("Insert articles")

def insert_article_activities(cursor, article_activities):
    for article_activity in article_activities:
        sql = "INSERT INTO ArticleActivities(userID,articleID, activityType, dateAdded) VALUES(%s,%s,%s,%s)"
        cursor.execute(sql, (article_activity))
    # connection.commit()
    # print("Insert article activities")

def insert_comments(cursor, comments):
    for comment in comments:
        sql = "INSERT INTO Comments(userID, articleID, content, dateAdded) VALUES(%s,%s,%s,%s)"
        cursor.execute(sql, (comment))
    # connection.commit()
    # print("Insert comments")

def insert_connections(cursor, connections):
    for connection in connections:
        sql = "INSERT INTO Connections(follower, following) VALUES(%s,%s)"
        cursor.execute(sql, (connection))
    # connection.commit()
    # print("Insert connections")



def populate():

    try:
        connection = pymysql.connect(host="overlooked-db.ctpilp2ahgud.us-west-1.rds.amazonaws.com",user="overlooked_db", passwd="overlooked", db="overlooked_db", charset='utf8')
    except:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

    with connection.cursor() as cursor:
        populate_statements = []

        #create users
        # users = [
        #     ("asf24trgq5yq5y4q45c44w5v4", "jasonw@usc.edu", "Jason", "Witherspoon", '2017-12-25 23:59:59' , "BIO"),
        #     ("4b257octn403857v9348y6b8", "collinb@usc.edu", "Collin", "Bhojwani",'2011-12-25 23:59:59', "BIO"),
        #     ("5vuq4novy438tyiunvuyhuoi5y", "georges@usc.edu", "George", "Sehremelis",'2017-12-25 23:59:59', "BIO"),
        #     ("ew5vn89by56qv845o58ob8yn", "dylana@usc.edu", "Dylan", "Alesio",'2017-12-25 23:59:59', "BIO"),
        #     ("p8nyv5245by46b64yb654b43","georgem@usc.edu", "George", "Miller", '2017-12-25 23:59:59', "BIO"),
        #     ("7nw457n658m936n3868n3sd", "jayb@usc.edu", "Jay", "Bergstrom", '2017-12-25 23:59:59', "BIO")
        # ]
        # insert_users(cursor, users)
        # populate_statements.append(users)
        # connection.commit()

        #create activeUsers
        # active_users = [
        #     ("asf24trgq5yq5y4q45c44w5v4","IkqXnRIKqtBFv0jc"),
        #     ("4b257octn403857v9348y6b8","KHnguQYfNHzEOaQu"),
        #     ("5vuq4novy438tyiunvuyhuoi5y","VPSLkLVJrhjwxUTX"),
        #     ("ew5vn89by56qv845o58ob8yn","YgviPihk6pz2aQpX"),
        #     ("p8nyv5245by46b64yb654b43", "0RNTRTNN8UBMkNLb")
        # ]
        # insert_active_users(cursor, active_users)
        # populate_statements.append(active_users)
        # connection.commit()

        #create topics
        topics = [
            ("Government"),
            ("Innovation"),
            ("Corruption"),
            ("Human Rights"),
            ("Universities"),
            ("Sports")
        ]
        insert_topics(cursor, topics)
        populate_statements.append(topics)
        connection.commit()

        #create articles
        # articles = [
        #     ("SOURCE",1,
        #     "http://www.abc.net.au/news/2018-03-07/bitcoin-sports-bet-site-under-acma-probe-after-wilkie-complaint/9510512" ,
        #     "http://www.abc.net.au/news/image/5487174-16x9-700x394.jpg",
        #     "Jack Kerr",
        #     "Central American bitcoin sports betting site 'pretending' to be Australian in ACMA's sights",
        #     "An Australian-registered sports gambling website, which is based in Costa Rica and allows bets to placed with bitcoin, is under investigation after urging from independent federal MP Andrew Wilkie.",
        #     '2017-12-25 23:59:59'
        #     ),
        #
        #     ("SOURCE", 1,
        #     "https://www.newsbtc.com/2018/03/07/the-ultimate-guide-to-cannabis-tokens/",
        #     "https://s3.amazonaws.com/main-newsbtc-images/2018/03/06220527/budbo.png",
        #     "Guest Author",
        #     "The Ultimate Guide To Cannabis Tokens",
        #     "Disclaimer: The author does not provide investment advice. This article has been prepared for informational purposes only, and is not intended to provide, and should not be relied on for investment advice. By now, Bitcoin is as famous as can be. But deep down…",
        #     '2017-12-25 23:59:59'
        #     ),
        #
        #     ("SOURCE",2,
        #     "https://www.deepdotweb.com/2018/03/07/07-03-18-dark-web-cybercrime-roundup/",
        #     "https://www.deepdotweb.com/wp-content/uploads/2018/03/word-image-660x254.png",
        #     "C. Aliens",
        #     "07.03.18 Dark Web and Cybercrime Roundup",
        #     "Georgia Man Made Furanyl Fentanyl Pills in U-Haul Storage Unit A judge in Gwinnett County, Georgia, sentenced a 32-year-old man to 44 years in prison for producing counterfeit oxycodone pills. As usual, the counterfeits contained a fentanyl analogue instead o…",
        #     '2017-12-25 23:59:59'
        #     ),
        #
        #     ("SOURCE",3,
        #     "https://www.youbrandinc.com/crytocurrency/wyoming-blockchain-bill-rockets-ahead-for-signing/",
        #     "https://www.youbrandinc.com/wp-content/uploads/2018/03/Wyoming_bill2.max-800x800.jpg",
        #     "Scott Scanlon",
        #     "Wyoming Blockchain Bill Rockets Ahead for Signing",
        #     "In a landmark development for blockchain advancement, Wyoming’s state legislature has cleared what is known as House Bill 70 (HB 70), which exempts various types of crypto assets from securities laws. The bill was originally passed by Wyoming’s House of Repre…",
        #     '2017-12-25 23:59:59'
        #     ),
        #
        #     ("SOURCE",2,
        #     "https://www.newsbtc.com/2018/03/07/ethereum-price-technical-analysis-eth-usd-sell-rallies/",
        #     "https://s3.amazonaws.com/main-newsbtc-images/2018/03/07030835/Ethereum5.png",
        #     "Aayush Jindal",
        #     "Ethereum Price Technical Analysis – ETH/USD Sell on Rallies",
        #     "Key Highlights ETH price extended declines and traded below the $828 support level against the US Dollar. There is a major bearish trend line forming with resistance at $818 on the hourly chart of ETH/USD (data feed via SimpleFX). The pair is currently correc…",
        #     '2017-12-25 23:59:59'
        #     ),
        #
        #     ("SOURCE",2,
        #     "https://www.cnbc.com/2018/03/06/knight-frank-2018-wealth-report-the-ultra-rich-are-investing-in-cryptocurrencies.html",
        #     "https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2017/12/10/104890072-GettyImages-887657576.1910x1000.jpg",
        #     "Yen Nee Lee",
        #     "The world’s ultra-rich are investing more in cryptocurrencies — even if they may not understand it",
        #     "Around 21 percent of wealth advisers and private bankers surveyed by Knight Frank said their clients increased investments in cryptocurrencies in 2017.",
        #     '2017-12-25 23:59:59'
        #     ),
        #
        #     ("SOURCE",4,
        #     "https://www.cnet.com/news/dirty-coin-is-the-love-child-of-cryptocurrency-and-the-wu-tang-clan/",
        #     "https://cnet4.cbsistatic.com/img/q25E-Y1lSlpbT-1TNLjTRUa8rb8=/670x503/2018/03/07/c7697096-3541-4dca-83b2-e75a9875ad20/gettyimages-2296136.jpg",
        #     "Daniel Van Boom",
        #     "Dirty Coin is the love child of cryptocurrency and the Wu-Tang Clan - CNET",
        #     "The estate of Wu-Tang Clan rapper Ol' Dirty Bastard is launching a new cryptocurrency. We know what you're thinking -- about time.",
        #     '2017-12-25 23:59:59'
        #     ),
        #
        #     ("SOURCE",4,
        #     "https://www.youbrandinc.com/blockchain/what-you-should-know-about-the-chinese-blockchain-market/",
        #     "https://www.youbrandinc.com/wp-content/uploads/2018/03/blockchain_cryptocurrency_digital_security-100745939-large.3x2.jpg",
        #     "Scott Scanlon",
        #     "What you should know about the Chinese blockchain market",
        #     "Mar 6, 2018 8:23 AM PT Despite the hype, there is a case to be made that CIOs and other IT leaders do not need to know about blockchain technology. It is so new, so slow and so deeply unhelpful for many business processes that that one CIO described it as “a …",
        #     '2017-12-25 23:59:59'
        #     )
        # ]
        # insert_articles(cursor, articles)
        # populate_statements.append(articles)
        # connection.commit()

        #create article_activites
        # article_activities = [
        #     (1, 1, 'Like', '2017-12-25 23:59:59'),
        #     (1, 1, 'Share', '2017-12-25 23:59:59'),
        #     (1, 2, 'Like', '2017-12-25 23:59:59'),
        #     (1, 3, 'Share', '2017-12-25 23:59:59'),
        #     (1, 4, 'Like', '2017-12-25 23:59:59'),
        #
        #     (2, 1, 'Like', '2017-12-25 23:59:59'),
        #     (2, 1, 'Share', '2017-12-25 23:59:59'),
        #     (2, 2, 'Share', '2017-12-25 23:59:59'),
        #     (2, 3, 'Like', '2017-12-25 23:59:59'),
        #     (2, 5, 'Like', '2017-12-25 23:59:59'),
        #
        #     (3, 2, 'Like', '2017-12-25 23:59:59'),
        #     (3, 3, 'Like', '2017-12-25 23:59:59'),
        #     (3, 3, 'Share', '2017-12-25 23:59:59'),
        #     (3, 4, 'Like', '2017-12-25 23:59:59'),
        #     (3, 4, 'Share', '2017-12-25 23:59:59'),
        #
        #     (4, 1, 'Like', '2017-12-25 23:59:59'),
        #     (4, 2, 'Like', '2017-12-25 23:59:59'),
        #     (4, 2, 'Share', '2017-12-25 23:59:59'),
        #     (4, 3, 'Like', '2017-12-25 23:59:59'),
        #     (4, 4, 'Share', '2017-12-25 23:59:59'),
        #
        #     (5, 2, 'Like', '2017-12-25 23:59:59'),
        #     (5, 3, 'Like', '2017-12-25 23:59:59'),
        #     (5, 3, 'Share', '2017-12-25 23:59:59'),
        #     (5, 4, 'Like', '2017-12-25 23:59:59'),
        #     (5, 5, 'Share', '2017-12-25 23:59:59')
        # ]
        # insert_article_activities(cursor, article_activities)
        # populate_statements.append(article_activities)
        # connection.commit()

        #create comments
        # comments = [
        #     (1, 1, "THIS IS A TEST COMMENT", '2017-12-25 23:59:59'),
        #     (1, 1, "THIS IS A TEST COMMENT", '2017-12-25 23:59:59'),
        #     (1, 2, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (1, 3, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (1, 5, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #
        #     (2, 1, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (2, 2, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (2, 3, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (2, 4, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (2, 4, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #
        #     (3, 1, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (3, 2, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (3, 2, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (3, 4, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (3, 5, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #
        #     (4, 2, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (4, 2, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (4, 3, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (4, 4, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (4, 5, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #
        #     (5, 3, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (5, 4, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (5, 5, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (5, 6, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59'),
        #     (5, 6, "THIS IS ANOTHER TEST COMMENT", '2017-12-25 23:59:59')
        # ]
        # insert_comments(cursor, comments)
        # populate_statements.append(comments)
        # connection.commit()

        #create connections
        # connections = [
        #     (1, 2),
        #     (1, 3),
        #     (1, 4),
        #     (2, 1),
        #     (2, 3),
        #     (2, 5),
        #     (3, 4),
        #     (4, 1),
        #     (4, 3),
        #     (4, 5),
        #     (5, 1)
        # ]
        # insert_connections(cursor, connections)
        # populate_statements.append(connections)
        # connection.commit()


        print(populate_statements)

        connection.close()





# populate()
