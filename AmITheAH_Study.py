import praw
import os
import pymysql.cursors
import AmITheAH_Study_Settings

# Create the Reddit instance
reddit = praw.Reddit('bot2')

# checking if a txt file following the posts that were already commented on
# created or not
if not os.path.isfile("AMITA_posts_replied_to.txt"):
    posts_replied_to = []
else:  # opens the already created txt file to make sure we're not double
    # commenting on a post
    with open("AMITA_posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))
possible_answers = ['YTA', 'NTA', 'ESH', 'NAH']
# load amitheashhole subreddit
subreddit = reddit.subreddit('AmItheASSHOLE')
# load 5 newest posts, if the are in the tracking txt file skips them else,
# comments "NTA"
i = 0
for submission in subreddit.new(limit=8):
    if submission.id not in posts_replied_to:
        text = possible_answers[i % 4]
        comment = submission.reply(text)
        print("Bot replying to : ", submission.title)
        posts_replied_to.append([submission.id, text, comment.id])
        posts_replied_to = list(filter(None, posts_replied_to))
        i += 1

# create DB
connection = pymysql.connect(host='localhost',
                             user='root',
                             port=3306,
                             password= AmITheAH_Study_Settings.pwd,
                             db='amitheasshole',
                             autocommit=True)
try:
    with connection.cursor() as cursor:
        query = 'SELECT id FROM COMMENTS ORDER BY id DESC ' \
                'LIMIT 1'
        table_id = int(cursor.execute(query))
        table_id = table_id + 1
        for post_id in posts_replied_to:
            to_db = [table_id, post_id[0], post_id[1], post_id[2], 0]
            new_row = "INSERT INTO comments (id, post_id, " \
                      "comment, comment_id, score) VALUES (%s, %s, " \
                      "%s, %s, %s)"
            cursor.execute(new_row, to_db)
            table_id += 1

finally:
    connection.close()

# writes the newly added posts we commented on to the txt file
with open("AMITA_posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        for item in post_id:
            f.write(item)
        f.write('\n')
