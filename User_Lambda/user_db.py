import pymysql
import json
import sys
import json
import time
import rds_config
import random
import string
import boto3
import s3_image_handler
import time

class user_db:

    try:

        # 1) DB on Overlooked account in Private Subnet
        connection = pymysql.connect(host="overlooked-db.ctpilp2ahgud.us-west-1.rds.amazonaws.com",user="overlooked_db", passwd="overlooked", db="overlooked_db", charset='utf8')


    except:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()


    #uploadImage
    def uploadImage(self, firebaseID, profilePic):
        s3URL = s3_image_handler.image_handler(firebaseID, profilePic)
        return s3URL

    #search
    def search(self, keywords):
        # parse keywords
        keywords = keywords.split()
        results = {}
        results['users'] = self.userSearch(keywords)
        results['articles'] = self.articleSearch(keywords)

        return results

    # userSearch: returns list of user objects that match on one or more keywords
    def userSearch(self, keywords):
        results = []
        sessionIDs = self.getSessionIDs()
        for sessionID in sessionIDs:
            user = self.getUserData(sessionID)
            userInfo = {}
            userInfo['sessionID'] = sessionID
            userInfo['fName'] = user['fName']
            userInfo['lName'] = user['lName']
            userInfo['profilePic'] = "THIS WILL BE PROFILE PIC URL"

            for keyword in keywords:
                if keyword.lower() in user['fName'].lower():
                    results.append(userInfo)
                if keyword.lower() in user['lName'].lower():
                    results.append(userInfo)
                # if keyword.lower() in user['bio'].lower():
                #     results.append(userInfo)

        return results


    # articleSearch: returns list of user objects that match on one or more keywords
    def articleSearch(self, keywords):
        results = []
        articles = self.getArticleData(sessionID=None, topic="all")
        for article in articles:
            for keyword in keywords:
                if keyword in article['title'].lower() and article['articleID'] not in results:
                    results.append(article)
                if keyword in article['description'].lower() and article['articleID'] not in results:
                    results.append(article)
                # if keyword in article['topic'].lower() and article['articleID'] not in results:
                #     results.append(article)
                # if keyword in article['author'].lower() and article['articleID'] not in results:
                #     results.append(article)
        return results

    # getFirebaseID: get the firebaseID of the user specified
    def getFirebaseID(self, userID):
        with self.connection.cursor() as cursor:
            sql = "SELECT firebaseID FROM Users WHERE userID=%s"
            cursor.execute(sql,(userID))
            result = cursor.fetchall()
        result = result[0][0]

        return result


    # getSessionID get the current sessionID of the user specified
    def getSessionID(self, userID):
        with self.connection.cursor() as cursor:
            sql = "SELECT a.sessionID FROM Users u JOIN ActiveUsers a  ON u.firebaseID = a.firebaseID WHERE u.userID=%s"
            cursor.execute(sql,(userID))
            result = cursor.fetchall()
        result = result[0][0]
        return result

    # )"ID: get the userID (User Table primary key) of the user specified
    def getUserID(self, sessionID):
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID FROM Users u JOIN ActiveUsers a ON u.firebaseID = a.firebaseID WHERE a.sessionID=%s"
            cursor.execute(sql,(sessionID))
            result = cursor.fetchall()
        result = int(result[0][0])

        return result

    #getSessionIDs: get a list of all the ActiveUser sessionID's
    def getSessionIDs(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT sessionID FROM ActiveUsers"
            cursor.execute(sql)
            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            out.append(result[i][0])
        return out

    #getFirebaseIDs: get a list of all the ActiveUser firebaseID's
    def getFirebaseIDs(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT firebaseID FROM ActiveUsers"
            cursor.execute(sql)
            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            out.append(result[i][0])
        return out


    # loginUser: login (assign randomly generated) an authorized user given the firebaseID
    def loginUser(self, firebaseID):
        with self.connection.cursor() as cursor:
            currentSessionIDs = self.getSessionIDs()
            currentFirebaseIDs = self.getFirebaseIDs()
            #generate random sessionID
            # newSessionID = random.randint(1,500000)
            newSessionID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            # make sure sessionID is unique
            while newSessionID in currentSessionIDs:
                newSessionID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            sql = "DELETE FROM  ActiveUsers WHERE firebaseID=%s"
            cursor.execute(sql, (firebaseID))
            self.connection.commit()
            time.sleep(1.25)
            sql = "INSERT INTO ActiveUsers(firebaseID, sessionID) VALUES(%s,%s)"
            cursor.execute(sql, (firebaseID, newSessionID))
            # sql = "UPDATE ActiveUsers SET sessionID=%s WHERE firebaseID=%s"
            # cursor.execute(sql, (newSessionID, firebaseID))
            self.connection.commit()

        # on successful login, return user info of logged in user
        # result = self.getUserData(sessionID)
        # return result
        #
        # on successful login return new sessionID
        return newSessionID



    # logoutUser:
    def logoutUser(self, firebaseID):
        with self.connection.cursor() as cursor:
            currentSessionIDs = self.getSessionIDs()
            currentFirebaseIDs = self.getFirebaseIDs()
            # generate new random sessionID to invalidate current sessionID
            newSessionID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            # ensure unique sessionID
            while newSessionID in currentSessionIDs:
                newSessionID = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            # sql = "DELETE FROM  ActiveUsers WHERE firebaseID=%s"
            # cursor.execute(sql, (firebaseID))
            # sql = "INSERT INTO ActiveUsers(firebaseID, sessionID) VALUES(%s,%s)"
            # cursor.execute(sql, (firebaseID, newSessionID))
            sql = "UPDATE ActiveUsers SET sessionID=%s WHERE firebaseID=%s"
            cursor.execute(sql, (newSessionID, firebaseID))
            self.connection.commit()


    # getUserData: return all needed user information
    def getUserData(self, sessionID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "SELECT email, fName, lName, bio, joinDate, profilePic FROM Users WHERE userID=%s"
            cursor.execute(sql, (userID))
            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            user = {}
            user['email'] = result[i][0]
            user['fName'] = result[i][1]
            user['lName'] = result[i][2]
            user['bio'] = result[i][3]
            user['joinDate'] = str(result[i][4])
            user['profilePic'] = result[i][5]
            # number of people following the user
            user['numFollowingUser'] = len(self.followingUserIDs(sessionID))
            # number of people followed by the user
            user['numFollowedByUser'] = len(self.followedByUserIDs(sessionID))
            # list of names of users following the user
            user['listFollowingUser'] = self.listFollowingUser(sessionID)
            # list of names of users followed by the user
            user['listFollowedByUser'] = self.listFollowedByUser(sessionID)
            # list of articles that the user has interacted with, and their action
            user['articleActivities'] = self.getUserArticleActivities(sessionID)
            # list of comments that the user has interacted with, and their action and information about the article commented on
            user['commentActivities'] = self.getUserCommentActivities(sessionID)
            self.connection.commit()

        return user

    # getUser: return all needed user information
    def getUser(self, firebaseID):
        with self.connection.cursor() as cursor:
            sql = "SELECT userID FROM Users WHERE firebaseID=%s"
            cursor.execute(sql, (firebaseID))
            result = cursor.fetchall()
        return result

    # addUser
    def addUser(self, firebaseID, email, fName, lName, bio):
        ts = time.gmtime()
        joinDate = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        profilePic = " "
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO Users (firebaseID, email, fName, lName, bio, joinDate, profilePic) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(firebaseID, email, fName, lName, bio, joinDate, profilePic))
        self.connection.commit()
        # automatically login user when creating a new account
        result = self.loginUser(firebaseID)
        return result


    def editUser(self, sessionID, email, fName, lName, bio, profilePic):
        userID = self.getUserID(sessionID)
        firebaseID = self.getFirebaseID(userID)
        userData = self.getUserData(sessionID)
        s3URL =  self.uploadImage(firebaseID, profilePic)
        # s3URL = profilePic
        with self.connection.cursor() as cursor:
            sql = "UPDATE Users SET email=%s, fName=%s, lName=%s, bio=%s, profilePic=%s WHERE userID=%s"
            cursor.execute(sql,(email, fName, lName, bio, s3URL, userID))
        self.connection.commit()

### BEGIN RECURSIVE DELETE FUNCTIONS

    def deleteUser(self, sessionID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            self.deleteComments(userID)
            self.deleteShares(userID)
            self.deleteLikes(userID)
            self.deleteActiveUser(sessionID)
            self.deleteFollowing(userID)
            self.deleteFollowedBy(userID)

            sql = "DELETE FROM Users WHERE userID=%s"
            cursor.execute(sql,(userID))
        self.connection.commit()


    def deleteComments(self, userID):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM Comments WHERE userID=%s"
            cursor.execute(sql,(userID))
            self.connection.commit()

    def deleteShares(self, userID):
        activityType = "Share"
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM ArticleActivities WHERE userID=%s AND activityType=%s"
            cursor.execute(sql,(userID,activityType))
            self.connection.commit()


    def deleteLikes(self, userID):
        activityType = "Like"
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM ArticleActivities WHERE userID=%s AND activityType=%s"
            cursor.execute(sql,(userID, activityType))
            self.connection.commit()

    def deleteCommentLikes(self, userID):
        activityType = "Like"
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM CommentActivities WHERE userID=%s AND activityType=%s"
            cursor.execute(sql,(userID, activityType))
            self.connection.commit()

    def deleteActiveUser(self, sessionID):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM ActiveUsers WHERE sessionID=%s"
            cursor.execute(sql,(sessionID))
            self.connection.commit()


    def deleteFollowing(self, userID):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM Connections WHERE following=%s"
            cursor.execute(sql,(userID))
            self.connection.commit()

    def deleteFollowedBy(self, userID):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM Connections WHERE follower=%s"
            cursor.execute(sql,(userID))
            self.connection.commit()

### END RECURSIVE DELETE FUNCTIONS

    #getArticleIDs
    def getArticleIDs(self, articleList):
        articleIDs = []
        for i in range(len(articleList)):
            articleIDs.append(articleList[i]['articleID'])
        return articleIDs

    #getArticleData
    def getArticleData(self, sessionID, topic):
        with self.connection.cursor() as cursor:
            # if there is not a specified topic
            if(topic == "all"):
                sql = "SELECT a.articleID, a.articleURL, a.imageURL, t.topic, a.author, a.title, a.description, a.dateAdded, a.source  FROM Articles a, Topics t  WHERE a.topicID = t.topicID "# ORDER BY %s
                cursor.execute(sql)
            # if there is a specificied topic
            else:
                sql = "SELECT a.articleID, a.articleURL, a.imageURL, t.topic, a.author, a.title, a.description, a.dateAdded, a.source FROM Articles a, Topics t WHERE a.topicID = t.topicID  AND t.topic=%s "#ORDER BY %s LIMIT %s"
                cursor.execute(sql, (topic))
            result = cursor.fetchall()

        articles = []
        for i in range(len(result)):
            article = {}
            articleID = result[i][0]
            article['articleID'] = articleID
            article['articleURL'] = result[i][1]
            article['imageURL'] = result[i][2]
            article['topic'] = result[i][3]
            article['author'] = result[i][4]
            article['title'] = result[i][5]
            article['description'] = result[i][6]
            article['dateAdded'] = str(result[i][7])
            article['source'] = result[i][8]
            # returns comment/user information for each comment made on the article
            article['comments'] = self.getArticleComments(articleID)
            # returns user information for each user that liked the article
            article['likes'] = self.getArticleLikesInfo(articleID)
            # returns user information for each user that shared the article
            article['shares'] = self.getArticleSharesInfo(articleID)
            # if sessionID is given, check if userID has shared and/or liked current article
            if (sessionID):
                article['userHasLiked'] = self.likedArticle(sessionID, articleID)
                article['userHasShared'] = self.sharedArticle(sessionID, articleID)
            articles.append(article)
        self.connection.commit()

        return articles

    # getArticles: get ONLY article specific information (i.e. no comments, likes, or shares)
    def getArticles(self, sessionID, topic):
        with self.connection.cursor() as cursor:
            # if there is not a specificied topic
            if(topic == "all"):
                sql = "SELECT a.articleID, a.articleURL, a.imageURL, t.topic, a.author, a.title, a.description, a.dateAdded  FROM Articles a, Topics t WHERE a.topicID = t.topicID "#  ORDER BY %s   LIMIT %s "
                cursor.execute(sql)
            # if there is a specificied topic
            else:
                sql = "SELECT a.articleID, a.articleURL, a.imageURL, t.topic, a.author, a.title, a.description, a.dateAdded FROM Articles a, Topics t WHERE a.topicID = t.topicID AND t.topic=%s"# ORDER BY %s  LIMIT %s"
                cursor.execute(sql, (topic))
            result = cursor.fetchall()

        articles = []
        for i in range(len(result)):
            articleInfo = {}
            articleInfo['articleID'] = result[i][0]
            articleInfo['articleURL'] = result[i][1]
            articleInfo['imageURL'] = result[i][2]
            articleInfo['topic'] = result[i][3]
            articleInfo['author'] = result[i][4]
            articleInfo['title'] = result[i][5]
            articleInfo['description'] = result[i][6]
            articleInfo['dateAdded'] = str(result[i][7])
            if (sessionID):
                articleInfo['userHasLiked'] = self.likedArticle(sessionID, articleID)
                articleInfo['userHasShared'] = self.sharedArticle(sessionID, articleID)
            articles.append(articleInfo)

        self.connection.commit()
        return articles

    #getArticleLikesInfo
    def getArticleInfo(self, sessionID, articleID):
        with self.connection.cursor() as cursor:
            # if there is not a specificied topic
            sql = "SELECT articleURL, imageURL, title, author, description, dateAdded  FROM Articles WHERE articleID=%s"#  ORDER BY %s   LIMIT %s "
            cursor.execute(sql,(articleID))
            result = cursor.fetchall()
        for i in range(len(result)):
            articleInfo = {}
            articleInfo['articleURL'] = result[i][0]
            articleInfo['imageURL'] = result[i][1]
            articleInfo['title'] = result[i][2]
            articleInfo['author'] = result[i][3]
            articleInfo['description'] = result[i][4]
            articleInfo['dateAdded'] = str(result[i][5])
            # returns comment/user information for each comment made on the article
            articleInfo['comments'] = self.getArticleComments(articleID)
            # returns user information for each user that liked the article
            articleInfo['likes'] = self.getArticleLikesInfo(articleID)
            # returns user information for each user that shared the article
            articleInfo['shares'] = self.getArticleSharesInfo(articleID)
            # if sessionID is given, check if userID has shared and/or liked current article
            if (sessionID):
                articleInfo['userHasLiked'] = self.likedArticle(sessionID, articleID)
                articleInfo['userHasShared'] = self.sharedArticle(sessionID, articleID)

        return articleInfo


    # getArticleLikesIDs: get userID for each user who shared specified article
    def getArticleLikesIDs(self, articleID):
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID FROM ArticleActivities AS aa JOIN Users AS u ON aa.userID = u.userID WHERE aa.activityType='Like' AND aa.articleID=%s"
            cursor.execute(sql,(articleID))
            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            out.append(sessionID)
        return out

    # getArticleLikesInfo: get user info for each user who likes specified article
    def getArticleLikesInfo(self, articleID):
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID, u.fName, u.lName, aa.dateAdded FROM ArticleActivities AS aa JOIN Users AS u ON aa.userID = u.userID WHERE aa.activityType='Like' AND aa.articleID=%s ORDER BY aa.dateAdded DESC"
            cursor.execute(sql,(articleID))
            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            likeInfo = {}
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            likeInfo['sessionID'] = sessionID
            likeInfo['fName'] = result[i][1]
            likeInfo['lName'] = result[i][2]
            likeInfo['dateAdded'] = str(result[i][3])
            out.append(likeInfo)

        return out


    # getArticleLikesInfo: get user info for each user who likes specified article
    def getArticleLikesInfo(self, articleID):
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID, u.fName, u.lName, aa.dateAdded FROM ArticleActivities AS aa JOIN Users AS u ON aa.userID = u.userID WHERE aa.activityType='Like' AND aa.articleID=%s"
            cursor.execute(sql,(articleID))
            result = cursor.fetchall()

        out = []
        for i in range(len(result)):
            likeInfo = {}
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            likeInfo['sessionID'] = sessionID
            likeInfo['fName'] = result[i][1]
            likeInfo['lName'] = result[i][2]
            likeInfo['dateAdded'] = str(result[i][3])
            out.append(likeInfo)

        return out


    ## BEGIN ARTICLE LOOKS

    # getArticleLooksInfo: get user info for each user who likes specified article
    def getArticleLooksInfo(self, sessionID):
        users = []
        lookFeed = []
        # get list of users followed by logged in user\
        users = self.followedByUserIDs(sessionID)
        # get user activities for each of ^^ users
        for sessionID in users:
            userActivity = {}
            userInfo = self.getUserData(sessionID)
            articleActivities = self.getUserArticleActivities(sessionID)
            commentActivities = self.getUserCommentActivities(sessionID)
            for activity in articleActivities:
                userActivity['sessionID'] = sessionID
                userActivity['fName'] = userInfo['fName']
                userActivity['lName'] = userInfo['lName']
                userActivity['profilePic'] = "THIS WILL BE PROFILE PIC URL"
                userActivity['activityType'] = activity['activityType']
                userActivity['articleInfo'] = activity['articleInfo']
                userActivity['dateAdded'] = activity['dateAdded']
                if userActivity not in lookFeed:
                    lookFeed.append(userActivity)

            userActivity = {}
            for activity in commentActivities:
                userActivity['sessionID'] = sessionID
                userActivity['fName'] = userInfo['fName']
                userActivity['lName'] = userInfo['lName']
                userActivity['profilePic'] = "THIS WILL BE PROFILE PIC URL"
                userActivity['activityType'] = 'Comment'
                userActivity['commentID'] = activity['commentID']
                userActivity['content'] = activity['content']
                userActivity['dateAdded'] = activity['dateAdded']
                userActivity['articleInfo'] = activity['articleInfo']
                if userActivity not in lookFeed:
                    lookFeed.append(userActivity)

        return lookFeed
        # return X number of most recent activities
        # ^^ still need this

        ## END ARTICLE LOOKS



    # getArticleSharesIDs: get userID for each user who shared specified article
    def getArticleSharesIDs(self, articleID):
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID FROM ArticleActivities AS aa JOIN Users AS u ON aa.userID = u.userID WHERE aa.activityType='Share' AND aa.articleID=%s"
            cursor.execute(sql,(articleID))
            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            out.append(sessionID)
        return out


    # getArticleSharesInfo: get user info for each user who shared specified article
    def getArticleSharesInfo(self, articleID):
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID, u.fName, u.lName, aa.dateAdded FROM ArticleActivities AS aa JOIN Users AS u ON aa.userID = u.userID WHERE aa.activityType='Share' AND aa.articleID=%s ORDER BY aa.dateAdded ASC"
            cursor.execute(sql,(articleID))
            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            shareInfo = {}
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            shareInfo['sessionID'] = sessionID
            shareInfo['fName'] = result[i][1]
            shareInfo['lName'] = result[i][2]
            shareInfo['dateAdded'] = str(result[i][3])
            out.append(shareInfo)

        return out

    # getArticleComments: get commenter (user) info and comment info for each comment made on a specified article
    def getArticleComments(self, articleID):
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID, u.fName, u.lName, c.commentID, c.content, c.dateAdded FROM Comments AS c JOIN Users AS u ON c.userID = u.userID WHERE c.articleID=%s ORDER BY c.dateAdded ASC"
            cursor.execute(sql,(articleID))
            result = cursor.fetchall()

        out = []
        for i in range(len(result)):
            commentInfo = {}
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            commentInfo['sessionID'] = sessionID
            commentInfo['fName'] = result[i][1]
            commentInfo['lName'] = result[i][2]
            commentInfo['commentID'] = result[i][3]
            commentInfo['content'] = result[i][4]
            commentInfo['dateAdded'] = str(result[i][5])

            out.append(commentInfo)

        return out


    # getUserArticleActivities(): get list of article activites (likes/shares) for specified user
    def getUserArticleActivities(self, sessionID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "SELECT aa.articleID, aa.activityType, aa.dateAdded FROM ArticleActivities aa JOIN Articles a ON aa.articleID = a.articleID WHERE userID=%s ORDER BY aa.dateAdded ASC"
            cursor.execute(sql, (userID))
            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            articleActivity = {}
            articleID = result[i][0]
            articleInfo = self.getArticleInfo(sessionID, articleID)
            articleActivity['articleInfo'] = articleInfo
            articleActivity['activityType'] = result[i][1]
            articleActivity['dateAdded'] = str(result[i][2])

            out.append(articleActivity)

        return out

    # getUserCommentActivities: get list of article comments for specified user
    def getUserCommentActivities(self, sessionID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "SELECT c.commentID, a.articleID, c.content, c.dateAdded FROM Comments c JOIN Articles a ON c.articleID = a.articleID WHERE userID=%s ORDER BY c.dateAdded ASC"
            cursor.execute(sql, (userID))

            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            commentActivity = {}
            commentActivity['commentID'] = result[i][0]
            articleID = result[i][1]
            articleInfo = self.getArticleInfo(sessionID, articleID)
            commentActivity['articleInfo'] = articleInfo
            commentActivity['content'] = result[i][2]
            commentActivity['dateAdded'] = str(result[i][3])
            out.append(commentActivity)

        return out

    # addArticleLike: add article like for specified user
    def addArticleLike(self, sessionID, articleID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            activityType = 'Like'
            ts = time.gmtime()
            dateAdded = time.strftime("%Y-%m-%d %H:%M:%S", ts)
            sql = "INSERT INTO ArticleActivities(userID, articleID, activityType, dateAdded) VALUES(%s,%s,%s,%s)"
            cursor.execute(sql,(userID, articleID, activityType, dateAdded))
        self.connection.commit()

    # deleteArticleLike: delelte article like from specified user
    def deleteArticleLike(self, sessionID, articleID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM ArticleActivities WHERE activityType='Like' AND userID=%s AND articleID=%s"
            cursor.execute(sql, (userID, articleID))

        self.connection.commit()

    # addArticleShare: add article share for specified user
    def addArticleShare(self, sessionID, articleID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            activityType = 'Share'
            ts = time.gmtime()
            dateAdded = time.strftime("%Y-%m-%d %H:%M:%S", ts)
            sql = "INSERT INTO ArticleActivities(userID, articleID, activityType, dateAdded) VALUES(%s,%s,%s,%s)"
            cursor.execute(sql, (userID, articleID, activityType, dateAdded))

        self.connection.commit()

    # deleteArticleShare: delete article share for specified user
    def deleteArticleShare(self, sessionID, articleID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM ArticleActivities WHERE activityType='Share' AND userID=%s AND articleID=%s"
            cursor.execute(sql, (userID, articleID))

        self.connection.commit()

    # addArticleComment: add article comment from specified user s
    def addArticleComment(self, sessionID, articleID, content):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            ts = time.gmtime()
            dateAdded = time.strftime("%Y-%m-%d %H:%M:%S", ts)
            sql = "INSERT INTO Comments(userID, articleID, content, dateAdded) VALUES(%s,%s,%s,%s)"
            cursor.execute(sql,(userID, articleID, content, dateAdded))

        self.connection.commit()


    # deleteArticleComment
    def deleteArticleComment(self, sessionID, commentID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM Comments WHERE commentID=%s AND userID=%s"
            cursor.execute(sql, (commentID,userID))

        self.connection.commit()

###### END ARTICLE/OP-ED FUNCTIONS


###### BEGIN COMMENT FUNCTIONS

    #getCommentLikes: get sessionIDs of all users who liked a comment
    def getCommentLikes(self, commentID):
        with self.connection.cursor() as cursor:
            sql = "SELECT userID FROM CommentActivities WHERE activityType='Like' AND commentID=%s"
            cursor.execute(sql,(commentID))
            result = cursor.fetchall()

        out = []
        for i in range(len(result)):
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            out.append(sessionID)
        return out

    # getCommentShares: get sessionIDs of all users who shared an article
    def getCommentShares(self, commentID):
        with self.connection.cursor() as cursor:
            sql = "SELECT userID FROM CommentActivities WHERE activityType='Share' AND commentID=%s"
            cursor.execute(sql,(commentID))
            result = cursor.fetchall()

        out = []
        for i in range(len(result)):
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            out.append(sessionID)
        return out


    # addCommentLike: add a like to a comment from a specified user
    def addCommentLike(self, sessionID, commentID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            activityType = 'Like'
            ts = time.gmtime()
            dateAdded = time.strftime("%Y-%m-%d %H:%M:%S", ts)
            sql = "INSERT INTO CommentActivities(userID, commentID, activityType, dateAdded) VALUES(%s,%s,%s,%s)"
            cursor.execute(sql,(userID, commentID, activityType, dateAdded))

        self.connection.commit()

### DEPRECATED ###
    # # addCommentShare:
    # def addCommentShare(self, sessionID, commentID):
    #     userID = self.getUserID(sessionID)
    #     with self.connection.cursor() as cursor:
    #         activityType = 'Share'
    #         ts = time.gmtime()
    #         dateAdded = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    #         sql = "INSERT INTO CommentActivities(userID, commentID, activityType, dateAdded) VALUES(%s,%s,%s,%s)"
    #         cursor.execute(sql,(userID, commentID, activityType, dateAdded))
    #
    #     self.connection.commit()
### ^^^ DEPRECATED ###

    # deleteCommentLike: delete a comment like from a specified user
    def deleteCommentLike(self, sessionID, commentID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM CommentActivities WHERE activityType='Like' AND userID=%s AND commentID=%s"
            cursor.execute(sql, (userID, commentID))

        self.connection.commit()

### DEPRECATED ###
    # # deleteCommentShare
    # def deleteCommentShare(self, sessionID, commentID):
    #     userID = self.getUserID(sessionID)
    #     with self.connection.cursor() as cursor:
    #         sql = "DELETE FROM CommentActivities WHERE activityType='Share' AND userID=%s AND commentID=%s"
    #         cursor.execute(sql, (userID, commentID))
    #
    #     self.connection.commit()
### ^^^ DEPRECATED ###

##### END COMMENT FUNCTIONS ####

#### BEGIN USER CONNECTION FUNCTIONS

    # followUser: add a connection between to users
    def followUser(self, followedBySessionID, toFollowSessionID):
        followedByID = self.getUserID(followedBySessionID)
        toFollowID = self.getUserID(toFollowSessionID)
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO Connections(follower, following) VALUES(%s, %s)"
            cursor.execute(sql,(followedByID, toFollowID))
        self.connection.commit()


    # unfollowUser: remove a connection between two users
    def unfollowUser(self, unfollowedBySessionID, toUnfollowSessionID):
        unfollowedByID = self.getUserID(unfollowedBySessionID)
        toUnfollowID = self.getUserID(toUnfollowSessionID)
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM Connections WHERE follower=%s AND following=%s"
            cursor.execute(sql,(unfollowedByID, toUnfollowID))
        self.connection.commit()

    # followingUserIDs: get list of sessionIDs of users following a specified user
    def followingUserIDs(self, sessionID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID FROM Connections c JOIN Users u ON c.follower = u.userID AND c.following=%s"
            cursor.execute(sql, (userID))
            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            out.append(sessionID)
        return out

    # followedByUserIDs: get list of sessionIDs of users followed by a specified user
    def followedByUserIDs(self, sessionID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID FROM Connections c JOIN Users u ON c.following = u.userID WHERE c.follower=%s"
            cursor.execute(sql, (userID))
            result = cursor.fetchall()
        out = []
        for i in range(len(result)):
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            out.append(sessionID)
        return out

    # listFollowingUser: get a list of user names and sessionIDs of users following a specified user
    def listFollowingUser(self, sessionID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID, u.fName, u.lName FROM Connections c JOIN Users u ON c.follower = u.userID AND c.following=%s"
            cursor.execute(sql, (userID))
            result = cursor.fetchall()

        out = []
        for i in range(len(result)):
            userInfo = {}
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            userInfo['sessionID'] = sessionID
            userInfo['fName'] = result[i][1]
            userInfo['lName'] = result[i][2]
            out.append(userInfo)
        return out

    # listFollowedByUser: get a list of user names and sessionIDs of users followed by a specified user
    def listFollowedByUser(self, sessionID):
        userID = self.getUserID(sessionID)
        with self.connection.cursor() as cursor:
            sql = "SELECT u.userID, u.fName, u.lName FROM Connections c JOIN Users u ON c.following = u.userID WHERE c.follower=%s"
            cursor.execute(sql, (userID))
            result = cursor.fetchall()

        out = []
        for i in range(len(result)):
            userInfo = {}
            userID = result[i][0]
            sessionID = self.getSessionID(userID)
            userInfo['sessionID'] = sessionID
            userInfo['fName'] = result[i][1]
            userInfo['lName'] = result[i][2]
            out.append(userInfo)
        return out

######## BEGIN REDUNDANCY CHECK FUNCTIONS

    # likedArticle: check if a specific user has already liked a specific article
    def likedArticle(self, sessionID, articleID):
        articleLikes = self.getArticleLikesIDs(articleID)
        if sessionID in articleLikes:
            result =  True
        else:
            result  = False
        return result

    # sharedArticle: check if a specific user has already shared a specific article
    def sharedArticle(self, sessionID, articleID):
        articleShares = self.getArticleSharesIDs(articleID)
        if sessionID in articleShares:
            result =  True
        else:
            result  = False
        return result

    # likedArticleComment: check if a specific user has already liked a specific comment
    def likedArticleComment(self, sessionID, commentID):
        commentLikes = self.getCommentLikes(commentID)
        if sessionID in commentLikes:
            result =  True
        else:
            result  = False
        return result

### DEPRECATED ###
    # # sharedArticleComment: check if a specific user has already liked a specific comment
    # def sharedArticleComment(self, sessionID, commentID):
    #     commentShares = self.getCommentShares(commentID)
    #     if sessionID in commentShares:
    #         result =  True
    #     else:
    #         result  = False
    #     return result
### ^^^ DEPRECATED ###

    # doesFollow: check if a specific user follows another user
    def doesFollow(self, followedBySessionID, toFollowSessionID):
        # toFollowID = self.getUserID(toFollowSessionID)
        currentFollowers = self.followingUserIDs(toFollowSessionID)
        if followedBySessionID in currentFollowers:
            result =  True
        else:
            result  = False
        return result

    # # isLoggedIn: check if a specific user is currently logged in
    # def isLoggedIn(self, sessionID):
    #     sessionIDs = self.getSessionIDs()
    #     if sessionID in loggedInUserIDs:
    #         result = True
    #     else:
    #         result = False
    #     return result


    # isRegistered: check if a specific firebase is currently registered in DBs
    def isRegistered(self, firebaseID):
        firebaseIDs = self.getFirebaseIDs()
        if firebaseID in firebaseIDs:
            result = True
        else:
            result = False
        return result


######## END REDUNDANCY CHECK FUNCTIONS
