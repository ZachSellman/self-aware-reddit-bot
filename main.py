"""Self Aware Reddit Bot is a python based bot that utilizes PRAW to search 
for comments being made mentioning Reddit. It then replies yes, ask me a 
simple question, and attempts to find an answer to said reply on r/ask reddit 
using the pushshift api."""

from os import getenv, environ
from datetime import datetime as dt
from dotenv import load_dotenv
import praw
import requests


load_dotenv()

# use this base for K8s to grab environ server url
# BASE = environ["SERVER_URL"]
# this is the default flask base url:
BASE = "http://127.0.0.1:5000/"
CLIENT_SECRET = getenv("CLIENT_SECRET")
USERNAME = getenv("NAME")
PASSWORD = getenv("PASSWORD")
CLIENT_ID = getenv("CLIENT_ID")
USER_AGENT = "meta_bot (by u/OmnicBoy)"

SEARCH_PARAM = "reddit"


# class Mention:
#     def __init__(self, submission_id, time_created, subreddit):
#         self.submission_id = submission_id
#         self.time_created = dt.fromtimestamp(time_created)
#         self.subreddit = subreddit

#     def __repr__(self):
#         return (
#             f"submission_id = {self.submission_id}, "
#             "time_created = {self.time_created}, subreddit = {self.sub_reddit}"
#         )


def main():
    live_comments_stream()


def live_comments_stream():
    """Live scans reddit comments being made and returns their comment id's"""
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME,
    )
    subreddit = reddit.subreddit("all")
    for submission in subreddit.stream.submissions():
        submission.comments.replace_more(limit=None)
        if (
            SEARCH_PARAM.lower() in submission.title.lower()
            or SEARCH_PARAM.lower() in submission.selftext.lower()
        ):
            print(f"Found one: {submission.id}")


# This is for sending files off to an api to be stored.
# def send(submission):
#     headers = {"Content_Type": "application/json"}

#     obj_dict = {
#         "submission_id": str(submission.id),
#         "post_date": str(dt.fromtimestamp(submission.created_utc)),
#         "subreddit": str(submission.subreddit.display_name),
#     }
#     response = requests.post(
#         BASE + "/mentions/all", headers=headers, json=obj_dict, timeout=2
#     )
#     print(response.json())


if __name__ == "__main__":
    main()
