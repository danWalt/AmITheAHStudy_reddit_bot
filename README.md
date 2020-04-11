# AmITheAH_Study.py

AmITheAH_Study project is a code + sql project I wrote with a purposes to
find out if there's a NTA (not the asshole) bias in Reddit's "AmITheAsshole" 
subreddit.
When learning how to create a reddit bot using praw I've created a bot that
 commented
on 5 posts ESH (everyone sucks here) in a matter of a few minutes I've
received my fair share of down votes and angry comments.
I have then thought that there might be a NTA bias and decided to check
this out.
My plan was to comment 8 new comments (iterate between NTA, ESH, YTA and NAH) 
every hour (using a scheduler) and calculate the average comment score after a
few weeks.
All of the comments and scores are stored in a MySQL table using pymysql.

Unfortunately, before I was able to get any serious results I was banned.
  

## Installation

You'll need to install a few packages in order for this to run:
pymysql
praw (I've followed this guide originally: https://www.pythonforengineers.com/build-a-reddit-bot-part-1/)
have a working MySQL environment


## Usage

Current usage is straightforward. 
In the future I would like to change this parts of the code:
- ability to easily change the subreddit, comments
- Code will create a new DB and table the first time it's used instead of
 having this manually created in advance
- Maybe switch the current table to NoSQL format as the current table is
 answering one specific answer
- Breakdown the current MySQL table structures to make it more flexible to
 answer future questions 