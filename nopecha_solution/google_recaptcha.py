import nopecha
from selenium.webdriver.remote.webdriver import WebDriver
from base_page import BasePage
from captcha_locators.google_recaptcha_locator import GoogleReCaptchaLocator


class GoogleReCaptcha(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        
    
    def check_captcha(self):
        self.click_captcha_checkbox()
        self.get_recaptcha_params()
        
    def click_captcha_checkbox(self):
        
        iframe_recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_checkbox_recaptcha)        
        self.switch_to_iframe(iframe_recaptcha_checkbox_locator)
        
        recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.recaptcha_checkbox)
        # self.click(recaptcha_checkbox_locator)
        recaptcha_checkbox_locator.click()
        
        self.switch_to_default_content()
        
        
    def get_recaptcha_text_instructions(self):
        
        instructions_text_locator = self.wait_for_element(GoogleReCaptchaLocator.instruction_text1).text
        if not instructions_text_locator:
            instructions_text_locator = self.wait_for_element(GoogleReCaptchaLocator.instruction_text2).text
        
        return instructions_text_locator
            
         
    def get_recaptcha_params(self):
        
        iframe_recaptcha_popup_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_popup_recaptcha)
        self.switch_to_iframe(iframe_recaptcha_popup_locator)
        
        instructions_text = self.get_recaptcha_text_instructions()
        
        iframe_recaptcha_popup_rows = self.wait_for_elements(GoogleReCaptchaLocator.recaptcha_images_rows)
        iframe_recaptcha_popup_rows_len = len(iframe_recaptcha_popup_rows)
        recaptcha_images_link = self.wait_for_element(GoogleReCaptchaLocator.recaptcha_images).get_attribute("src")
        
        if iframe_recaptcha_popup_rows_len == 3:
            grid = '3x3'
        else:
            grid = '4x4'
            
        return instructions_text, recaptcha_images_link, grid
    
    
    