import pymysql.cursors
import AmITheAH_Study_Settings

def update_comment_score(reddit):
    # connect to mysql
    connection = pymysql.connect(host='localhost',
                             user='root',
                             port=3306,
                             password=AmITheAH_Study_Settings.pwd,
                             db='amitheasshole',
                             autocommit=True)
    try:
        with connection.cursor() as cursor:
            user_comments = reddit.redditor(
                AmITheAH_Study_Settings.user_name).comments.new(limit=None)
            for comment in user_comments:
                score = comment.score
                comment_id = comment.id
                update = """UPDATE comments SET score = %s where comment_id = %s"""
                to_db = (score, comment_id)
                cursor.execute(update, to_db)
    finally:
        connection.close()
