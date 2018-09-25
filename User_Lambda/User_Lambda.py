import pymysql
import json
import sys
import user_db as d
import populate_db
import create_tables


def lambda_handler(event, context):

    db = d.user_db()

    resourcePath = event["resourcePath"]
    httpMethod = event["httpMethod"]
    result = {}
    # resourcePath = '/test'
    # httpMethod = 'GET'

    if resourcePath == "/client/populate":
        if httpMethod == "GET":
            result['status'] = "Success"
            populate_db.populate()
        else:
            result['status'] = "FAILED"
        return result

    elif resourcePath =="/test":
        print(db.getSessionIDs())
        print(db.getFirebaseIDs())

    elif resourcePath == "/client/create":
        if httpMethod == "GET":
            result['status'] = "Success"
            create_tables.create()
        else:
            result['status'] = "FAILED"
        return result

    elif resourcePath == "/client/search-func":
        if httpMethod == "POST":
            keywords = event['body']['params']['keywords']
            result['status'] = "Success"
            result['body'] = db.search(keywords)
        else:
            result['status'] = "FAILED"

        return result


    #Resource Path: /client/users/login
    elif resourcePath == "/client/users/login":
        if httpMethod == "POST":
            firebaseID = event['body']['params']["firebaseID"]
            # firebaseID = "asf24trgq5yq5y4q45c44w5v4"
            if db.getUser(firebaseID):
                result['status'] = "Success"
                result['body'] = db.loginUser(firebaseID)
            else:
                result['status'] = "Failure"
                errMsg = "FirebaseID not in use"
                result['body'] = errMsg

        elif httpMethod == "DELETE":
            firebaseID = event['body']['params']["firebaseID"]
            result['status'] = "Success"
            result['body'] = db.logoutUser(firebaseID)

        else:
            result['status'] = "FAILED"

        return result

    #Resource Path: /client/users/info
    elif resourcePath == "/client/users/info":
        if httpMethod == "GET":
            sessionID = event["query"]["sessionID"]
            if db.getUserData(sessionID):
                result['status'] = "Success"
                result['body'] = db.getUserData(sessionID)
                print(result)
            else:
                errMsg = "ERROR: User doesn't exist"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)

        elif httpMethod == "POST":
            firebaseID = event['body']['params']['firebaseID']
            email = event['body']['params']["email"]
            fName = event['body']['params']["fName"]
            lName = event['body']['params']["lName"]
            bio = event['body']['params']["bio"]
            if db.getUser(firebaseID):
                result['status'] = "Success"
                result['body'] = db.loginUser(firebaseID)

            else:
                result['status'] = "Success"
                result['body'] = db.addUser(firebaseID, email, fName, lName, bio)


        elif httpMethod == "PUT":
            sessionID = event['body']['params']["sessionID"]
            email = event['body']['params']["email"]
            fName = event['body']['params']["fName"]
            lName = event['body']['params']["lName"]
            bio = event['body']['params']["bio"]
            profilePic = event['body']['params']["profilePic"]

            if db.getUserData(sessionID):
                result['status'] = "Success"
                db.editUser(sessionID, email, fName, lName, bio, profilePic)
            else:
                errMsg = "ERROR: User to edit does not exist "
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)

        elif httpMethod == "DELETE":
            sessionID = event['body']['params']["sessionID"]
            if db.getUser(sessionID):
                result['status'] = "Success"
                db.deleteUser(sessionID)
            else:
                errMsg = "ERROR: User doesn't exist"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)
        else:
            errMsg = "ERROR: Improper HTTP request type"
            result['status'] = "Failure"
            result['body'] = json.dumps(errMsg)

        return result

    #Resource Path: /client/users/connections
    elif resourcePath == "/client/users/connections":
        if httpMethod == "GET":
            # get following AND followers
            sessionID = event["query"]["sessionID"]
            direction = event["query"]["direction"]
            if direction == "following":
                result['status'] = "Success"
                result['body'] = db.listFollowingUser(sessionID)
            elif direction == "followedBy":
                result['status'] = "Success"
                result['body'] = db.listFollowedByUser(sessionID)
            else:
                errMsg = "Error: Incorrect connection direction"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)

        elif httpMethod == "POST":
            # follow User
            followedBySessionID = event['body']['params']["followedBySessionID"]
            toFollowSessionID = event['body']['params']["toFollowSessionID"]
            if db.doesFollow(followedBySessionID, toFollowSessionID):
                errMsg = "ERROR: User already followers other user"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)
            else:
                result['status'] = "Success"
                db.followUser(followedBySessionID, toFollowSessionID)

        elif httpMethod == "DELETE":
            #unfollow User
            unfollowedBySessionID = event['body']['params']["unfollowedBySessionID"]
            toUnfollowSessionID = event['body']['params']["toUnfollowSessionID"]
            if db.doesFollow(unfollowedBySessionID, toUnfollowSessionID):
                result['status'] = "Success"
                db.unfollowUser(unfollowedBySessionID, toUnfollowSessionID)
            else:
                errMsg = "ERROR: User doesn't currently follow other user"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)
        else:
            errMsg = "ERROR: Improper HTTP request type"
            result['status'] = "Failure"
            result['body'] = json.dumps(errMsg)

        return result


    #Resource Path: /client/articles
    elif resourcePath == "/client/articles":
        if httpMethod == "GET":
            topic = str(event["query"]["topic"])
            sessionID = 0
            if (event["query"]["sessionID"]):
                sessionID = event["query"]["sessionID"]
            # numArticles = event["query"]["numArticles"]
            # direction = event["query"]["direction"]
            # articleID = event["query"]["articleID"]
            result['status'] = "Success"
            result['body'] = db.getArticleData(sessionID, topic)
        else:
            errMsg = "ERROR: Improper HTTP request type"
            result['status'] = "Failure"
            result['body'] = json.dumps(errMsg)

        return result


