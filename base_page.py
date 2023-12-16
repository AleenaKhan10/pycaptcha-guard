# Standard library imports
import os
import datetime
import logging
import random
import time
from pathlib import Path
from typing import List, Tuple, Optional, Union

# Third party imports
from PIL import Image
import pyautogui
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException, ElementNotInteractableException, StaleElementReferenceException, JavascriptException

# # Local application imports
from common_components import constants
# from common_components.context import ParamContext
# from locators.locator_base_page import BasePageLocators
# from mixins import AllMixin

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