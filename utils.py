import urllib3
import requests

def setup_session():
    session = requests.Session()
    retry = urllib3.Retry(
        respect_retry_after_header=False
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    return [session, retry, adapter]

def format_retry_after(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"