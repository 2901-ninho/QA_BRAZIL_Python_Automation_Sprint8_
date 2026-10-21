import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers import retrieve_phone_code


class UrbanRoutesPage:
 # --- Endereços ---
 FROM_LOCATOR = (By.ID, 'from')
 TO_LOCATOR = (By.ID, 'to')

 # --- Solicitação de táxi e tarifas ---
 CALL_TAXI_BUTTON_LOCATOR = (By.XPATH, '//button[contains(text(), "Chamar")]')
 COMFORT_PLAN_LOCATOR = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
 ACTIVE_PLAN_LOCATOR = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-title"]')

 # --- Telefone ---
 PHONE_BUTTON_LOCATOR = (By.XPATH, '//div[@class="np-button"]')
 PHONE_INPUT_LOCATOR = (By.ID, 'phone')
 PHONE_NEXT_BUTTON_LOCATOR = (By.XPATH, '//button[text()="Próximo"]')
 SMS_CODE_INPUT_LOCATOR = (By.XPATH, '//div[@class="section active"]//input[@id="code"]')
 PHONE_CONFIRM_BUTTON_LOCATOR = (By.XPATH, '//button[text()="Confirmar"]')
 PHONE_TEXT_LOCATOR = (By.CLASS_NAME, 'np-text')

 # --- Cartão ---
 PAYMENT_METHOD_LOCATOR = (By.CLASS_NAME, 'pp-button')
 ADD_CARD_LOCATOR = (By.CLASS_NAME, 'pp-plus-container')
 CARD_NUMBER_INPUT_LOCATOR = (By.ID, 'number')
 CARD_CODE_INPUT_LOCATOR = (By.XPATH, '//div[@class="card-code-input"]//input[@id="code"]')
 CARD_SUBMIT_BUTTON_LOCATOR = (By.XPATH, '//button[text()="Adicionar"]')
 CARD_CLOSE_BUTTON_LOCATOR = (
 By.XPATH,
 '//div[@class="payment-picker open"]'
 '//button[@class="close-button section-close"]'
 )
 CURRENT_PAYMENT_LOCATOR = (By.CLASS_NAME, 'pp-value-text')

 # --- Opções da corrida ---
 COMMENT_LOCATOR = (By.ID, 'comment')
 BLANKET_SWITCH_LOCATOR = (
 By.XPATH,
 '//div[@class="r-sw-label" and text()="Cobertor e lenços"]'
 '/following-sibling::div//span[@class="slider round"]'
 )
 BLANKET_INPUT_LOCATOR = (
 By.XPATH,
 '//div[@class="r-sw-label" and text()="Cobertor e lenços"]'
 '/following-sibling::div//input[@type="checkbox"]'
 )
 ICE_CREAM_PLUS_LOCATOR = (
 By.XPATH,
 '//div[@class="r-counter-label" and text()="Sorvete"]'
 '/following-sibling::div//div[@class="counter-plus"]'
 )
 ICE_CREAM_VALUE_LOCATOR = (
 By.XPATH,
 '//div[@class="r-counter-label" and text()="Sorvete"]'
 '/following-sibling::div//div[@class="counter-value"]'
 )
 # --- Confirmação do pedido ---
 ORDER_BUTTON_LOCATOR = (By.CLASS_NAME, 'smart-button-wrapper')
 ORDER_POPUP_LOCATOR = (By.CLASS_NAME, 'order-body')

 def __init__(self, driver):
 self.driver = driver
 self.wait = WebDriverWait(driver, 10)

 # ----- Métodos auxiliares (esperas explícitas) -----
 def _find(self, locator):
 return self.wait.until(EC.presence_of_element_located(locator))

 def _visible(self, locator):
 return self.wait.until(EC.visibility_of_element_located(locator))

 def _click(self, locator):
 self.wait.until(EC.element_to_be_clickable(locator)).click()

 def _type(self, locator, text):
 self._visible(locator).send_keys(text)

 def _scroll_to(self, locator):
 element = self._find(locator)
 self.driver.execute_script("arguments[0].scrollIntoView();", element)

 # ----- Endereços -----
 def set_from(self, from_address):
 self._type(self.FROM_LOCATOR, from_address)

 def set_to(self, to_address):
 self._type(self.TO_LOCATOR, to_address)

 def set_route(self, from_address, to_address):
 self.set_from(from_address)
 self.set_to(to_address)

 def get_from(self):
 return self._find(self.FROM_LOCATOR).get_property('value')

 def get_to(self):
 return self._find(self.TO_LOCATOR).get_property('value')

 # ----- Solicitação de táxi e tarifa Comfort -----
 def click_call_taxi_button(self):
 self._click(self.CALL_TAXI_BUTTON_LOCATOR)

 def select_comfort_plan(self):
 self._scroll_to(self.COMFORT_PLAN_LOCATOR)
 self._click(self.COMFORT_PLAN_LOCATOR)

 def get_current_selected_plan(self):
 return self._find(self.ACTIVE_PLAN_LOCATOR).text

 # ----- Telefone -----
 def set_phone(self, phone_number):
 self._click(self.PHONE_BUTTON_LOCATOR)
 self._type(self.PHONE_INPUT_LOCATOR, phone_number)
 self._click(self.PHONE_NEXT_BUTTON_LOCATOR)
 code = retrieve_phone_code(self.driver)
 self._type(self.SMS_CODE_INPUT_LOCATOR, code)
 self._click(self.PHONE_CONFIRM_BUTTON_LOCATOR)

 def get_phone(self):
 return self._find(self.PHONE_TEXT_LOCATOR).text

 # ----- Cartão -----
 def set_card(self, card_number, card_code):
 self._click(self.PAYMENT_METHOD_LOCATOR)
 self._click(self.ADD_CARD_LOCATOR)
 self._type(self.CARD_NUMBER_INPUT_LOCATOR, card_number)
 self._type(self.CARD_CODE_INPUT_LOCATOR, card_code)
 # Tab tira o foco do campo e habilita o botão "Adicionar"
 self._find(self.CARD_CODE_INPUT_LOCATOR).send_keys(Keys.TAB)
 self._click(self.CARD_SUBMIT_BUTTON_LOCATOR)
 self._click(self.CARD_CLOSE_BUTTON_LOCATOR)

 def get_current_payment_method(self):
 return self._find(self.CURRENT_PAYMENT_LOCATOR).text

 # ----- Comentário -----
 def set_message_for_driver(self, message):
 self._scroll_to(self.COMMENT_LOCATOR)
 self._type(self.COMMENT_LOCATOR, message)

 def get_message_for_driver(self):
 return self._find(self.COMMENT_LOCATOR).get_property('value')

 # ----- Cobertor e lenços -----
 def click_blanket_and_handkerchiefs(self):
 self._scroll_to(self.BLANKET_SWITCH_LOCATOR)
 self._click(self.BLANKET_SWITCH_LOCATOR)

 def is_blanket_and_handkerchiefs_selected(self):
 return self._find(self.BLANKET_INPUT_LOCATOR).get_property('checked')

 # ----- Sorvetes -----
 def add_ice_cream(self, amount):
 self._scroll_to(self.ICE_CREAM_PLUS_LOCATOR)
 for _ in range(amount):
 self._click(self.ICE_CREAM_PLUS_LOCATOR)

 def get_ice_cream_amount(self):
 return int(self._find(self.ICE_CREAM_VALUE_LOCATOR).text)

 # ----- Pedir o táxi -----
 def click_order_taxi_button(self):
 self._click(self.ORDER_BUTTON_LOCATOR)

 def get_order_popup(self):
 return self._visible(self.ORDER_POPUP_LOCATOR)
