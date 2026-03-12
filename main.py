import os
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Render server is live!"}

@app.get("/download")
def download_test():
    url = "https://www.w3.org/TR/PNG/iso_8859-1.txt"
    response = requests.get(url)
    with open("downloaded_file.txt", "wb") as f:
        f.write(response.content)
    return {"message": "Success!", "bytes": len(response.content)}

# No need for an 'if __name__ == "__main__"' block if using the command below
