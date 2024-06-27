from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from flask import Flask, jsonify

app = Flask(__name__)
app.json.sort_keys = False

def set_driver():
    try: 
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("--headless=new")
        # options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-infobars')  # Disable "Chrome is being controlled by automated test software" infobar
        options.add_argument('--disable-extensions')  # Disable extensions
        options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

        # Set up experimental options to remove the automation controlled flag
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('mobileEmulation', {
            'deviceName': 'iPhone XR'
        })

        # return webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        return webdriver.Chrome(options=options, service=Service(executable_path="./chromedriverlinux"))
    except Exception as e:
        print(f"Error SetDriver: {str(e)}")
        return None

@app.route("/")
def home():
    return jsonify(get_updated_manga_list())
    # if check_variable_type(driver, webdriver.Chrome):
    #     print("Getting url...")
    #     driver.get(url)
    #     return get_manga_list(set_driver())
    # else:
    #     return json.dumps({
    #         "status": "Failed",
    #         "message": "Variable is of the incorrect type."
    #     })

@app.route("/about")
def about():
    return jsonify({
        "Created by": "NikxPhreaker"
    })
    
def check_variable_type(variable: any, expected_type: type) -> bool:
    if not isinstance(variable, expected_type):
        print(f"Error: Expected {expected_type}, but got {type(variable)}")
        return False
    return True
    
def get_updated_manga_list():
    print("setting up driver...")
    driver: webdriver.Chrome = set_driver()
    try:
        print("getting updated manga list...")
        url = "http://mangaku.lat"
        driver.get(url)
        # Wait for an element to be present
        element = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="t1"]/div/div[1]/div[@class="utao"]')))
        # element = driver.find_element(By.XPATH, '//*[@id="t1"]/div/div[1]/div[2]')
        mangalist = []
        for i in element:
            manga_data = {
                "tittle": i.find_element(By.XPATH, "./div/div[2]/a").text,
                "img": i.find_element(By.XPATH, "./div/div[1]/img").get_attribute("data-src"),
                "rating": i.find_element(By.XPATH, "./div/div[2]/div/span/b").text,
                "last_chapter": i.find_element(By.XPATH, "./div/div[2]/ul/li[1]/a/button").text,
                "last_update": i.find_element(By.XPATH, "./div/div[2]/ul/li[3]/time").text,
                "link_chapter": i.find_element(By.XPATH, "./div/div[2]/ul/li[1]/a").get_attribute("href"),
                "link_list_chapter": i.find_element(By.XPATH, "./div/div[2]/ul/li[2]/a").get_attribute("href")
            }
            mangalist.append(manga_data)
        print("quit driver...")
        driver.close()
        driver.quit()
        return {
            "status": "Sucess",
            "mangalist": mangalist
        }
    except Exception as e:
        print("quit driver...")
        driver.close()
        driver.quit()
        return {
            "status": "Failed",
            "message": f"Error({str(e)})"
        }
    
    # Find the <body> element
    # body = driver.find_element(By.TAG_NAME, 'body')
    
    # Get entire page
    # source = driver.page_source
    # with open("html.html", "w", encoding="utf-8") as file:
    #     file.write(source)

if __name__ == '__main__':
    app.run()