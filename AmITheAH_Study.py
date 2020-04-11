import praw
import os
import pymysql.cursors
import AmITheAH_Study_Settings
import getCommentScore


def get_posts_file():
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
    return posts_replied_to


# comments on at max 8 new posts from AMITHEASSHOLE subreddit
def commenting(reddit):
    # open posts replied to file
    posts_replied_to = get_posts_file()

    possible_answers = ['YTA', 'NTA', 'ESH', 'NAH']

    # load amitheashhole subreddit
    subreddit = reddit.subreddit('AmItheASSHOLE')
    # load 8 newest posts, if the are in the tracking txt file skips them else,
    # comments one of the possible answers
    i = 0
    for submission in subreddit.new(limit=8):
        if submission.id not in posts_replied_to:
            text = possible_answers[i % 4]
            comment = submission.reply(text)
            print("Bot replying to : ", submission.title)
            posts_replied_to.append([submission.id, text, comment.id])
            posts_replied_to = list(filter(None, posts_replied_to))
            i += 1
    return posts_replied_to


# insert each new comment to an SQL DB
def insert_to_db(posts_replied_to):
    # connect to DB
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 port=3306,
                                 password=AmITheAH_Study_Settings.pwd,
                                 db='amitheasshole',
                                 autocommit=True)
    try:
        with connection.cursor() as cursor:
            table_id = AmITheAH_Study_Settings.table_id
            for post_id in posts_replied_to:
                to_db = [table_id, post_id[0], post_id[1], post_id[2], 0]
                new_row = "INSERT INTO comments (id, post_id, " \
                          "comment, comment_id, score) VALUES (%s, %s, " \
                          "%s, %s, %s)"
                cursor.execute(new_row, to_db)
                table_id += 1

    finally:
        AmITheAH_Study_Settings.table_id = table_id
        connection.close()


def add_posts_to_txt(posts_replied_to):
    # writes the newly added posts we commented on to the txt file
    with open("AMITA_posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            for item in post_id:
                f.write(item)
            f.write('\n')


def main():
    # Create the Reddit instance
    reddit = praw.Reddit('bot2')
    # comment on new posts
    posts_replied_to = commenting(reddit)
    # inserting new comments to SQL DB
    insert_to_db(posts_replied_to)
    # add new posts commented on to txt file
    add_posts_to_txt(posts_replied_to)
    # update all comments score column
    getCommentScore.update_comment_score(reddit)


if __name__ == "__main__":
    main()
