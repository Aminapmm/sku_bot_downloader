from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

HOME = os.path.dirname(__file__)

url = "https://sess.sku.ac.ir/sess/12901415214"
firefox_driver_path = os.path.join(HOME, "geckodriver")

s = Service(firefox_driver_path)
options = Options()
options.headless = False
driver = webdriver.Firefox(service=s, options=options)
driver.get(url)
driver.maximize_window()


def login(driver, USERNAME, PASSWORD):
    username_field = driver.find_element(By.NAME, 'edId')
    password_field = driver.find_element(By.ID, "edPass")
    login_btn = driver.find_element(By.ID, "edEnter")
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    login_btn.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "edflname")))
    assert "امين احمدپورمعرفي" == driver.find_element(By.ID, "edflname").text


def classroom_affairs(driver, subject):
    # ورود به امورکلاسی درس
    form_ = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bg-aqua .inner")))
    form_.click()
    semester_check_list = driver.find_elements(By.CSS_SELECTOR, '#edMiddle td:nth-child(3)')
    titles = {l.text: l for l in semester_check_list}
    ActionChains(driver).move_to_element(titles[subject]).click().perform()
    driver.implicitly_wait(3)
    course_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "edCourseName"))).text


def download_files(driver):
    files = driver.find_elements(By.CSS_SELECTOR, "#edListFolders .link")
    if not files:
        return "فایلی برای این درس وجود ندارد."
    for f in files:
        f.click()


def next_page(driver):
    driver.execute_script("window.scrollTo(1070, 759)")
    nextpage_elem = driver.find_element(By.CLASS_NAME, 'NextPage')
    ActionChains(driver).move_to_element(nextpage_elem).click().perform()


if __name__ == '__main__':
    USERNAME = input("شماره دانشجویی را وارد کنید:")  # Student number
    PASSWORD = input("رمز عبور را وارد کنید:")  # Password
    title = "فارسي عمومي"  # Resources to be downloaded
    login(driver, USERNAME, PASSWORD)
    driver.implicitly_wait(3)
    classroom_affairs(driver, title)
    download_files(driver)
