import base64
import capsolver
import logging
import time
import requests

from selenium.webdriver.remote.webdriver import WebDriver

from pycaptcha_guard.base_page import BasePage
from pycaptcha_guard.captcha_locators.textcaptcha_locator import TextCaptchaLocators
from pycaptcha_guard.common_components import constants



class capsolverTextCaptcha(BasePage):
    def __init__(self, driver: WebDriver, key: str) -> None:
        
        """
            Initializes the capsolverTextCaptcha class.

            Args:
                driver (WebDriver): The WebDriver object for interacting with the web browser.
                key (str): The key for accessing the capsolver API.
        """
        self.captcha = True
        self.capsolver_key = key
        super().__init__(driver)
        
    
    def textcaptcha_solution(self):
        
        """
            Solves the text captcha challenge by repeatedly fetching the captcha image, 
            obtaining the solution using the capsolver API, and filling the input field with the solution.

            Returns:
                bool: True if the text captcha challenge is successfully solved, False otherwise.
        """
        tries_count = 0
        while self.captcha:
            tries_count += 1
            
            url = self.driver.current_url
            captcha_image_encoded_str = self.get_textcaptcha_params()
            for _ in range(constants.MAX_RECURSION_COUNT):
                try:
                    solution = self.get_captcha_solution(captcha_image_encoded_str)
                    break
                except Exception as e:
                    logging.exception(f"Unable to get API response {e}")
                    time.sleep(4)
             
            try:       
                self.captcha = self.fill_input_field(solution)
            except Exception as e:
                logging.exception(f"Unable to write the solution in input field {e}")
            time.sleep(2)
                
            if self.driver.current_url == url:
                self.captcha = True
                
        return self.captcha, tries_count
        
        
    def get_textcaptcha_params(self):
        
        """
            Retrieves the URL of the text captcha image and encode it in Base64 str.

            Returns:
                str: Encoded STR of the image.
        """
        encoded_string = None
        captcha_img = self.wait_for_element(TextCaptchaLocators.captcha_img)
        captcha_img_src = captcha_img.get_attribute("src")
        response = requests.get(captcha_img_src)
        if response.status_code == 200:
            encoded_string = base64.b64encode(response.content).decode('utf-8')
        return encoded_string
    
    
    def get_captcha_solution(self, image_encoded_str):
        
        """
            Retrieves the solution for the captcha challenge using the provided image endcoded STR.

            Args:
                image_encoded_str (str): The endcoded STR of captcha image.

            Returns:
                str: The solution for the captcha challenge.
        """
        capsolver.api_key = self.capsolver_key
        
        task = {
            "type": "ImageToTextTask",
            "body": image_encoded_str
        }
        solution = capsolver.solve(task)
        if solution and 'text' in solution:
            solution_text = solution['text'].lower()
        return solution_text
    
    
    def fill_input_field(self, solution):   
             
        """
            Fills the input field with the provided solution for the text captcha challenge.

            Args:
                solution (str): The solution for the text captcha challenge.

            Returns:
                bool: False if the solution is successfully entered, True otherwise.
        """
        if solution:
            self.enter_text(TextCaptchaLocators.captcha_text_field, solution)
            return False
        return True