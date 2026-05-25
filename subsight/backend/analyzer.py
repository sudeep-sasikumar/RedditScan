from __future__ import annotations
import re
from collections import Counter

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "it", "its", "i", "my", "we", "our", "you", "your",
    "they", "their", "this", "that", "be", "are", "was", "were", "have",
    "has", "had", "do", "did", "not", "no", "just", "get", "got", "so",
    "up", "out", "if", "as", "by", "from", "about", "what", "how", "when",
    "who", "why", "would", "could", "should", "will", "can", "dont", "ive",
    "im", "its", "like", "really", "also", "even", "still", "much", "more",
    "ve", "re", "ll", "s", "t", "d", "m",
}


def extract_keywords(posts: list[dict]) -> list[dict]:
    counter: Counter = Counter()
    for post in posts:
        text = f"{post.get('title', '')} {post.get('selftext', '')}"
        words = re.split(r"[\s\W]+", text.lower())
        for word in words:
            if len(word) >= 4 and word.isalpha() and word not in STOP_WORDS:
                counter[word] += 1
    return [{"word": w, "count": c} for w, c in counter.most_common(20)]


def build_subreddit_summary(posts: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for post in posts:
        name = post["subreddit"]
        groups.setdefault(name, []).append(post)

    summaries = []
    for name, group in groups.items():
        avg_score = round(sum(p["score"] for p in group) / len(group), 1)
        top_post = max(group, key=lambda p: p["score"])
        summaries.append({
            "name": name,
            "post_count": len(group),
            "avg_score": avg_score,
            "top_post_title": top_post["title"],
        })

    summaries.sort(key=lambda s: s["post_count"], reverse=True)
    return summaries


def get_high_signal_posts(posts: list[dict], min_score: int = 50) -> list[dict]:
    filtered = [p for p in posts if p["score"] >= min_score]
    filtered.sort(key=lambda p: p["score"], reverse=True)
    return filtered[:20]


def analyze(posts: list[dict]) -> dict:
    return {
        "total_posts": len(posts),
        "subreddit_breakdown": build_subreddit_summary(posts),
        "top_keywords": extract_keywords(posts),
        "high_signal_posts": get_high_signal_posts(posts),
        "all_posts": posts,
    }
