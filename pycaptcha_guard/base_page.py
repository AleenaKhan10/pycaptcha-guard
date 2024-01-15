# Standard library imports
import logging
import random
import time
import pyautogui
from typing import List, Tuple, Optional

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException, ElementNotInteractableException, StaleElementReferenceException, JavascriptException

from pycaptcha_guard.common_components import constants

class BasePage:
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver: WebDriver) -> None:
        """ This function is called every time a new object of the base class is created"""
        self.driver = driver
        
        
    def wait_for_element(self, locator: Tuple[str, str], timeout: int=constants.WAIT_TIMEOUT, silent=False) -> Optional[WebElement]:
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            if not silent:
                logging.exception(f"Element with locator {locator} on url {self.driver.current_url} not found within {timeout} seconds")
        return None
        
        
    def switch_to_iframe(self, locator: Tuple[str, str], timeout: int = constants.WAIT_TIMEOUT) -> None:
        WebDriverWait(self.driver, timeout).until(EC.frame_to_be_available_and_switch_to_it(locator))
        
                
    def switch_to_default_content(self) -> None:
        self.driver.switch_to.default_content()
        
    def wait_for_elements(self, locator: Tuple[str, str], timeout: int=constants.WAIT_TIMEOUT, silent=False) -> Optional[List[WebElement]]:
        try:
            elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            if not silent:
                logging.exception(f"Elements with locator {locator} on url {self.driver.current_url} not found within {timeout} seconds")
        return None
    
    
    def enter_text(self, by_locator: Tuple[str, str], text: str) -> None:
        """ Performs text entry of the passed in text, in a web element whose locator is passed to it"""
        
        self.driver.execute_script("window.onfocus")
        element = self.wait_for_element(by_locator)

        if element:
            for one in text:
                element.send_keys(one)

            self.press_enter_on_element(by_locator)
        time.sleep(2) 
        
        
    def press_enter_on_element(self, locator: Tuple[str, str]):
        try:
            element = self.wait_for_element(locator, constants.WAIT_TIMEOUT, silent=True)
            if element:
                element.send_keys(Keys.ENTER)
            else:
                ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        except (NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException):
            logging.exception(f"Element with locator {locator} not found or not editable")
            
            
    def click_captcha(self, element: WebElement, iframe_measures ) -> None:
        """ 
            Performs click on captcha web element whose locator is passed to it
        """
        
        try: 
            self.move_mouse_to_captcha_element(element, iframe_measures)
        except:
            pass
        try:
            element.click()
        except:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                element.click()
            except:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView();", element)
                    self.driver.execute_script("arguments[0].click();", element)
                except:
                    pass
                
                
    def move_mouse_to_captcha_element(self, element, iframe_measures):
        """
        Move the mouse to a random location within a WebElement.

        Parameters:
        - `element`: a Selenium WebElement
        - `iframe measure`: iframe axis location for exact mouse movement
        """
        x_iframe, y_iframe, top_height = iframe_measures
                
        try:
            # Get the size and location of the element
            loc = element.location
            size = element.size

            # Obtain the window position
            window_position = self.driver.get_window_position()

            # Adjust the location of the WebElement by the position of the WebDriver's browser window
            loc['x'] += window_position['x'] + x_iframe
            loc['y'] += window_position['y'] + top_height + y_iframe

            # Get the position of each side of the element
            top, bottom = loc['y'], loc['y'] + size['height']
            left, right = loc['x'], loc['x'] + size['width']

            # Generate a random location within these bounds
            end_x = int(random.uniform(left, right))
            end_y = int(random.uniform(top, bottom))

            pyautogui.moveTo(end_x, end_y, duration=0.5)
        except:
            pass
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element)
            actions.perform()
        except:
            pass
        
                
    def get_frame_axis(self, element):
        """
            Get the locations of axis of the iframe and windows top bar height
        """
        
        x_iframe = element.location['x']
        y_iframe = element.location['y']
        top_height = self.driver.execute_script("return window.outerHeight - window.innerHeight;")
        
        return x_iframe, y_iframe, top_height