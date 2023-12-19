from selenium.webdriver.remote.webdriver import WebDriver
from base_page import BasePage
from captcha_locators.textcaptcha_locator import TextCaptchaLocators
import nopecha



class nopechaTextCaptcha(BasePage):
    def __init__(self, driver: WebDriver, key: str) -> None:
        self.nopecha_key = key
        super().__init__(driver)
        
    
    def textcaptcha_solution(self):
        captcha_image_src = self.get_textcaptcha_params()
        solution = self.get_captcha_solution(captcha_image_src)
        captcha = self.fill_input_field(solution)
        return captcha
        
        
    def get_textcaptcha_params(self):
        captcha_img = self.wait_for_element(TextCaptchaLocators.captcha_img)
        captcha_img_src = captcha_img.get_attribute("src")
        return captcha_img_src
    
    
    def get_captcha_solution(self, image_src):
        nopecha.api_key = self.nopecha_key
        
        solution = nopecha.Recognition.solve(
            type='textcaptcha',
            image_urls=[image_src]
        )        
        return solution[0]
    
    
    def fill_input_field(self, solution):        
        if solution:
            self.enter_text(TextCaptchaLocators.captcha_text_field, solution)
            return True
        return False