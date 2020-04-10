import praw
import pymysql.cursors
import AmITheAH_Study_Settings

# create reddit instance
reddit = praw.Reddit('bot2')

# connect to mysql
connection = pymysql.connect(host='localhost',
                             user='root',
                             port=3306,
                             password=AmITheAH_Study_Settings.pwd,
                             db='amitheasshole',
                             autocommit=True)
try:
    with connection.cursor() as cursor:
        query = 'SELECT * FROM COMMENTS'
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            comment = reddit.submission(id=row[3])
            score = comment.score
            update = """UPDATE comments SET score = %s where comment_id = %s"""
            to_db = (score, comment)
            cursor.execute(update, to_db)
finally:
    connection.close()
