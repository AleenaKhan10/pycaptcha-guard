import time
import logging
import nopecha

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from base_page import BasePage
from captcha_locators.google_recaptcha_locator import GoogleReCaptchaLocator
from common_components import constants


class nopechaGoogleReCaptcha(BasePage):
    
    def __init__(self, driver: WebDriver, key: str) -> None:
        """
        Initializes the nopechaGoogleReCaptcha class.

        Args:
            driver (WebDriver): The WebDriver object for interacting with the web browser.
            key (str): The key for accessing the nopecha API.
        """
        super().__init__(driver)
        self.captcha = True
        self.nopecha_key = key
    
    def recaptcha_solution(self):
        
        """
            This function solves the reCAPTCHA challenge by clicking the checkbox, completing the captcha, and returning the result.

            Returns:
                bool: True if the reCAPTCHA challenge is successfully solved, False otherwise.
        """
        self.click_captcha_checkbox()
        tries_count = 0
        while self.captcha:
            tries_count += 1
            
            iframe_popup = self.wait_for_element(GoogleReCaptchaLocator.iframe_popup_recaptcha)
            self.switch_to_iframe(iframe_popup)
            self.complete_captcha()
            self.switch_to_default_content()

            iframe_popup = self.wait_for_element(GoogleReCaptchaLocator.iframe_popup_recaptcha, constants.WAIT_TIMEOUT, silent=True)
            if not iframe_popup:
                self.captcha = False
            
        return self.captcha
    
        
    def click_captcha_checkbox(self):
        
        """
            Clicks the reCAPTCHA checkbox to verify the user's action.
        """        
        iframe_recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_checkbox_recaptcha)        
        self.switch_to_iframe(iframe_recaptcha_checkbox_locator)
        
        recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.recaptcha_checkbox)
        recaptcha_checkbox_locator.click()
        
        self.switch_to_default_content()
        
        
    def get_recaptcha_text_instructions(self):
        
        """
            Returns:
                str: The text instructions for completing the reCAPTCHA.
        """        
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
        
        """
            Completes the captcha challenge using the provided parameters.

            Args:
                counter (int, optional): The number of the captcha challenge. Defaults to 1.
                image_link (str, optional): The URL of the captcha image. Defaults to None.
                all_imgs_list (list, optional): List of all captcha image URLs. Defaults to [].
        """
        text = self.get_recaptcha_text_instructions()
        total_rows = len(self.wait_for_elements(GoogleReCaptchaLocator.recaptcha_images_rows))
        all_imgs = self.wait_for_elements(GoogleReCaptchaLocator.recaptcha_images)
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
                            
        if total_rows == 3:
            grid = '3x3'
        else:
            grid = '4x4'
            
        if grid == '3x3':
            if len(unique_image_links) > 1:
                grid = '1x1'
            if int(counter) > 1:
                grid = '1x1'

        grid_click_array, bool_array = self.nopecha_captcha(text, unique_image_links, grid)

        if counter > 1 and total_rows != 4:
            grid_click_array = [pos for pos, is_true in zip(positions, bool_array) if is_true]
        

        self.click_captcha_image(grid_click_array, counter, image_link, all_imgs_list, text)


    def nopecha_captcha(self, text, unique_image_links, grid):
                
        """
            This function uses the nopecha API to solve the captcha challenge.

            Args:
                text (str): The captcha challenge text.
                unique_image_links (List[str]): List of unique image URLs.
                grid (str): The grid size of the captcha challenge.

            Returns:
                List[int]: List of grid indices to click on.
                List[bool]: List of boolean values indicating whether to click on each grid index.
        """        
        nopecha.api_key = self.nopecha_key

        try:
            clicks = nopecha.Recognition.solve(
                type='recaptcha',
                task=text,
                image_urls=unique_image_links,
                grid=grid
            )
            
        except nopecha.error.InvalidRequestError as e:
            logging.error(f'Nopecha request failed with parameters: task={text}, image_urls={unique_image_links}, grid={grid}')            
            return [], []


        true_indices = [i for i, value in enumerate(clicks) if value]
        
        grid_click_array = true_indices
        grid_click_array = [int(x+1) for x in grid_click_array]

        return grid_click_array, clicks
    

    def click_captcha_image(self, grid_click_array, counter, image_link, all_imgs_list, text):
        
        """
            This function will click on the captcha images by finding its xpath and element through grid_click_array.

            Args:
                grid_click_array (List[int]): List of numbers which are returned from the nopecha key.
        """        
        total_rows = len(self.wait_for_elements(GoogleReCaptchaLocator.recaptcha_images_rows))
        
        for number in grid_click_array:
            cell_xpath = GoogleReCaptchaLocator.get_matched_image_path(number, total_rows)
            cell = self.wait_for_element(cell_xpath)
            
            cell.click()
        
        submit_button = self.wait_for_element(GoogleReCaptchaLocator.submit_button)
        text_submit_button = submit_button.text
        text_submit_button = text_submit_button.lower().strip()
            
        if grid_click_array == []:
            submit_button.click()
                        
        elif "Click verify once there are none left" in text:
            self.complete_captcha(counter+1, image_link, all_imgs_list)
        else:
            if "skip" in text_submit_button:
                self.complete_captcha(counter+1, image_link, all_imgs_list)
            submit_button.click()