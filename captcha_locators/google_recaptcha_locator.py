from selenium.webdriver.common.by import By

class GoogleReCaptchaLocator:
    iframe_checkbox_recaptcha = (By.CSS_SELECTOR,"iframe[title='reCAPTCHA']")
    recaptcha_checkbox = (By.CSS_SELECTOR, "div.recaptcha-checkbox-border")
    iframe_popup_recaptcha =  (By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']")
    instruction_text1 = (By.CLASS_NAME, "rc-imageselect-desc-no-canonical")
    instruction_text2 = (By.CLASS_NAME, "rc-imageselect-desc")
    recaptcha_images_rows = (By.XPATH, "//table//tr")
    recaptcha_images = (By.XPATH, "//table//img")