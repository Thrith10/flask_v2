import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class AppTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        self.url = "http://192.168.1.9:5000"  # Make sure this matches your Flask app's host and port
        self.valid_search_term = "SafeSearch"
        self.invalid_search_term_xss = "<script>alert('XSS')</script>"
        self.invalid_search_term_sql = "SELECT * FROM users"

    def tearDown(self):
        self.driver.quit()

    def test_search_with_valid_term(self):
        driver = self.driver
        driver.get(self.url)
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
        print(f"Page source: {driver.page_source[:500]}")  # Print first 500 characters of page source
        self.wait.until(EC.title_contains("Search Form"))

        # Enter valid search term
        search_field = self.wait.until(EC.presence_of_element_located((By.NAME, "search_term")))
        search_field.send_keys(self.valid_search_term)
        driver.find_element(By.XPATH, "//input[@value='Search']").click()

        # Check the result
        self.wait.until(EC.title_contains("Search Result"))
        result_text = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
        self.assertEqual(result_text, "Search Result")

    def test_search_with_invalid_term_xss(self):
        driver = self.driver
        driver.get(self.url)
        print(f"Page source: {driver.page_source[:500]}")  # Print first 500 characters of page source
        self.wait.until(EC.title_contains("Search Form"))

        # Enter invalid search term (XSS)
        search_field = self.wait.until(EC.presence_of_element_located((By.NAME, "search_term")))
        search_field.send_keys(self.invalid_search_term_xss)
        driver.find_element(By.XPATH, "//input[@value='Search']").click()

        # Check the result
        error_msg = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[@style='color:red;']")))
        self.assertTrue(error_msg.is_displayed())
        self.assertEqual(error_msg.text, "Input validated to be XSS attack. Please try again.")

    def test_search_with_invalid_term_sql(self):
        driver = self.driver
        driver.get(self.url)
        print(f"Page source: {driver.page_source[:500]}")  # Print first 500 characters of page source
        self.wait.until(EC.title_contains("Search Form"))

        # Enter invalid search term (SQL Injection)
        search_field = self.wait.until(EC.presence_of_element_located((By.NAME, "search_term")))
        search_field.send_keys(self.invalid_search_term_sql)
        driver.find_element(By.XPATH, "//input[@value='Search']").click()

        # Check the result
        error_msg = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[@style='color:red;']")))
        self.assertTrue(error_msg.is_displayed())
        self.assertEqual(error_msg.text, "Input validated to be SQL injection attack. Please try again.")

if __name__ == "__main__":
    unittest.main()
