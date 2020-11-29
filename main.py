import os
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# driver = webdriver.Chrome('D:\\Program\\Environment\\WebDriver\\chromedriver.exe')
driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)


def signer():
    driver.maximize_window()
    driver.get('http://yqdj.zucc.edu.cn/feiyan_api/h5/html/daka/daka.html')

    driver.implicitly_wait(120)
    # driver.find_element_by_css_selector("#username").send_keys(31801136)
    # driver.find_element_by_css_selector("#password").send_keys('31421X')
    driver.find_element_by_css_selector("#username").send_keys(os.environ["SCHOOL_ID"])
    driver.find_element_by_css_selector("#password").send_keys(os.environ["PASSWORD"])
    driver.find_element_by_css_selector(".btn-submit").click()

    sign = '''
        document.querySelector("input[name=mqszd]").value = "校内 校内 校内";
        var question = document.querySelector(".question-ul").children;
        for (let i = 0; i < question.length; i++) {
            var el = question[i];
            if (el.className == "card question-item required") {
                if (el.querySelector(".card-header").textContent.indexOf("是否") >= 0) {
                    el.querySelector('input[value^="否"]').click();
                }
                if (el.querySelector(".card-header").textContent.indexOf("颜色") >= 0) {
                    el.querySelector('input[value^="绿"]').click();
                }
            }
        }
        document.querySelector(".examen-box > div.content-block.submit-box > a").click()
    '''

    locator = (By.CSS_SELECTOR, ".examen-box > div")
    WebDriverWait(driver, 120, 0.5).until(EC.presence_of_all_elements_located(locator))
    isSigned = driver.execute_script(
        '''return document.querySelector(".examen-box > div.content-block.submit-box > a") == null''')

    if isSigned:
        print("今日已打卡")
    else:
        driver.execute_script(sign)
        print("打卡成功")


if __name__ == '__main__':
    signer()
    # driver.close()
