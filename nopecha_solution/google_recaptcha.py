import nopecha
from selenium.webdriver.remote.webdriver import WebDriver
from base_page import BasePage
from captcha_locators.google_recaptcha_locator import GoogleReCaptchaLocator
from common_components import constants
import logging


class nopechaGoogleReCaptcha(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.captcha = True
        
    
    def recaptcha_solution(self):
        self.click_captcha_checkbox()
        while self.captcha:
            instructions_text, images_link, grid = self.get_recaptcha_params()
            captcha_matched_images = self.get_captcha_solution(instructions_text, images_link, grid)
            self.click_captcha_image(captcha_matched_images)
            self.captcha = self.check_style_display()
        return self.captcha
        
        
    def click_captcha_checkbox(self):
        
        iframe_recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_checkbox_recaptcha)        
        self.switch_to_iframe(iframe_recaptcha_checkbox_locator)
        
        recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.recaptcha_checkbox)
        # self.click(recaptcha_checkbox_locator)
        recaptcha_checkbox_locator.click()
        
        self.switch_to_default_content()
        
        
    def get_recaptcha_text_instructions(self):
        
        try:
            instructions_text_locator = self.wait_for_element(GoogleReCaptchaLocator.instruction_text1).text
        except:            
            try:
                instructions_text_locator = self.wait_for_element(GoogleReCaptchaLocator.instruction_text2).text
            except:
                pass
        
        return instructions_text_locator
            
         
    def get_recaptcha_params(self):
        
        image_link = []
        
        iframe_recaptcha_popup_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_popup_recaptcha)
        self.switch_to_iframe(iframe_recaptcha_popup_locator)
        
        instructions_text = self.get_recaptcha_text_instructions()
        
        iframe_recaptcha_popup_rows = self.wait_for_elements(GoogleReCaptchaLocator.recaptcha_images_rows)
        iframe_recaptcha_popup_rows_len = len(iframe_recaptcha_popup_rows)
        recaptcha_images_link = self.wait_for_element(GoogleReCaptchaLocator.recaptcha_images).get_attribute("src")
        image_link.append(recaptcha_images_link)
        
        if iframe_recaptcha_popup_rows_len == 3:
            grid = '3x3'
        else:
            grid = '4x4'
            
            
        return instructions_text, image_link, grid
    
    
    def get_captcha_solution(self, instructions_text, recaptcha_images_link, grid):
        
        nopecha.api_key = constants.NOPECHA_API_KEY
        try:
            clicks = nopecha.Recognition.solve(
                type='recaptcha',
                task=instructions_text,
                image_urls = recaptcha_images_link,
                grid=grid
            )
            
        except nopecha.error.InvalidRequestError as e:
            logging.exception(f'Nopecha request failed with parameters: task={instructions_text}, image_urls={recaptcha_images_link}, grid={grid}')
            
            logging.exception(f'Invalid request error: {e}')
    
        captcha_matched_images = [i+1 for i, value in enumerate(clicks) if value]
        
        return captcha_matched_images
    
    
    def click_captcha_image(self, captcha_matched_images):
        
        for number in captcha_matched_images:
            image_path = GoogleReCaptchaLocator.get_matched_image_path(number)
            
            image_locator = self.wait_for_element(image_path)
            image_locator.click()
            
        submit_button = self.wait_for_element(GoogleReCaptchaLocator.submit_button)
        submit_button.click()
        
        
    def check_style_display(self):
        if constants.GOOGLE_RECAPTCHA_PAGE_URL in self.driver.current_url:
            return True
        return False