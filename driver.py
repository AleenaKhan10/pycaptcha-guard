from selenium import webdriver
from nopecha_solution.google_recaptcha import GoogleReCaptcha

driver = webdriver.Chrome()

driver.get("https://www.google.com/recaptcha/api2/demo")

captch = GoogleReCaptcha(driver)

captch.solve_captcha()