### DEPRECATED ###
    # #Resource Path: /client/articledata
    # elif resourcePath == "/client/articledata":
    #     if httpMethod == "GET":
    #         topic = event["query"]["topic"]
    #         # numArticles = event["query"]["numArticles"]
    #         # direction = event["query"]["direction"]
    #         # articleID = event["query"]["articleID"]
    #         result['status'] = "Success"
    #         result['body'] = db.getArticleData(topic)
    #     else:
    #         errMsg = "ERROR: Improper HTTP request type"
    #         result['status'] = "Failure"
    #         result['body'] = errMsg
    #
    #     return result
### ^^^ DEPRECATED ###


    #Resource Path: /client/articles/likes
    elif resourcePath == "/client/articles/likes":
        if httpMethod == "GET":
            # articleID = 6
            articleID = event["query"]["articleID"]
            result['status'] = "Success"
            result['body'] = db.getArticleLikesInfo(articleID)
            print(result)

        elif httpMethod == "POST":
            # sessionID = 41245
            # articleID = 6
            sessionID = event['body']['params']['sessionID']
            articleID = event['body']['params']['articleID']
            #if user already likes article s
            if db.likedArticle(sessionID, articleID):
                errMsg = "ERROR: User already liked"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)
            #if user does NOT already like article
            else:
                result['status'] = "Success"
                db.addArticleLike(sessionID,articleID)
            print(result)

        elif httpMethod == "DELETE":
            #result = "Recieved DELETE request from /client/articles/likes"
            sessionID = event['body']['params']["sessionID"]
            articleID = event['body']['params']["articleID"]
            if db.likedArticle(sessionID, articleID):
                result['status'] = "Success"
                db.deleteArticleLike(sessionID,articleID)
            else:
                errMsg = "ERROR: User doesn't currently like"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)

        else:
            result['status'] = "Failure"
            result['body'] = "ERROR: Improper HTTP request type"

        return result

    elif resourcePath == "/client/articles/looks":
        if httpMethod == "GET":
            sessionID = event["query"]["sessionID"]
            # sessionID = 'VPSLkLVJrhjwxUTX'

            result['status'] = "Success"
            result['body'] = db.getArticleLooksInfo(sessionID)
            print(result)

        return result


    #Resource Path: /client/articles/shares
    elif resourcePath == "/client/articles/shares":
        if httpMethod == "GET":
            #result = "Recieved GET request from /client/articles/shares"
            articleID = event["query"]["articleID"]
            result['status'] = "Success"
            result['body'] = db.getArticleSharesInfo(articleID)

        elif httpMethod == "POST":
            #result = "Recieved POST request from /client/articles/shares"
            sessionID = event['body']['params']['sessionID']
            articleID = event['body']['params']['articleID']
            if db.sharedArticle(sessionID, articleID):
                result['status'] = "Failure"
                result['body'] = "ERROR: User already shared"
            else:
                result['status'] = "Success"
                db.addArticleShare(sessionID,articleID)

        elif httpMethod == "DELETE":
            sessionID = event['body']['params']['sessionID']
            articleID = event['body']['params']['articleID']
            if db.sharedArticle(sessionID, articleID):
                result['status'] = "Success"
                db.deleteArticleShare(sessionID,articleID)

            else:
                errMsg = "ERROR: User doesn't currently share"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)
        else:
            errMsg = "ERROR: Improper HTTP request type"
            result['status'] = "Failure"
            result['body'] = json.dumps(errMsg)

        return result


    elif resourcePath == "/client/articles/comments":
        if httpMethod == "GET":
            articleID = event["query"]["articleID"]
            result['status'] = "Success"
            result['body'] = db.getArticleComments(articleID)

        elif httpMethod == "POST":
            sessionID = event['body']['params']["sessionID"]
            articleID = event['body']['params']["articleID"]
            content = event['body']['params']["content"]
            result['status'] = "Success"
            db.addArticleComment(sessionID,articleID, content)

        elif httpMethod == "DELETE":
            sessionID = event['body']['params']['sessionID']
            commentID = event['body']['params']["commentID"]
            result['status'] = "Success"
            db.deleteArticleComment(sessionID,commentID)

        else:
            errMsg = "ERROR: Improper HTTP request type"
            result['status'] = "Failure"
            result['body'] = json.dumps(errMsg)

        return result


