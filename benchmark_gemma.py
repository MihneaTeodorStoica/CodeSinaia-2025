import time
import requests

prompt = "Explain the theory of general relativity in simple terms."

data = {
    "model": "gemma3:1b",
    "messages": [{"role": "user", "content": prompt}],
    "stream": False
}

start = time.time()
response = requests.post("http://localhost:11434/api/chat", json=data)
end = time.time()

if response.ok:
    content = response.json()["message"]["content"]
    tokens = len(content.split())
    elapsed = end - start
    print(f"Response length: {tokens} tokens")
    print(f"Time taken: {elapsed:.2f} seconds")
    print(f"Tokens per second: {tokens / elapsed:.2f} t/s")
else:
    print(f"Error: {response.status_code}")
