from selenium.webdriver.common.by import By


class TextCaptchaLocators:
    captcha_img = (By.CSS_SELECTOR, ".a-row.a-text-center img")
    captcha_text_field = (By.ID, "captchacharacters")