#### BEGIN (NEW) COMMENT AND COMMENTCOMMENT FUNCTIONS

    #Resource Path: /client/articles/comments/likes
    elif resourcePath == "/client/articles/comments/likes":
        if httpMethod == "GET":
            commentID = event["query"]["commentID"]
            result['status'] = "Success"
            result['body'] = db.getCommentLikes(commentID)

        elif httpMethod == "POST":
            sessionID = event['body']['params']["sessionID"]
            commentID = event['body']['params']["commentID"]
            if db.likedArticleComment(sessionID, commentID):
                errMsg = "ERROR: User already liked comment"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)
            else:
                result['status'] = "Success"
                db.addCommentLike(sessionID, commentID)

        elif httpMethod == "DELETE":
            sessionID = event['body']['params']["sessionID"]
            commentID = event['body']['params']["commentID"]
            if db.likedArticleComment(sessionID, commentID):
                result['status'] = "Success"
                db.deleteCommentLike(sessionID, commentID)
            else:
                errMsg = "ERROR: User doesn't currently like comment"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)

        else:
            errMsg = "ERROR: Improper HTTP request type"
            result['status'] = "Failure"
            result['body'] = json.dumps(errMsg)

        return result


    #Resource Path: /client/articles/comments/shares
    elif resourcePath == "/client/articles/comments/shares":
        if httpMethod == "GET":
            commentID = event["query"]["commentID"]
            result['status'] = "Success"
            result['body'] = db.getCommentShares(commentID)

        elif httpMethod == "POST":
            sessionID = event['body']['params']["sessionID"]
            commentID = event['body']['params']["commentID"]
            if db.sharedArticleComment(sessionID, commentID):
                errMsg = "ERROR: User already shared comment"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)
            else:
                result['status'] = "Success"
                db.addCommentShare(sessionID, commentID)

        elif httpMethod == "DELETE":
            sessionID = event['body']['params']["sessionID"]
            commentID = event['body']['params']["commentID"]
            if db.sharedArticleComment(sessionID, commentID):
                result['status'] = "Success"
                db.deleteCommentShare(sessionID, commentID)

            else:
                errMsg = "ERROR: User doesn't currently share comment"
                result['status'] = "Failure"
                result['body'] = json.dumps(errMsg)
        else:
            errMsg = "ERROR: Improper HTTP request type"
            result['status'] = "Failure"
            result['body'] = json.dumps(errMsg)

        return result


    else:
        errMsg = "Unrecognized resource path"
        result['status'] = "Failure"
        result['body'] = json.dumps(errMsg)

        return result


# event = " "
# context = " "
# lambda_handler(event, context)
