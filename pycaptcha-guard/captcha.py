from selenium import webdriver
from nopecha_solution.google_recaptcha import nopechaGoogleReCaptcha
from nopecha_solution.textcaptcha import nopechaTextCaptcha
from common_components import constants

driver = webdriver.Chrome()

class SolveCaptcha:
    def __init__(self, key, captcha_type, driver) -> None:
        self.key_file = key
        self.captcha_type = captcha_type
        self.driver = driver
        
        
    def solve_captcha(self):
        
        if self.key_file == "nopecha":            
            captcha_map = {
                constants.CAPTCHA_TYPE_RECAPTCHA : (nopechaGoogleReCaptcha, 'recaptcha_solution'),
                constants.CAPTCHA_TYPE_TEXTCAPTCHA : (nopechaTextCaptcha, 'textcaptcha_solution'),
            }

        
        
        captcha_class, captcha_method = captcha_map[self.captcha_type]
        capthca_instance = captcha_class(self.driver, constants.NOPECHA_API_KEY)
        captcha, tries_count = getattr(capthca_instance, captcha_method)()
        return captcha, tries_count
    

main = SolveCaptcha('nopecha', 'recaptcha', driver)
main.solve_captcha()
    
    
