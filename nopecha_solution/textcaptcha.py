from selenium.webdriver.remote.webdriver import WebDriver
from base_page import BasePage
from captcha_locators.textcaptcha_locator import TextCaptchaLocators
import nopecha



class nopechaTextCaptcha(BasePage):
    def __init__(self, driver: WebDriver, key: str) -> None:
        
        """
            Initializes the nopechaTextCaptcha class.

            Args:
                driver (WebDriver): The WebDriver object for interacting with the web browser.
                key (str): The key for accessing the nopecha API.
        """
        self.captcha = True
        self.nopecha_key = key
        super().__init__(driver)
        
    
    def textcaptcha_solution(self):
        
        """
            Solves the text captcha challenge by repeatedly fetching the captcha image, 
            obtaining the solution using the nopecha API, and filling the input field with the solution.

            Returns:
                bool: True if the text captcha challenge is successfully solved, False otherwise.
        """
        tries_count = 0
        while self.captcha:
            tries_count += 1
            
            captcha_image_src = self.get_textcaptcha_params()
            solution = self.get_captcha_solution(captcha_image_src)
            self.captcha = self.fill_input_field(solution)
        return self.captcha, tries_count
        
        
    def get_textcaptcha_params(self):
        
        """
            Retrieves the URL of the text captcha image.

            Returns:
                str: The URL of the text captcha image.
        """
        captcha_img = self.wait_for_element(TextCaptchaLocators.captcha_img)
        captcha_img_src = captcha_img.get_attribute("src")
        return captcha_img_src
    
    
    def get_captcha_solution(self, image_src):
        
        """
            Retrieves the solution for the captcha challenge using the provided image source.

            Args:
                image_src (str): The URL of the captcha image.

            Returns:
                str: The solution for the captcha challenge.
        """
        nopecha.api_key = self.nopecha_key
        
        solution = nopecha.Recognition.solve(
            type='textcaptcha',
            image_urls=[image_src]
        )        
        return solution[0]
    
    
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