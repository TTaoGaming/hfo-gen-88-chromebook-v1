# Medallion: Bronze | Mutation: 0% | HIVE: I
import os
import requests

def load_env():
    env_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

def search_tavily(query, api_key):
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced"
    }
    response = requests.post(url, json=payload)
    return response.json()

def main():
    load_env()
    tavily_key = os.getenv("TAVILY_API_KEY")
    query = "Context7 AI agent coding search"
    print(f"Searching Tavily for: {query}")
    results = search_tavily(query, tavily_key)
    for result in results.get('results', []):
        print(f"Title: {result['title']}\nURL: {result['url']}\nSnippet: {result['content']}\n")

if __name__ == "__main__":
    main()
