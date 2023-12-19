import nopecha
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from base_page import BasePage
from captcha_locators.google_recaptcha_locator import GoogleReCaptchaLocator
from common_components import constants
import logging
import time


class nopechaGoogleReCaptcha(BasePage):
    def __init__(self, driver: WebDriver, key: str) -> None:
        super().__init__(driver)
        self.captcha = True
        self.nopecha_key = key
        
    
    def recaptcha_solution(self):
        self.click_captcha_checkbox()
        tries_count = 0
        while self.captcha:
            tries_count += 1
            instructions_text, images_link, grid, rows_length = self.get_recaptcha_params()
            captcha_matched_images = self.get_captcha_solution(instructions_text, images_link, grid)
            self.click_captcha_image(captcha_matched_images, instructions_text, images_link, grid, rows_length)
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
        
        time.sleep(5)
        instructions_text_locator = None
        try:
            instructions_text_locator = self.wait_for_element(GoogleReCaptchaLocator.instruction_text1, constants.WAIT_TIMEOUT, silent= True).text
        except:            
            try:
                instructions_text_locator = self.wait_for_element(GoogleReCaptchaLocator.instruction_text2, constants.WAIT_TIMEOUT, silent= True).text
            except:
                pass
        
        return instructions_text_locator
            
         
    def get_recaptcha_params(self, counter=1):
        
        unique_image_links = []
        positions = []
        all_imgs_list=[]
        
        iframe_recaptcha_popup_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_popup_recaptcha)
        self.switch_to_iframe(iframe_recaptcha_popup_locator)
        
        instructions_text = self.get_recaptcha_text_instructions()
        
        iframe_recaptcha_popup_rows = self.wait_for_elements(GoogleReCaptchaLocator.recaptcha_images_rows)
        iframe_recaptcha_popup_rows_len = len(iframe_recaptcha_popup_rows)
        recaptcha_images = self.wait_for_elements(GoogleReCaptchaLocator.recaptcha_images)
        
                
        if counter == 1 or iframe_recaptcha_popup_rows_len == 4:
            image_link =self.wait_for_element(GoogleReCaptchaLocator.recaptcha_images).get_attribute("src")
            unique_image_links.append(image_link)

        for one_img in recaptcha_images:
            img_src = one_img.get_attribute("src")
            if img_src != image_link:
                if img_src not in unique_image_links:
                    if img_src not in all_imgs_list:
                        td_ancestor = one_img.find_element(By.XPATH,"ancestor::td")
                        positions.append(int(td_ancestor.get_attribute("tabIndex"))-3)
                        unique_image_links.append(img_src)

        for each in unique_image_links:
            all_imgs_list.append(each)
        
        if iframe_recaptcha_popup_rows_len == 3:
            grid = '3x3'
        else:
            grid = '4x4'
            
        if grid == '3x3':
            if len(unique_image_links) > 1:
                grid = '1x1'
            if int(counter) > 1:
                grid = '1x1'
            
            
        return instructions_text, unique_image_links, grid, iframe_recaptcha_popup_rows_len
    
    
    def get_captcha_solution(self, instructions_text, recaptcha_images_link, grid):
        
        nopecha.api_key = self.nopecha_key
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
    
    
    def click_captcha_image(self, captcha_matched_images, instructions_text, images_link, grid, rows_length):
        
        for number in captcha_matched_images:
            image_path = GoogleReCaptchaLocator.get_matched_image_path(number, rows_length)
            
            image_locator = self.wait_for_element(image_path)
            image_locator.click()
            
        submit_button = self.wait_for_element(GoogleReCaptchaLocator.submit_button)
        submit_button_text = submit_button.text
        submit_button_text = submit_button_text.lower().strip()
        
        if captcha_matched_images == []:
            submit_button.click()
            
        
        elif "skip" in submit_button_text:
            captcha_matched_images = self.get_captcha_solution(instructions_text, images_link, grid)  
            self.click_captcha_image(captcha_matched_images, instructions_text, images_link, grid, rows_length)
             
        elif "Click verify once there are none left" in instructions_text:
            self.switch_to_default_content()
            instructions_text, images_link, grid, iframe_recaptcha_popup_rows_len = self.get_recaptcha_params()
            captcha_matched_images = self.get_captcha_solution(instructions_text, images_link, grid)
            self.click_captcha_image(captcha_matched_images, instructions_text, images_link, grid, rows_length)
            
        submit_button.click()
        self.switch_to_default_content()
        
        
    def check_style_display(self):
        if constants.GOOGLE_RECAPTCHA_PAGE_URL in self.driver.current_url:
            return True
        return False