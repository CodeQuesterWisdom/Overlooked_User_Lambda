
import pymysql
import json
import json
import time
import sys

def create():

    try:
        connection = pymysql.connect(host="overlooked-db.ctpilp2ahgud.us-west-1.rds.amazonaws.com",user="overlooked_db", passwd="overlooked", db="overlooked_db", charset='utf8')

    except:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

    populate_statements = []

    with connection.cursor() as cursor:
        # check for existing database
        sql = """DROP DATABASE IF EXISTS overlooked_db"""
        cursor.execute(sql)
        connection.commit()

        sql = """CREATE DATABASE overlooked_db"""
        cursor.execute(sql)
        connection.commit()

        sql = """USE overlooked_db"""
        cursor.execute(sql)
        connection.commit()


        #create master table
        sql = """CREATE TABLE Master(
            master_password VARCHAR(350)
            ) """
        cursor.execute(sql)
        connection.commit()

        #create employee table
        sql = """CREATE TABLE Employees(
            employeeID INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
            email VARCHAR(75) NOT NULL,
            password VARCHAR(100) NOT NULL
            ) """
        cursor.execute(sql)
        connection.commit()

        #create user table
        sql = """CREATE TABLE Users(
            userID INT(11) PRIMARY KEY  NOT NULL AUTO_INCREMENT,
            firebaseID VARCHAR(75) NOT NULL UNIQUE,
            email VARCHAR(75) NOT NULL,
            fName VARCHAR(1000) NOT NULL,
            lName VARCHAR(1000) NOT NULL,
            joinDate TIMESTAMP NOT NULL,
            bio VARCHAR (1000)  NOT NULL,
            profilePic VARCHAR(750)
        --     lastLogin TIMESTAMP NOT NULL,
        --     salt VARCHAR(100) NOT NULL,
        --     imageID INT (11) NOT NULL,
        -- 	   FOREIGN KEY fk1(imageID) references Images(imageID)
            ) """
        cursor.execute(sql)
        connection.commit()

        #create activeUsers table
        sql = """ CREATE TABLE ActiveUsers(
            activeID INT (11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
            firebaseID VARCHAR(75)   NOT NULL,
            sessionID VARCHAR(50)  NOT NULL,
            FOREIGN KEY fk1(firebaseID) REFERENCES Users(firebaseID)
            )"""
        cursor.execute(sql)
        connection.commit()

        #create topics table
        sql = """CREATE TABLE Topics(
            topicID INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
            topic VARCHAR(50) NOT NULL
            ) """
        cursor.execute(sql)
        connection.commit()

        #create articles table
        sql = """CREATE TABLE Articles(
            articleID INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
            source VARCHAR(75) NOT NULL,
            topicID INT(11) NOT NULL,
            articleURL VARCHAR(150) NOT NULL,
            imageURL VARCHAR(1000) ,
            author VARCHAR(65) ,
            title VARCHAR(150) ,
            description LONGTEXT ,
            dateAdded TIMESTAMP,
            FOREIGN KEY fk1(topicID) REFERENCES Topics(topicID)
            ) """
        cursor.execute(sql)
        connection.commit()

        #create comments table
        sql = """CREATE TABLE Comments(
            commentID INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
            userID INT(11) NOT NULL,
            articleID INT(11) NOT NULL,
            content LONGTEXT NOT NULL,
            dateAdded TIMESTAMP NOT NULL,
            FOREIGN KEY fk1(userID) REFERENCES Users(userID),
            FOREIGN KEY fk2(articleID) REFERENCES Articles(articleID)
            )"""
        cursor.execute(sql)
        connection.commit()

        #create articleActivities table
        sql = """CREATE TABLE ArticleActivities(
            activityID INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
            userID INT(11) NOT NULL,
            articleID INT(11) NOT NULL,
            activityType VARCHAR(50) NOT NULL,
            dateAdded TIMESTAMP NOT NULL,
            FOREIGN KEY fk1(userID) REFERENCES Users(userID),
            FOREIGN KEY fk2(articleID) REFERENCES Articles(articleID)
            ) """
        cursor.execute(sql)
        connection.commit()

        #create commentActivities table
        sql = """ CREATE TABLE CommentActivities(
            activityID INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
            userID INT(11) NOT NULL,
            commentID INT(11) NOT NULL,
            activityType VARCHAR(50) NOT NULL,
            dateAdded TIMESTAMP NOT NULL,
            FOREIGN KEY fk1(userID) REFERENCES Users(userID),
            FOREIGN KEY fk2(commentID) REFERENCES Comments(commentID)
            ) """
        cursor.execute(sql)
        connection.commit()

        #create connections table
        sql = """ CREATE TABLE Connections(
            followingID INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
            follower INT(11) NOT NULL,
            following INT(11) NOT NULL,
            FOREIGN KEY fk1(follower) REFERENCES Users(userID),
            FOREIGN KEY fk2(following) REFERENCES Users(userID)
            ) """
        cursor.execute(sql)
        connection.commit()

        connection.close()
