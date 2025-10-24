import pyautogui as pag
import time
import requests
import os
import sys

# Optional: You can add your GoFile API token here (or leave blank for anonymous upload)
GOFILE_API_TOKEN = ""  # Leave empty if you don't have one

# Wait for Avica setup to finish installing
time.sleep(40)

print("🚀 Starting Avica automation...")

# Define click actions (x, y, duration)
actions = [
    (516, 405, 4),  # Install
    (50, 100, 1),   # Tick launch Avica
    (496, 438, 4),  # Later Update
    (249, 203, 4),  # Allow RDP button
    (249, 203, 4),
    (249, 203, 4),
    (249, 203, 4),
    (447, 286, 4),  # Launch Avica & upload screenshot
]

# Screenshot file name
img_filename = "NewAvicaRemoteID.png"


def upload_image_to_gofile(img_filename):
    """Uploads the screenshot to GoFile.io using the 2025 API."""
    url = "https://api.gofile.io/contents/uploadfile"
    headers = {}

    if GOFILE_API_TOKEN.strip():
        headers = {"Authorization": f"Bearer {GOFILE_API_TOKEN}"}

    try:
        with open(img_filename, "rb") as img_file:
            files = {"file": img_file}
            print("📤 Uploading screenshot to GoFile.io ...")
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            result = response.json()

            print("🧾 GoFile Response:", result)

            if result.get("status") == "ok":
                download_page = result["data"]["downloadPage"]
                # Append to show.bat for GitHub Action display
                with open("show.bat", "a", encoding="utf-8") as bat_file:
                    bat_file.write(f'\necho Avica Remote ID : {download_page}\n')
                print(f"✅ Image uploaded successfully: {download_page}")
                return download_page
            else:
                print("❌ Upload error:", result)
                return None
    except Exception as e:
        print(f"⚠️ Failed to upload image: {e}")
        return None


# Perform the click sequence
time.sleep(10)

for x, y, duration in actions:
    pag.click(x, y, duration=duration)
    print(f"🖱️ Clicked at ({x}, {y}) with duration {duration}")
    time.sleep(2)

    # If the action corresponds to launching Avica and uploading
    if (x, y) == (447, 286):
        print("🖥️ Launching Avica and preparing screenshot...")
        try:
            os.system('"C:\\Program Files (x86)\\Avica\\Avica.exe"')
        except Exception as e:
            print(f"⚠️ Could not start Avica: {e}")

        time.sleep(10)
        pag.click(249, 203, duration=4)  # Attempt to click Allow again
        time.sleep(10)

        # Take screenshot and upload
        pag.screenshot().save(img_filename)
        print(f"📸 Screenshot saved as {img_filename}")

        gofile_link = upload_image_to_gofile(img_filename)
        if not gofile_link:
            print("❌ Failed to get GoFile link.")
        else:
            print(f"🔗 GoFile Link: {gofile_link}")

    time.sleep(10)

print("✅ Avica setup automation complete!")
