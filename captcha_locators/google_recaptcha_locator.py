from selenium.webdriver.common.by import By

class GoogleReCaptchaLocator:
    
    @staticmethod
    def get_matched_image_path(number):
        if number:
            return (By.XPATH, f'//table//td[@tabindex="{number+3}"]')
        return None
    
    
    iframe_checkbox_recaptcha = (By.CSS_SELECTOR,"iframe[title='reCAPTCHA']")
    recaptcha_checkbox = (By.CSS_SELECTOR, "div.recaptcha-checkbox-border")
    iframe_popup_recaptcha =  (By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']")
    instruction_text1 = (By.CLASS_NAME, "rc-imageselect-desc-no-canonical")
    table_iframe = (By.TAG_NAME,'table')
    instruction_text2 = (By.CLASS_NAME, "rc-imageselect-desc")
    recaptcha_images_rows = (By.XPATH, "//table//tr")
    recaptcha_images = (By.XPATH, "//table//img")
    submit_button = (By.ID,'recaptcha-verify-button')
    try_again_error = (By.CLASS_NAME, "rc-imageselect-incorrect-response")
    selecl_more_error = (By.CLASS_NAME, "rc-imageselect-error-select-more")
    select_new_error = (By.CLASS_NAME, "rc-imageselect-error-select-something")