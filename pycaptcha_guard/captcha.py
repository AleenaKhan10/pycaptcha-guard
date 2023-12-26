from selenium import webdriver
from pycaptcha_guard.nopecha_solution.google_recaptcha import nopechaGoogleReCaptcha
from pycaptcha_guard.nopecha_solution.textcaptcha import nopechaTextCaptcha
from pycaptcha_guard.common_components import constants


class SolveCaptcha:
    def __init__(self, key, key_type, captcha_type, driver) -> None:
        self.key = key
        self.key_type = key_type
        self.captcha_type = captcha_type
        self.driver = driver
        
        
    def solve_captcha(self):
        
        if self.key_type == "nopecha":            
            captcha_map = {
                constants.CAPTCHA_TYPE_RECAPTCHA : (nopechaGoogleReCaptcha, 'recaptcha_solution'),
                constants.CAPTCHA_TYPE_TEXTCAPTCHA : (nopechaTextCaptcha, 'textcaptcha_solution'),
            }

        
        
        captcha_class, captcha_method = captcha_map[self.captcha_type]
        capthca_instance = captcha_class(self.driver, self.key)
        captcha, tries_count = getattr(capthca_instance, captcha_method)()
        return captcha, tries_count
