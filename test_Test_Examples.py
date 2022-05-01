# Import modules
import time
import unittest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import HtmlTestRunner

# Class Method
class TestExamples(unittest.TestCase):


    # Statics
    @staticmethod
    def data():
        return driver.find_element(By.XPATH, '//*[@id="competitors-stat__filters"]/div/div[1]/div[4]/span/div/div[1]')

    # SetUp
    @classmethod
    def setUpClass(cls):

        # Global variables for tests
        global driver, BASE, PAGE

        BASE = 'https://hostsite.ru'
        PAGE = 'https://hostpage/page.ru'

        capabilities = {
            "browserName": "chrome",
            "browserVersion": "96.0",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False
            }
        }

        # Path To Drivers
        # Driver on Local machine
        s = Service("./drivers/chromedriver")
        driver = webdriver.Chrome(service=s)

        # Jenkins Server with capabilities
        driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities=capabilities)
        # Or Remote Driver
        WebDriver driver = new RemoteWebDriver(new URL("https://" + username + ":" + accesskey + "@hub.lambdatest.com/wd/hub"),
        
      
    # LogIn to Personal Profile
    @classmethod
    def LogIn(cls):
        
        # Get to site
        driver.get(BASE)
        driver.maximize_window()
        
        # Wait untill Login button us loaded
        WebDriverWait(driver, 360).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/login')]"))).click()
        
        # Set Login-Pass
        driver.find_element(By.NAME, "WorkLoginForm[login]").send_keys('LOGIN')
        driver.find_element(By.NAME, "WorkLoginForm[password]").send_keys('PASSWORD')
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        

    # Fast Filters Block (Period)
    # Example: 1) Click to sort buttons 2) Check URL parameters 3) If something wrong asserterror with Allure screenshot
    @classmethod
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story('Filter description 1')
    def test_1_Fast_Filters_Grown_Leaders(cls):
        
        driver.get(PAGE)

        # Wait untill Page is loaded
        WebDriverWait(driver, 360).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pagination-status")))

        driver.execute_script("arguments[0].click();", cls.data())

        period = driver.find_element(By.XPATH, '//button[contains(text(),"Месяц")]')
        driver.execute_script("arguments[0].click();", period)

        WebDriverWait(driver, 360).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pagination-status")))

        try:
            var = driver.find_element(By.XPATH, '//*[@id="competitors_stats_quick_filters"]/span[1]/span[1]/a')
            driver.execute_script("arguments[0].click();", var)

            assert 'text' in driver.current_url

        except (AssertionError, NoSuchElementException, TimeoutException):
            with open('log.txt', 'w') as file:
                assert False, file.write('Problem with filter 1!\n')
                allure.attach(driver.get_screenshot_as_png(), name="GrownLeaders",
                            attachment_type=AttachmentType.PNG)

    # Block Fast Filters (Day)
    # Check the same filters but for one day
    @classmethod
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story('Filter description 2')
    def test_2_Fast_Filters_Absolute_Leaders(cls):

        driver.execute_script("arguments[0].click();", cls.data())

        day = driver.find_element(By.XPATH, '//button[contains(text(),"День")]')
        driver.execute_script("arguments[0].click();", day)

        WebDriverWait(driver, 360).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pagination-status")))

        try:
            var2 = driver.find_element(By.XPATH,
                                                   '//*[@id="competitors_stats_quick_filters"]/span[1]/span[1]/a')
            driver.execute_script("arguments[0].click();", var2)

            assert 'text' in driver.current_url

        except (AssertionError, NoSuchElementException, TimeoutException):
            with open('log.txt', 'w') as file:
                assert False, file.write('Problem with filter 2!\n')
                allure.attach(driver.get_screenshot_as_png(), name="AbsoluteLeaders",
                            attachment_type=AttachmentType.PNG)


    # Block Table Metric Sorting
    # %TOP Metric
    # Sorting by ASC/DESC numbers
    @classmethod
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story('Check correct sorting %TOP')
    def test_3_Sorting_TOP(cls):

        driver.get(PAGE)
        
        WebDriverWait(driver, 360).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pagination-status")))

        try:
            var3 = driver.find_element(By.XPATH,
                                               "//div[@data-test='competitors_stats_sort_count']/div[@class='sort _margin __column']/div[1]")
            driver.execute_script("arguments[0].click();", var3)

            assert 'text' in driver.current_url

            # Variable of object list with nums
            top_desc_list = driver.find_elements(By.XPATH, '//td[@data-test="competitors_stats_count_prc"]')

            # Set array of nums
            top_desc_nums = []

            # Loop for nums appending + Trim superfluous symbols and spaces
            for num in top_desc_list:
                top_desc_nums.append(float(num.get_attribute('innerHTML').strip().replace('%', '').replace('&nbsp;', '').replace(",", "")))
            
            print('List of numbers by DESC: ', top_desc_nums)

            # Check for current sorting in array
            for i in range(len(top_desc_nums)-1):

                if top_desc_nums[i] < top_desc_nums[i+1]:

                    with open('log.txt', 'w') as file:
                        assert False, file.write("Sorting DESC %TOP not working\n")
                        break
            
            # Same operation for ASC
            top_prc_asc = driver.find_element(By.XPATH,
                                              "//div[@data-test='competitors_stats_sort_count']/div[@class='sort _margin __column']/div[2]")
            driver.execute_script("arguments[0].click();", top_prc_asc)

            assert 'sort_metrica=count_prc&sort_direction=ASC&sort_value=value' in driver.current_url

            top_asc_list = driver.find_elements(By.XPATH, '//td[@data-test="competitors_stats_count_prc"]')

            top_asc_nums = []

            for num in top_asc_list:
                top_asc_nums.append(float(num.get_attribute('innerHTML').strip().replace('%', '').replace('&nbsp;', '').replace(",", "")))
            
            print('List of numbers by ASC: ', top_desc_nums)

            for i in range(len(top_asc_nums) - 1):

                if top_asc_nums[i] > top_asc_nums[i + 1]:
                    with open('competitors_stats_log.txt', 'a+') as file:
                        assert False, file.write("Sorting ASC %TOP not working\n")
                        break

        except (AssertionError, NoSuchElementException, TimeoutException, ValueError):
            with open('log.txt', 'w') as file:
                assert False, file.write('Проблема с сортировкой по %TOP"!\n')
                allure.attach(driver.get_screenshot_as_png(), name="top_prc_sorting",
                            attachment_type=AttachmentType.PNG)
    

    # Input Data manually test
    # Test how to work with inputs
    @classmethod
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story('Chech how to put data manually in selectors')
    def test_4_Input_Data_Manually(cls):

        try:
            # Wait till element (Data selecor) loaded on page
            WebDriverWait(driver, 360).until(
            EC.presence_of_element_located(cls.data()))

            # Find and click to selector from
            date_click = driver.find_element(By.CLASS_NAME, 'calendar-input__value')
            driver.execute_script("arguments[0].click();", date_click)

            # Clear the field
            date_click.send_keys(Keys.BACKSPACE * 10)

            # Set new data
            date_from = driver.find_element(By.CSS_SELECTOR,
                                            'div.datepicker-calendars._default > div:nth-child(1) > div.calendar-input > input')
            date_from.send_keys('01.10.2021' + Keys.ENTER)

            date_to_click = driver.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div.calendar-input > input')
            driver.execute_script("arguments[0].click();", date_to_click)
            date_to_click.send_keys(Keys.BACKSPACE * 10)

            date_to = driver.find_element(By.CSS_SELECTOR,
                                          'div.datepicker-calendars._default > div:nth-child(2) > div.calendar-input > input')
            date_to.send_keys('15.10.2021' + Keys.ENTER)

            time.sleep(2)

            # Assert correct expected data in URL
            assert 'date_from=2021-10-01&date_to=2021-10-15' in driver.current_url, f'Data input not working'

        except (AssertionError, NoSuchElementException, TimeoutException):
            with open('log.txt', 'w') as file:
                assert False, file.write('Data input not working!\n')
                allure.attach(driver.get_screenshot_as_png(), name="DataManuallyFilter",
                                attachment_type=AttachmentType.PNG)
        
    # Hovers and Buttons
    # Performing and get text atribute to assert it
    @classmethod
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story('How to perform on howers and check for buttons are enabled')
    def test_5_HoversButtons_And_Buttons(cls):

        try:
            # Try to find hover icon / hint marker
            hover_filters = driver.find_element(By.CSS_SELECTOR, "#semantics-quick-filters > div.hint.tags__hint > span > span > svg")

            hover_text = hover_filters.get_attribute('innerText')

            assert 'test' in hover_text

            # Driver hover on element
            hover = ActionChains(driver).move_to_element(hover_filters)
            hover.perform()

            button = driver.find_element_by_id('button_id')

            assert button.is_displayed() and button.is_enabled()
 
        except (AssertionError, NoSuchElementException, TimeoutException):
            with open('log.txt', 'w') as file:
                file.write('hovers and button not working properly!\n')
                assert False, allure.attach(driver.get_screenshot_as_png(), name="HoversButtons",
                                            attachment_type=AttachmentType.PNG)
    # Check Access to the Page
    # Go to URL -> Wait for 10 seconds error message not located on page
    @classmethod
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story('Access Page Test')
    def test_6_Page_Access(cls):

        try:
                # Capture CSS_SELECTOR as VUE.JS error
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '.vue-notassertication-template.vue-notassertication.error')))

                with open('log.txt', 'a+') as file:
                    file.write('No access to the page!\n')
                assert_raises(TimeoutException), f'Error message was shown!'
                allure.attach(driver.get_screenshot_as_png(), name="NoAccessToPage",
                              attachment_type=AttachmentType.PNG)
                return False

            except:
                return True
    
    # This test determines if a list is unique and not repeated
    # Get to page -> Get list of task-list with date of creation -> Assert for unique in loop
    @classmethod
    @allure.severity(allure.severity_level.MINOR)
    @allure.story('Task TaskTime Unique')
    def test_7_Task_TaskTime_Unique(cls):

        # Get to oage with limits
        driver.get(BASE + '?limit=10')

        # Variable for dates of 10 elems
        the_dates = driver.find_elements(By.CLASS_NAME, 'task-item__subcontent')
        
        dates = []

        for date in the_dates:
            dates.append(date.get_attribute('innerText'))

        def array_date():

            if [dates[0]] * len(dates) != dates:
                pass
            else:
                with open('log.txt', 'a+') as file:
                    file.write('Task TaskTime  isnt Unique!\n')
                allure.attach(driver.get_screenshot_as_png(), name="UniqueTaskDates",
                              attachment_type=AttachmentType.PNG)
    
    # This test shows how to handle with windows of webdriver
    # Get to page -> Find button [On 1st window] -> Click -> Test [On 2nd window] -> Close [2nd window] -> Return back [On 1st window]
    @classmethod
    @allure.severity(allure.severity_level.MINOR)
    @allure.story('Handles')
    def test_8_Handles(cls):

        article_button = driver.find_element(By.XPATH, '//*[@id="article-btn"]')
        driver.execute_script("arguments[0].click();", article_button)
                                       
        def hande():
                                               
            # Habdle window
            handles = driver.window_handles
            driver.switch_to.window(handles[1])
            time.sleep(2)

            article = 'articles/2444259'
            
            try:
                assert article in driver.current_url
                                               
            except (AssertionError, NoSuchElementException, TimeoutException):
                    with open('log.txt', 'a+') as file:
                        file.write('Wrond test in handle!')
                        assert False, allure.attach(driver.get_screenshot_as_png(), name="WrongArticlePage",
                                  attachment_type=AttachmentType.PNG)
             # Close 2nd window
            driver.close()

            # Back to 1st window
            driver.switch_to.window(handles[0])

    @classmethod
    def tearDownClass(cls):
        driver.quit()
        print('--- Test Case Finished ---')

# Finish testing and create HTML-Report in path
if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(
        output='./reports/test.html',
        report_name="test_name", add_timestamp=False, combine_reports=False))
