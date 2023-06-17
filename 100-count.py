#!/usr/bin/python3
"""Counts it."""
import requests


def count_words(subreddit, word_list, after="", count={}):
    """
    Returns a list containing the titles of all hot articles for a
    given subreddit. If no results are found for the given subreddit,
    the function should return None.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"limit": "100", "after": after}
    response = requests.get(url, headers=headers,
                            params=params, allow_redirects=False)
    if response.status_code != 200:
        return None
    data = response.json().get("data")
    if not data:
        return None
    children = data.get("children")
    if not children:
        return None
    for child in children:
        title = child.get("data").get("title")
        if not title:
            continue
        words = title.lower().split()
        for word in words:
            word = word.rstrip('.,?!_')
            if word in word_list:
                count[word] = count.get(word, 0) + 1
    after = data.get("after")
    if not after:
        sorted_count = sorted(count.items(), key=lambda x: (-x[1], x[0]))
        for word, cnt in sorted_count:
            print("{}: {}".format(word, cnt))
        return
    count_words(subreddit, word_list, after, count)
