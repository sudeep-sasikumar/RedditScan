from __future__ import annotations
from typing import Literal
from pydantic import BaseModel


class ContentFilters(BaseModel):
    sort: Literal["top", "hot", "new", "relevance"] = "top"
    time_filter: Literal["week", "month", "year", "all"] = "year"
    min_score: int = 5


class ResearchRequest(BaseModel):
    subreddits: list[str]
    search_queries: list[str]
    filters: ContentFilters = ContentFilters()
    research_label: str = ""


class RedditPost(BaseModel):
    id: str
    title: str
    selftext: str
    score: int
    num_comments: int
    url: str
    subreddit: str
    top_comments: list[str]


class KeywordFrequency(BaseModel):
    word: str
    count: int


class SubredditSummary(BaseModel):
    name: str
    post_count: int
    avg_score: float
    top_post_title: str


class AnalysisResult(BaseModel):
    total_posts: int
    subreddit_breakdown: list[SubredditSummary]
    top_keywords: list[KeywordFrequency]
    high_signal_posts: list[RedditPost]
    all_posts: list[RedditPost]
    collection_notes: list[str]


class ResearchResponse(BaseModel):
    label: str
    parameters: dict
    analysis: AnalysisResult
    status: str
