import requests

url = "https://api.x.ai/v1/models"
headers = {
    "Authorization": "Bearer xai-UK0sdBfM7tZFzM8Sy4kdp96BC5lUGUrjii7Tc5HEkYrbv6eoOzqs6cx3Kb9kSEFpgn7iZK8TIxnVTdZo"
}

res = requests.get(url, headers=headers)

print("Status:", res.status_code)
print(res.json())