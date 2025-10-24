import pyautogui as pag
import time
import requests
import os
import subprocess
import sys

print("🚀 Avica ID Capture Script Started!")
print(f"Current working directory: {os.getcwd()}")
print(f"Python version: {sys.version}")

# Check if Avica installer exists
avica_installer = "Avica_setup.exe"
demo_mode = not os.path.exists(avica_installer)

if demo_mode:
    print("⚠️ Demo mode: No Avica installer found")
else:
    print(f"✅ Avica installer found ({os.path.getsize(avica_installer)} bytes)")

# Function to launch Avica
def launch_avica_and_wait():
    print("🚀 Launching Avica...")
    
    avica_paths = [
        r"C:\Program Files (x86)\Avica\Avica.exe",
        r"C:\Program Files\Avica\Avica.exe",
        r"C:\Users\Public\Desktop\Avica.exe"
    ]
    
    launched = False
    for path in avica_paths:
        if os.path.exists(path):
            try:
                print(f"📍 Found Avica at: {path}")
                subprocess.Popen([path])
                launched = True
                break
            except Exception as e:
                print(f"❌ Launch error: {e}")
    
    if not launched:
        try:
            subprocess.Popen('start "" "Avica"', shell=True)
            launched = True
        except:
            print("❌ Could not launch Avica")
    
    if launched:
        print("⏳ Waiting 15 seconds for Avica to load...")
        time.sleep(15)
    
    return launched

# Function to minimize other windows (simple approach)
def minimize_cmd_windows():
    try:
        print("🗄️ Attempting to minimize CMD windows...")
        # Use Alt+Tab to cycle through windows
        pag.keyDown('alt')
        pag.press('tab')
        pag.press('tab')  # Move away from CMD
        pag.keyUp('alt')
        time.sleep(2)
        
        # Try to click on Avica area (center of screen)
        screen_width, screen_height = pag.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        pag.click(center_x, center_y)
        time.sleep(2)
        
        print("✅ Window focus adjusted")
    except Exception as e:
        print(f"⚠️ Window management error: {e}")

# Function to take multiple screenshots
def capture_avica_screenshots():
    screenshots = []
    
    try:
        print("📸 Taking screenshots...")
        
        # Take screenshot 1: Immediate
        screenshot1 = pag.screenshot()
        filename1 = 'avica_screenshot_1.png'
        screenshot1.save(filename1)
        screenshots.append(filename1)
        print(f"✅ Screenshot 1 saved: {filename1}")
        
        # Try clicking in center to ensure Avica is focused
        screen_width, screen_height = pag.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        pag.click(center_x, center_y)
        time.sleep(3)
        
        # Take screenshot 2: After centering
        screenshot2 = pag.screenshot()
        filename2 = 'avica_screenshot_2.png'
        screenshot2.save(filename2)
        screenshots.append(filename2)
        print(f"✅ Screenshot 2 saved: {filename2}")
        
        # Crop center area for ID focus
        width, height = screenshot2.size
        left = width // 4
        top = height // 4
        right = 3 * width // 4
        bottom = 3 * height // 4
        
        cropped = screenshot2.crop((left, top, right, bottom))
        filename3 = 'avica_id_focus.png'
        cropped.save(filename3)
        screenshots.append(filename3)
        print(f"✅ Cropped ID focus saved: {filename3}")
        
        return screenshots
        
    except Exception as e:
        print(f"❌ Screenshot error: {e}")
        return screenshots

# Upload function
def upload_to_gofile(filename):
    print(f"📤 Uploading {filename}...")
    url = 'https://store1.gofile.io/uploadFile'
    
    try:
        if not os.path.exists(filename):
            return None
            
        with open(filename, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, timeout=60)
            result = response.json()
            
            if result['status'] == 'ok':
                link = result['data']['downloadPage']
                print(f"✅ {filename} → {link}")
                return link
            else:
                print(f"❌ Upload failed for {filename}")
                return None
                
    except Exception as e:
        print(f"❌ Upload error for {filename}: {e}")
        return None

# Main execution
print("\n" + "="*50)
print("🎯 STARTING AVICA ID CAPTURE SEQUENCE")
print("="*50)

# Initial setup wait
if demo_mode:
    print("⏳ Demo mode: Short wait (10s)")
    time.sleep(10)
else:
    print("⏳ Normal mode: System stabilization (20s)")
    time.sleep(20)

# Perform Avica installation clicks
if not demo_mode:
    print("\n🖱️ Performing Avica setup clicks...")
    
    setup_sequence = [
        (516, 405, 3, "Install button"),
        (496, 438, 3, "Later/Skip update"), 
        (249, 203, 3, "Allow remote access - Try 1"),
        (249, 203, 3, "Allow remote access - Try 2"),
        (249, 203, 3, "Allow remote access - Try 3"),
    ]
    
    for x, y, duration, desc in setup_sequence:
        print(f"🖱️ {desc} at ({x}, {y})")
        try:
            pag.click(x, y, duration=duration)
            print(f"✅ Clicked: {desc}")
        except Exception as e:
            print(f"❌ Click failed: {e}")
        
        time.sleep(8)  # Wait between clicks

# Launch Avica
print("\n🚀 Launching Avica application...")
if not demo_mode:
    launch_avica_and_wait()
else:
    print("⏳ Demo mode: Simulating Avica launch wait...")
    time.sleep(10)

# Final wait before screenshots
print("⏳ Final wait before capturing (10s)...")
time.sleep(10)

# Adjust window focus
minimize_cmd_windows()

# Capture screenshots
print("\n📸 Starting screenshot capture...")
screenshots = capture_avica_screenshots()

if screenshots:
    print(f"\n📤 Uploading {len(screenshots)} screenshots...")
    
    links = {}
    for filename in screenshots:
        link = upload_to_gofile(filename)
        if link:
            links[filename] = link
    
    # Write results
    if links:
        print("\n" + "="*60)
        print("🎉 AVICA SCREENSHOTS SUCCESSFULLY UPLOADED!")
        print("="*60)
        
        try:
            with open('show.bat', 'a') as f:
                f.write('\necho ================================\n')
                f.write('echo 🎯 AVICA REMOTE ID SCREENSHOTS\n')
                f.write('echo ================================\n')
                
                for filename, link in links.items():
                    f.write(f'echo 📱 {filename}: {link}\n')
                    print(f"📱 {filename}: {link}")
                
                f.write('echo ================================\n')
                f.write('echo Check above links for Avica ID!\n')
                f.write('echo ================================\n')
            
            print("✅ Links saved to show.bat")
            
        except Exception as e:
            print(f"❌ Error writing to show.bat: {e}")
        
        print("="*60)
    else:
        print("❌ No successful uploads")
else:
    print("❌ No screenshots captured")

print("\n✅ Avica ID capture script completed!")
print("🔍 Check the uploaded images for Avica Remote ID and Password")
