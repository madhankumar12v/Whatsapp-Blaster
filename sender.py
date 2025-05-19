import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver():
    """Starts and returns a ChromeDriver instance with necessary options."""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--user-data-dir=chrome-data")

    # ❗️ DO NOT USE HEADLESS MODE (it breaks file uploads)
    # chrome_options.add_argument("--headless")

    project_path = os.path.abspath("chromedriver.exe")
    fallback_path = "C:\\ProgramData\\chocolatey\\lib\\chromedriver\\tools\\chromedriver.exe"
    chromedriver_path = project_path if os.path.exists(project_path) else fallback_path

    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError("❌ ChromeDriver not found in expected locations.")

    try:
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ ChromeDriver started successfully.")
        return driver
    except WebDriverException as e:
        print(f"❌ ChromeDriver error: {e}")
        raise

def load_contacts(file_path):
    """Loads phone numbers from a CSV or XLSX file and returns them as a list."""
    print(f"📄 Loading contacts from file: {file_path}")
    ext = file_path.split('.')[-1].lower()

    if ext == "csv":
        df = pd.read_csv(file_path)
    elif ext in ["xls", "xlsx"]:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .csv or .xlsx")

    if 'Phone' not in df.columns:
        raise ValueError("Contact file must contain a 'Phone' column")

    phones = df['Phone'].dropna().astype(str).tolist()
    print(f"✅ Loaded {len(phones)} contacts.")
    return phones

def send_message(driver, phone_number, message, attachment_path=None):
    """Sends a message and optionally an attachment to a specific number."""
    try:
        url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        driver.get(url)
        print(f"🌐 Opening chat with {phone_number}...")
        time.sleep(12)

        try:
            send_button = driver.find_element(By.XPATH, "//button[@aria-label='Send']")
            send_button.click()
            print(f"✅ Text message sent to {phone_number}")
        except Exception:
            print(f"⚠️ Send button not found for {phone_number}")

        # Send Attachment
        if attachment_path:
            attachment_path = os.path.abspath(attachment_path)
            if not os.path.exists(attachment_path):
                print(f"❌ Attachment file does not exist: {attachment_path}")
                return

            try:
                print(f"📎 Attaching file: {attachment_path}")
                wait = WebDriverWait(driver, 30)

                # Click the attach icon
                attach_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@title='Attach']")))
                attach_icon.click()
                time.sleep(1)

                # Upload the file
                file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
                file_input.send_keys(attachment_path)
                time.sleep(5)

                # Click the send button for attachment
                send_attach_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']")))
                send_attach_btn.click()
                print(f"📎 Attachment sent to {phone_number}")
            except Exception as e:
                print(f"❌ Error sending attachment to {phone_number}: {e}")

        time.sleep(2)

    except Exception as e:
        print(f"❌ Error sending to {phone_number}: {e}")

def start_whatsapp_blast(file_path, message, attachment_path=None):
    """Main controller for sending WhatsApp messages with optional attachments."""
    print("🚀 Starting WhatsApp Blaster...")

    phones = load_contacts(file_path)
    if not phones:
        print("❌ No valid contacts found!")
        return "Failed"

    driver = get_driver()
    print("🕒 Please scan the QR code in WhatsApp Web.")
    driver.get("https://web.whatsapp.com")
    time.sleep(25)

    status_dict = {}

    for i, phone in enumerate(phones, 1):
        print(f"📤 Sending to {phone} ({i}/{len(phones)})...")
        try:
            send_message(driver, phone, message, attachment_path)
            status_dict[phone] = "Success"
            print(f"✅ {i}/{len(phones)} complete")
        except Exception as e:
            print(f"❌ Error for {phone}: {e}")
            status_dict[phone] = "Failed"

    print("🎉 Blasting completed!")
    driver.quit()
    return status_dict

# Example call (Uncomment and modify as needed)
# start_whatsapp_blast("User_Data/user details.csv", "Hello from MRSA!", "User_Data/sample.jpg")
