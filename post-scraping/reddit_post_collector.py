import requests
import json
import csv
import time

def fetch_200_reddit_posts(subreddit="nba", target_count=200):
    """
    Fetches exactly 200 active post links, titles, and metrics from r/nba
    without requiring API credentials, exporting them directly to CSV and JSON.
    """
    print(f"Initializing collection of {target_count} posts from r/{subreddit}...")
    
    posts = []
    after = None
    headers = {
        # A generic User-Agent prevents Reddit from rate-limiting public requests
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    while len(posts) < target_count:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
        if after:
            url += f"&after={after}"
            
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                children = data.get("data", {}).get("children", [])
                
                if not children:
                    print("No more posts found.")
                    break
                    
                for child in children:
                    post_data = child.get("data", {})
                    # Build absolute URL from relative permalink
                    permalink = f"https://www.reddit.com{post_data.get('permalink')}"
                    title = post_data.get("title")
                    score = post_data.get("score")
                    num_comments = post_data.get("num_comments")
                    author = post_data.get("author")
                    
                    posts.append({
                        "index": len(posts) + 1,
                        "title": title,
                        "url": permalink,
                        "author": author,
                        "upvotes": score,
                        "comments": num_comments
                    })
                    
                    if len(posts) >= target_count:
                        break
                        
                after = data.get("data", {}).get("after")
                print(f"Collected {len(posts)} / {target_count} posts...")
                
                if not after:
                    break
                    
                # Polite rate-limiting delay between requests
                time.sleep(1.5)
            else:
                print(f"Failed to fetch data (HTTP Status {response.status_code}). Retrying...")
                time.sleep(3)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    csv_file = f"{subreddit.lower()}_200_posts.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["index", "title", "url", "author", "upvotes", "comments"])
        writer.writeheader()
        writer.writerows(posts)
        
    json_file = f"{subreddit.lower()}_200_posts.json"
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4)
        
    print(f"\nSuccess! Saved {len(posts)} posts to '{csv_file}' and '{json_file}'.")

if __name__ == "__main__":
    fetch_200_reddit_posts()