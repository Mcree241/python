import os
import requests
from urllib.parse import urlparse
from pathlib import Path

def download_image():
    # Step 1: Prompt user for image URL
    url = input("Enter the image URL: ").strip()
    print(f"[DEBUG] URL entered: {url}")  # Debug print
    
    # Step 2: Create directory if it doesn't exist
    save_dir = Path("Fetched_Images")
    save_dir.mkdir(exist_ok=True)
    print(f"[DEBUG] Save directory: {save_dir.resolve()}")  # Debug print
    
    try:
        # Step 3: Download image
        response = requests.get(url, stream=True, timeout=10)
        print(f"[DEBUG] HTTP status code: {response.status_code}")  # Debug print
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        # Step 4: Extract filename from URL or assign a default one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:  
            filename = "downloaded_image.jpg"
        filepath = save_dir / filename
        print(f"[DEBUG] File will be saved as: {filepath}")  # Debug print

        # Save the file in chunks (to handle large files)
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        
        print(f"✅ Image saved successfully as {filepath}")
    
    except requests.exceptions.MissingSchema:
        print("❌ Invalid URL. Please enter a valid image link.")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Try again later.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error occurred: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    download_image()
