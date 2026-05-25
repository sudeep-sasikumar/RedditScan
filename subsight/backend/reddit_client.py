from __future__ import annotations
import os
import praw
import prawcore.exceptions
from models import ContentFilters


def collect_posts(
    subreddits: list[str],
    search_queries: list[str],
    filters: ContentFilters,
) -> tuple[list[dict], list[str]]:
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        check_for_async=False,
    )

    seen_ids: set[str] = set()
    collected: list[dict] = []
    notes: list[str] = []

    for subreddit_name in subreddits:
        skip_subreddit = False
        for query in search_queries:
            if skip_subreddit:
                break
            try:
                sub = reddit.subreddit(subreddit_name)
                results = sub.search(
                    query,
                    sort=filters.sort,
                    time_filter=filters.time_filter,
                    limit=15,
                )
                for post in results:
                    if post.score < filters.min_score:
                        continue
                    if post.id in seen_ids:
                        continue
                    seen_ids.add(post.id)
                    post.comments.replace_more(limit=0)
                    top_comments = [
                        c.body[:300]
                        for c in post.comments.list()[:5]
                        if hasattr(c, "body")
                    ]
                    collected.append({
                        "id": post.id,
                        "title": post.title,
                        "selftext": post.selftext or "",
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "url": post.url,
                        "subreddit": subreddit_name,
                        "top_comments": top_comments,
                    })
            except prawcore.exceptions.NotFound:
                notes.append(f"Subreddit r/{subreddit_name} not found — skipped")
                skip_subreddit = True
            except prawcore.exceptions.Forbidden:
                notes.append(f"Subreddit r/{subreddit_name} is private — skipped")
                skip_subreddit = True
            except Exception as e:
                notes.append(
                    f"Warning on r/{subreddit_name} + '{query}': {str(e)[:100]}"
                )
                continue

    collected.sort(key=lambda p: p["score"], reverse=True)
    collected = collected[:150]
    return collected, notes
