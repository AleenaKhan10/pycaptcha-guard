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
            
            iframe_popup = self.wait_for_element(GoogleReCaptchaLocator.iframe_popup_recaptcha)
            self.switch_to_iframe(iframe_popup)
            self.complete_captcha()
            
        return self.captcha
        
        
    def click_captcha_checkbox(self):
        
        iframe_recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_checkbox_recaptcha)        
        self.switch_to_iframe(iframe_recaptcha_checkbox_locator)
        
        recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.recaptcha_checkbox)
        recaptcha_checkbox_locator.click()
        
        self.switch_to_default_content()
        
        
    def get_recaptcha_text_instructions(self):
        
        time.sleep(2)
        instructions_text_locator = None
        try:
            instructions_text_locator = self.wait_for_element(GoogleReCaptchaLocator.instruction_text1, constants.WAIT_TIMEOUT, silent= True).text
        except:            
            try:
                instructions_text_locator = self.wait_for_element(GoogleReCaptchaLocator.instruction_text2, constants.WAIT_TIMEOUT, silent= True).text
            except:
                pass
        
        return instructions_text_locator
            
         
    def complete_captcha(self, counter=1, image_link=None, all_imgs_list=[]):

        text = self.get_recaptcha_text_instructions()
        table_iframe = self.wait_for_element(GoogleReCaptchaLocator.table_iframe)
        total_rows = len(table_iframe.find_elements(By.TAG_NAME,'tr'))
        all_imgs = table_iframe.find_elements(By.TAG_NAME,'img')
        unique_image_links = []
        positions = []
        
        if counter == 1 or total_rows == 4:
            image_link =self.wait_for_element(GoogleReCaptchaLocator.image_link).get_attribute("src")
            unique_image_links.append(image_link)

        for one_img in all_imgs:
            img_src = one_img.get_attribute("src")
            if img_src != image_link:
                if img_src not in unique_image_links:
                    if img_src not in all_imgs_list:
                        td_ancestor = one_img.find_element(By.XPATH,"ancestor::td")
                        positions.append(int(td_ancestor.get_attribute("tabIndex"))-3)
                        unique_image_links.append(img_src)

        for each in unique_image_links:
            all_imgs_list.append(each)

        grid_click_array,bool_array = self.nopecha_captcha(text, unique_image_links, total_rows, counter)

        if counter > 1 and total_rows != 4:
            grid_click_array = [pos for pos, is_true in zip(positions, bool_array) if is_true]
        

        self.click_captcha_image(grid_click_array)

        if grid_click_array == [] or total_rows == 4:
            submit_button = self.wait_for_element(GoogleReCaptchaLocator.submit_button)
            text_submit_button = submit_button.text
            text_submit_button = text_submit_button.lower().strip()
            # self.click(submit_button, x_iframe, y_iframe, top_height)
            submit_button.click()
            if "next" in text_submit_button or "skip" in text_submit_button:
                self.complete_captcha(counter+1, image_link, all_imgs_list)

        elif "Click verify once there are none left" in text:
            self.complete_captcha(counter+1, image_link, all_imgs_list)
        else:
            submit_button = self.wait_for_element(GoogleReCaptchaLocator.submit_button)
            text_submit_button = submit_button.text
            text_submit_button = text_submit_button.lower().strip()
            submit_button.click()
            if "next" in text_submit_button or "skip" in text_submit_button:
                self.complete_captcha(counter+1, image_link, all_imgs_list)



    def nopecha_captcha(self, text, unique_image_links, total_rows, counter):
        
        nopecha.api_key = self.nopecha_key
        
        if total_rows == 3:
            grid = '3x3'
        else:
            grid = '4x4'
            
        if grid == '3x3':
            if len(unique_image_links) > 1:
                grid = '1x1'
            if int(counter) > 1:
                grid = '1x1'


        try:
            clicks = nopecha.Recognition.solve(
                type='recaptcha',
                task=text,
                image_urls = unique_image_links,
                grid=grid
            )
            
        except nopecha.error.InvalidRequestError as e:
            logging.error(f'Nopecha request failed with parameters: task={text}, image_urls={unique_image_links}, grid={grid}')            
            return [], []


        true_indices = [i for i, value in enumerate(clicks) if value]
        
        grid_click_array = true_indices
        grid_click_array = [int(x+1) for x in grid_click_array]

        return grid_click_array, clicks
    

    def click_captcha_image(self, grid_click_array):
        
        """
            This function will on the captcha images by finding its xpath and element through grid_click_array.

            Args:
                grid_click_array (List of integers): List of numbers which are returned from the nopecha key.
        """
        
        total_rows = len(self.wait_for_elements(GoogleReCaptchaLocator.recaptcha_images_rows))
        
        for number in grid_click_array:
            cell_xpath = GoogleReCaptchaLocator.get_matched_image_path(number, total_rows)
            cell = self.wait_for_element(cell_xpath)
            
            cell.click()