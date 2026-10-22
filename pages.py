from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from helpers import retrieve_phone_code


class UrbanRoutesPage:
    # Localizadores corrigidos e mais robustos
    FROM_FIELD = (By.ID, 'from')
    TO_FIELD = (By.ID, 'to')

    # Alterado para aceitar "Pedir" de forma genérica (evita conflito de idioma/texto exato)
    CALL_TAXI_BUTTON = (By.XPATH, '//button[contains(text(), "Pedir")]')

    COMFORT_TARIFF = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    PHONE_BUTTON = (By.XPATH, '//div[starts-with(@class, "np-button")]')
    PHONE_INPUT = (By.ID, 'phone')
    NEXT_BUTTON = (By.XPATH, '//button[text()="Próxima"]')
    CODE_INPUT = (By.ID, 'code')
    CONFIRM_CODE_BUTTON = (By.XPATH, '//button[text()="Confirmar"]')

    # Pagamento
    PAYMENT_METHOD_BUTTON = (By.XPATH, '//div[@class="pp-text" and text()="Método de pagamento"]')
    ADD_CARD_BUTTON = (By.XPATH, '//div[@class="pp-row subset" and text()="Adicionar cartão"]')
    CARD_NUMBER_INPUT = (By.ID, 'number')
    CARD_CVV_INPUT = (By.XPATH, '//div[@class="card-input-wrapper"]//input[@id="code"]')
    ADD_CARD_SUBMIT_BUTTON = (By.XPATH, '//button[text()="Adicionar"]')
    CLOSE_PAYMENT_MODAL = (By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button button"]')
    PAYMENT_LABEL = (By.XPATH, '//div[@class="pp-value-text"]')

    # Comentário e extras
    COMMENT_INPUT = (By.ID, 'comment')
    BLANKET_TOGGLE = (By.XPATH, '//div[@class="r-group"]//div[@class="switch"]')
    BLANKET_CHECKBOX = (By.XPATH, '//div[@class="r-group"]//input[@type="checkbox"]')

    # Sorvetes
    ICE_CREAM_PLUS_BUTTON = (By.XPATH, '//div[@class="r-group"]//div[text()="Sorvete"]/..//div[@class="counter-plus"]')
    ICE_CREAM_COUNTER = (By.XPATH, '//div[@class="r-group"]//div[text()="Sorvete"]/..//div[@class="counter-value"]')

    # Botão final e Modal de busca
    ORDER_BUTTON = (By.ID, 'smart-button')
    CAR_SEARCH_MODAL = (By.XPATH, '//div[@class="order-body" and contains(., "Procurando carros")]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # 1. Definir o endereço e rota (com ENTER para fechar o autocomplete)
    def set_from(self, address_from):
        from_input = self.wait.until(EC.visibility_of_element_located(self.FROM_FIELD))
        from_input.clear()
        from_input.send_keys(address_from)
        from_input.send_keys(Keys.ENTER)

    def set_to(self, address_to):
        to_input = self.wait.until(EC.visibility_of_element_located(self.TO_FIELD))
        to_input.clear()
        to_input.send_keys(address_to)
        to_input.send_keys(Keys.ENTER)

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def click_call_taxi_button(self):
        button = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON))
        button.click()

    def get_from(self):
        return self.wait.until(EC.visibility_of_element_located(self.FROM_FIELD)).get_property('value')

    def get_to(self):
        return self.wait.until(EC.visibility_of_element_located(self.TO_FIELD)).get_property('value')

    # 2. Selecionar o plano Comfort
    def select_comfort_plan(self):
        comfort_element = self.wait.until(EC.element_to_be_clickable(self.COMFORT_TARIFF))
        parent_element = comfort_element.find_element(By.XPATH, './..')
        if "active" not in parent_element.get_attribute("class") and "active" not in comfort_element.get_attribute(
                "class"):
            comfort_element.click()

    def get_current_selected_plan(self):
        comfort_element = self.wait.until(EC.visibility_of_element_located(self.COMFORT_TARIFF))
        parent_element = comfort_element.find_element(By.XPATH, './..')
        if "active" in comfort_element.get_attribute("class") or "active" in parent_element.get_attribute("class"):
            return 'Comfort'
        return ''

    # 3. Preencher o número de telefone
    def set_phone(self, phone_number):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT)).send_keys(phone_number)
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

        sms_code = retrieve_phone_code(self.driver)

        self.wait.until(EC.visibility_of_element_located(self.CODE_INPUT)).send_keys(sms_code)
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_CODE_BUTTON)).click()

    def get_phone(self):
        phone_btn = self.wait.until(EC.visibility_of_element_located(self.PHONE_BUTTON))
        return phone_btn.text

    # 4. Adicionar cartão de crédito
    def set_card(self, card_number, card_cvv):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()

        self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT)).send_keys(card_number)
        cvv_field = self.wait.until(EC.visibility_of_element_located(self.CARD_CVV_INPUT))
        cvv_field.send_keys(card_cvv)
        cvv_field.send_keys(Keys.TAB)  # Perda de foco (blur)

        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_SUBMIT_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.CLOSE_PAYMENT_MODAL)).click()

    def get_current_payment_method(self):
        label = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_LABEL))
        return label.text

    # 5. Escrever comentário para o motorista
    def set_message_for_driver(self, comment):
        self.wait.until(EC.visibility_of_element_located(self.COMMENT_INPUT)).send_keys(comment)

    def get_message_for_driver(self):
        return self.wait.until(EC.visibility_of_element_located(self.COMMENT_INPUT)).get_property('value')

    # 6. Pedir um cobertor e lenços
    def click_blanket_and_handkerchiefs(self):
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_TOGGLE)).click()

    def is_blanket_and_handkerchiefs_selected(self):
        checkbox = self.driver.find_element(*self.BLANKET_CHECKBOX)
        return checkbox.is_selected() or "checked" in checkbox.get_attribute("class")

    # 7. Pedir 2 sorvetes
    def add_ice_cream(self, count=2):
        plus_button = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON))
        for _ in range(count):
            plus_button.click()

    def get_ice_cream_amount(self):
        counter = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_COUNTER))
        return int(counter.text)

    # 8. Pedir o táxi e verificar o modal
    def click_order_taxi_button(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()

    def get_order_popup(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))