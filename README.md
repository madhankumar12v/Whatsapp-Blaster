# WhatsApp Blaster

## Overview
This script automates sending WhatsApp messages (with optional attachments) to a list of phone numbers using WhatsApp Web and Selenium WebDriver.

---

## Prerequisites

1. **Python 3.7+** installed on your system.

2. **Google Chrome browser** installed.

3. **ChromeDriver** executable matching your Chrome browser version.

---

## Required Python Packages

Make sure to install these Python packages:

- `ttkbootstrap`
- `requests`
- `pandas`
- `openpyxl`
- `selenium`

---

## Step-by-step Setup Guide

### Step 1: Install Python packages

Open your terminal or command prompt and run:

```bash
pip install ttkbootstrap requests pandas openpyxl selenium

# WhatsApp Blaster Setup Guide

## Step 2: Install Google Chrome

Download and install Google Chrome from:  
[https://www.google.com/chrome/](https://www.google.com/chrome/)

---

## Step 3: Check your Chrome version

- Open Chrome and go to `chrome://settings/help` or click **Help > About Google Chrome**.
- Note your Chrome version (e.g., `114.0.5735.110`).

---

## Step 4: Download matching ChromeDriver

- Visit [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
- Download the ChromeDriver version that matches your Chrome browser exactly.
- Extract and place `chromedriver.exe` in your project folder or a known directory.

---

## Step 5: Verify ChromeDriver location in the script

- By default, the script looks for `chromedriver.exe` in the current project folder.
- If not found, it tries the fallback path:  
  `C:\ProgramData\chocolatey\lib\chromedriver\tools\chromedriver.exe`
- You can change these paths inside the `get_driver()` function if needed.

---

## Step 6: Prepare your contacts file

- Create a CSV or Excel file with a column named **Phone**.
- Fill the **Phone** column with numbers in international format without the `+` sign or spaces.  
  Example: `919876543210`

---

## Step 7: Prepare your message and optional attachment

- Write the message text you want to send.
- Prepare any attachment file (image, PDF, etc.) if you want to send one (optional).

---

## Step 8: Run the script

- Run the Python script, e.g.,  
  ```bash
  python main.py
## Important Notes

- Do **NOT** use headless mode in Chrome, as it breaks file uploads.
- Keep your WhatsApp Web session active during sending.
- Use delays (e.g., `time.sleep(5)`) between sends to avoid getting blocked or banned.
- Ensure contacts are valid WhatsApp users.
- Use absolute file paths if your file paths contain spaces.

---

## Troubleshooting

- `chromedriver.exe` not found?  
  Check the path specified in the script or redownload the matching ChromeDriver version.
- ChromeDriver and Chrome browser versions **must match exactly**.
- If WhatsApp Web updates its interface, you may need to update the element selectors in the script.
- Check your internet connection for stability.
