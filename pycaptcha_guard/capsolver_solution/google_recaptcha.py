import time
import logging
import capsolver
import requests
import base64

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

from pycaptcha_guard.base_page import BasePage
from pycaptcha_guard.captcha_locators.google_recaptcha_locator import GoogleReCaptchaLocator
from pycaptcha_guard.common_components import constants


class capsolverGoogleReCaptcha(BasePage):
    
    def __init__(self, driver: WebDriver, key: str) -> None:
        
        """
            Initializes the capsolverGoogleReCaptcha class.

            Args:
                driver (WebDriver): The WebDriver object for interacting with the web browser.
                key (str): The key for accessing the capsolver API.
        """
        super().__init__(driver)
        self.captcha = True
        self.capsolver_key = key
        
    
    def recaptcha_solution(self): 
               
        """
            This function solves the reCAPTCHA challenge by clicking the checkbox, completing the captcha, and returning the result.

            Returns:
                bool: False if the reCAPTCHA challenge is successfully solved, True otherwise otherwise.
        """
        self.click_captcha_checkbox()
        tries_count = 0
        start_time = time.time()
        
        while self.captcha and tries_count < constants.RECURSION_COUNT_SIX:
            if round(time.time() - start_time) > constants.CAPTCHA_MAX_TIME:
                logging.info('Going to click to checkbox again')
                start_time = time.time()
                self.click_captcha_checkbox()
            
            tries_count += 1
            
            iframe_popup = self.wait_for_element(GoogleReCaptchaLocator.iframe_popup_recaptcha)
            time.sleep(2)
            iframe_popup_measures = self.get_frame_axis(iframe_popup, GoogleReCaptchaLocator.iframe_popup_recaptcha)
            self.switch_to_iframe(iframe_popup)
            try:
                logging.info("Solving captcha")
                self.complete_captcha(iframe_popup_measures)                
              
            except Exception as e:
                logging.exception(f"Error while solving captcha {e}")

                
            logging.info('Going to switch to the default content')
            self.switch_to_default_content()

            time.sleep(3)
            iframe_popup = self.wait_for_element(GoogleReCaptchaLocator.iframe_popup_recaptcha, constants.WAIT_TIMEOUT, silent=True)
            logging.info('Iframe found Trying again')
            if not iframe_popup:
                self.captcha = False
            
        return self.captcha, tries_count
    
    
    def click_captcha_checkbox(self):
        
        """
            Clicks the reCAPTCHA checkbox to verify the user's action.
        """        
        iframe_recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.iframe_checkbox_recaptcha)  
        iframe_recaptcha_checkbox_locator_measures = self.get_frame_axis(iframe_recaptcha_checkbox_locator, GoogleReCaptchaLocator.iframe_checkbox_recaptcha)       
        self.switch_to_iframe(iframe_recaptcha_checkbox_locator)
        
        recaptcha_checkbox_locator = self.wait_for_element(GoogleReCaptchaLocator.recaptcha_checkbox)
        self.click_captcha(recaptcha_checkbox_locator, iframe_recaptcha_checkbox_locator_measures)
        
        self.switch_to_default_content()
        
        
    def complete_captcha(self, iframe_popup_measures):
        
        """
            Completes the captcha challenge using the provided parameters.

            Args:
                iframe measures (list, required): List of measures of iframe's x-axis and y-axis and top height of browser. 
                counter (int, optional): The number of the captcha challenge. Defaults to 1.
                image_link (str, optional): The URL of the captcha image. Defaults to None.
                all_imgs_list (list, optional): List of all captcha image URLs. Defaults to [].
        """
        text = self.get_recaptcha_text_instructions()
        full_image_locator = self.wait_for_element(GoogleReCaptchaLocator.recaptcha_full_image)
        if full_image_locator:
            img_source = full_image_locator.get_attribute('src')
            logging.info(f"Image source found: {img_source}")
        
        for _ in range(constants.MAX_RECURSION_COUNT):
            try:
                grid_click_array, bool_array = self.capsolver_captcha(text)
                break
            except Exception as e:
                logging.exception(f"Unable to get the API response : {e}") 
                time.sleep(4)
        

        self.click_captcha_image(iframe_popup_measures, grid_click_array, text)
        
            
    def click_captcha_image(self, iframe_popup_measures, grid_click_array, text):
        
        """
            This function will click on the captcha images by finding its xpath and element through grid_click_array.

            Args:
                grid_click_array (List[int]): List of numbers which are returned from the nopecha key.
        """        
        total_rows = len(self.wait_for_elements(GoogleReCaptchaLocator.recaptcha_images_rows))
        
        for number in grid_click_array:
            cell_xpath = GoogleReCaptchaLocator.get_matched_image_path(number, total_rows)
            cell = self.wait_for_element(cell_xpath)            
            self.click_captcha(cell, iframe_popup_measures)
        
        submit_button = self.wait_for_element(GoogleReCaptchaLocator.submit_button)
        text_submit_button = submit_button.text
        text_submit_button = text_submit_button.lower().strip()
        time.sleep(4)
            
        if grid_click_array == []:
            self.click_captcha(submit_button, iframe_popup_measures)
        elif "Click verify once there are none left" in text:
            self.complete_captcha(iframe_popup_measures)
        else:
            if "skip" in text_submit_button:
                self.complete_captcha(iframe_popup_measures)
            self.click_captcha(submit_button, iframe_popup_measures)
            
                    
    def capsolver_captcha(text, image_url):
        """
        This function sends the captcha image to the capsolver API and returns the solution.

        Args:
            text (str): The text instructions for completing the reCAPTCHA.
            image_url (str): The URL of the captcha image.

        Returns:
            solution: The solution returned by the capsolver API.
        """
        # Optimize the code by checking the response status directly in the if condition
        if requests.get(image_url).status_code == 200:
            # Use context manager for file operations for better resource management
            with requests.get(image_url) as response, open("captcha_image.png", "wb") as f:
                f.write(response.content)
            
            # Convert the image to a base64 encoded string
            with open("captcha_image.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prepare the payload for the capsolver API
            payload = {
                "type": "ReCaptchaV2Classification",
                "image": encoded_string,
                "question": "/m/0199g",
            }
            
            # Send the payload to the capsolver API and get the solution
            solution = capsolver.solve(payload)
            
            # Print the solution for debugging purposes
            print(solution)
            
            
            
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