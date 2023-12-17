from selenium import webdriver
from nopecha_solution.google_recaptcha import nopechaGoogleReCaptcha
from anticaptcha_solution.google_recaptcha import anticaptchaGoogleReCaptcha
from common_components import constants
import base64

driver = webdriver.Chrome()

class Main:
    def __init__(self, key, captcha_type, driver) -> None:
        self.key_file = key
        self.captcha_type = captcha_type
        self.driver = driver
        
        
    def import_fuc(self):
        
        if self.key_file == "nopecha":            
            captcha_map = {
                constants.CAPTCHA_TYPE_RECAPTCHA : (nopechaGoogleReCaptcha, 'recaptcha_solution')
            }
            
        elif self.key_file == "anticaptcha":
            captcha_map = {
                constants.CAPTCHA_TYPE_RECAPTCHA : (anticaptchaGoogleReCaptcha, 'recaptcha_solution')
            }
        
        
        captcha_class, captcha_method = captcha_map[self.captcha_type]
        capthca_instance = captcha_class(self.driver)
        captcha = getattr(capthca_instance, captcha_method)()
        return captcha

# driver.get("https://www.google.com/recaptcha/api2/demo")

# captch = GoogleReCaptcha(driver)

main = Main('nopecha', 'recaptcha', driver)
main.import_fuc()

# captch.solve_captcha()


    
    
