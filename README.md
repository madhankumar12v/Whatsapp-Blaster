Overview
This script automates sending WhatsApp messages (with optional attachments) to a list of phone numbers using WhatsApp Web and Selenium WebDriver.

Prerequisites
Python 3.7+ installed on your system.

Google Chrome browser installed.

ChromeDriver executable matching your Chrome browser version.

Required Python Packages
Make sure to install these Python packages:

ttkbootstrap

requests

pandas

openpyxl

selenium

Step-by-step Setup Guide
Step 1: Install Python packages
Open your terminal or command prompt and run:

bash
Copy
Edit
pip install ttkbootstrap requests pandas openpyxl selenium
Step 2: Install Google Chrome
Download and install Google Chrome from https://www.google.com/chrome/

Step 3: Check your Chrome version
Open Chrome and navigate to chrome://settings/help or click Help > About Google Chrome.

Note your Chrome version number (e.g., 114.0.5735.110).

Step 4: Download matching ChromeDriver
Visit https://chromedriver.chromium.org/downloads

Download the ChromeDriver version that exactly matches your Chrome browser version.

Extract and place the chromedriver.exe file in your project folder or a known directory.

Step 5: Verify ChromeDriver location in script
By default, the script looks for chromedriver.exe in the current project folder.

If not found, it looks in the fallback path:
C:\ProgramData\chocolatey\lib\chromedriver\tools\chromedriver.exe

You can modify these paths in the get_driver() function if your chromedriver.exe is elsewhere.

Step 6: Prepare your contacts file
Create a CSV or Excel file with a column named Phone.

Fill this column with phone numbers in international format without '+' or spaces.
Example: 919876543210 (for an Indian number)

Step 7: Prepare your message and optional attachment
Write the message text you want to send.

Prepare any attachment file (image, pdf, etc.) you want to send along with the message (optional).

Step 8: Run the script
Run your Python script (for example: python main.py).

When prompted, scan the QR code with your WhatsApp mobile app to log in.

The script will start sending messages automatically to all contacts in the file.

Important Notes
Do NOT run Chrome in headless mode, as file uploads won’t work.

Keep your WhatsApp Web session active during sending.

Use an appropriate delay (time.sleep) between messages to avoid rate limiting.

Ensure all contacts are valid WhatsApp users to avoid failures.

If your file path or attachment path contains spaces, provide the full absolute path or handle quotes properly.

Troubleshooting
If chromedriver.exe is not found, check your path or download it again.

ChromeDriver and Chrome versions must match exactly.

If WhatsApp Web UI changes, some element selectors (XPATH, CSS) may need updating.

Check internet connection stability.
