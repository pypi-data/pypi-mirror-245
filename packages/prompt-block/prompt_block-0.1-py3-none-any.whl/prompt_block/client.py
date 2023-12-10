import requests

class Client:
    def __init__(self, key):
        self.key = key
        self.base_url = "https://prompt-block.onrender.com/api/prompt-by-name"

    def get_content(self, name):
        url = f"{self.base_url}?name={name}&key={self.key}"
        headers = {"Authorization": f"Bearer {self.key}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get content: {response.status_code}")

