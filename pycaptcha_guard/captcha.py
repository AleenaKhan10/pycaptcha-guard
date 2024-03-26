from pycaptcha_guard.nopecha_solution.google_recaptcha import nopechaGoogleReCaptcha
from pycaptcha_guard.nopecha_solution.textcaptcha import nopechaTextCaptcha
from pycaptcha_guard.capsolver_solution.google_recaptcha import capsolverGoogleReCaptcha
from pycaptcha_guard.capsolver_solution.textcaptcha import capsolverTextCaptcha
from pycaptcha_guard.common_components import constants


class SolveCaptcha:
    def __init__(self, key, key_type, captcha_type, driver) -> None:
        self.key = key
        self.key_type = key_type
        self.captcha_type = captcha_type
        self.driver = driver
        
        
    def solve_captcha(self):
        # Initialize captcha_map to a default value, such as an empty dictionary
        captcha_map = {}

        if self.key_type == "nopecha":
            captcha_map = {
                constants.CAPTCHA_TYPE_RECAPTCHA: (nopechaGoogleReCaptcha, 'recaptcha_solution'),
                constants.CAPTCHA_TYPE_TEXTCAPTCHA: (nopechaTextCaptcha, 'textcaptcha_solution'),
            }
        elif self.key_type == "capsolver":
            captcha_map = {
                constants.CAPTCHA_TYPE_RECAPTCHA: (capsolverGoogleReCaptcha, 'recaptcha_solution'),
                constants.CAPTCHA_TYPE_TEXTCAPTCHA : (capsolverTextCaptcha, 'textcaptcha_solution'),
            }

        captcha_class, captcha_method = captcha_map.get(self.captcha_type, (None, None))
        if captcha_class is None or captcha_method is None:
            raise ValueError(f"Unsupported captcha type or key type: {self.captcha_type}, {self.key_type}")

        captcha_instance = captcha_class(self.driver, self.key)
        captcha, tries_count = getattr(captcha_instance, captcha_method)()
        return captcha, tries_count
