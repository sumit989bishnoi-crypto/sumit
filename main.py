from fastapi import FastAPI
import requests
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Server is running"}

@app.get("/download")
def download_test():
    # Example: Downloading a small text file from the internet
    url = "https://www.w3.org/TR/PNG/iso_8859-1.txt"
    response = requests.get(url)
    
    # Save it to the server's temporary storage
    with open("downloaded_file.txt", "wb") as f:
        f.write(response.content)
        
    return {"message": "File downloaded successfully!", "size": len(response.content)}
