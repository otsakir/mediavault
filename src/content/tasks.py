from time import sleep
from celery import shared_task
from content.fetcher.ytdl import fetch_yt


@shared_task()
def fetch_yt_task(url, bucket_id):
    print("now i'm supposed to fetch stuff from yt.")
    fetch_yt(url, bucket_id)
