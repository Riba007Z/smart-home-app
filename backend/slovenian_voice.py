"""from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


options = webdriver.ChromeOptions()

options.add_argument("--headless=new")
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")


driver = webdriver.Chrome(options=options)

driver.get(
    "https://slovenscina.eu/en/razpoznavalnik"
)


def get_text():

    mic = WebDriverWait(driver,20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/main/div[1]/div[1]/div[2]/button"
            )
        )
    )


    input("Press ENTER to start recording...")


    mic.click()

    print("🎤 Govori...")


    input("Press ENTER to stop recording...")


    mic.click()


    textarea = WebDriverWait(driver,30).until(
        EC.presence_of_element_located(
            (By.ID,"textarea")
        )
    )


    WebDriverWait(driver,30).until(
        lambda d:
        d.find_element(
            By.ID,
            "textarea"
        ).get_attribute("value").strip() != ""
    )


    text = driver.find_element(
        By.ID,
        "textarea"
    ).get_attribute("value").strip()


    print("🗣️ Prepoznano:",text)


    return text"""
    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

options.add_argument(
    "--use-fake-ui-for-media-stream"
)
options.add_argument(
    "--use-fake-device-for-media-stream"
)


driver = webdriver.Chrome(options=options)

driver.get(
    "https://slovenscina.eu/en/razpoznavalnik"
)


def get_text():

    mic = WebDriverWait(driver,20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/main/div[1]/div[1]/div[2]/button"
            )
        )
    )


    mic.click()

    print("🎤 Speak now")


    input("Press ENTER to stop...")


    mic.click()


    textarea = WebDriverWait(driver,30).until(
        EC.presence_of_element_located(
            (By.ID,"textarea")
        )
    )


    text = textarea.get_attribute(
        "value"
    )


    print("🗣", text)

    return text