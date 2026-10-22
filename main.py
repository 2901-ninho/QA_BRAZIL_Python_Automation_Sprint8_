from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import data
import helpers
from pages import UrbanRoutesPage

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado.")

        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()

    def setup_method(self):
        self.driver.get('https://cnt-9532d4ed-d7f4-448f-92a7-87be5b0ad396.containerhub.tripleten-services.com?lng=pt')
        self.routes_page = UrbanRoutesPage(self.driver)

    def _prepare_comfort_order(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.click_call_taxi_button()
        self.routes_page.select_comfort_plan()

    # 1. Definir o endereço
    def test_set_route(self):
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.routes_page.get_from() == data.ADDRESS_FROM
        assert self.routes_page.get_to() == data.ADDRESS_TO

    # 2. Selecionar a tarifa Comfort
    def test_select_plan(self):
        self._prepare_comfort_order()
        assert self.routes_page.get_current_selected_plan() == 'Comfort'

    # 3. Preencher o número de telefone
    def test_fill_phone_number(self):
        self._prepare_comfort_order()
        self.routes_page.set_phone(data.PHONE_NUMBER)
        assert self.routes_page.get_phone() == data.PHONE_NUMBER

    # 4. Adicionar um cartão de crédito
    def test_fill_card(self):
        self._prepare_comfort_order()
        self.routes_page.set_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.routes_page.get_current_payment_method() == 'Cartão'

    # 5. Escrever um comentário para o motorista
    def test_comment_for_driver(self):
        self._prepare_comfort_order()
        self.routes_page.set_message_for_driver(data.MESSAGE_FOR_DRIVER)
        assert self.routes_page.get_message_for_driver() == data.MESSAGE_FOR_DRIVER

    # 6. Pedir um cobertor e lenços
    def test_order_blanket_and_handkerchiefs(self):
        self._prepare_comfort_order()
        self.routes_page.click_blanket_and_handkerchiefs()
        assert self.routes_page.is_blanket_and_handkerchiefs_selected() is True

    # 7. Pedir 2 sorvetes
    def test_order_2_ice_creams(self):
        self._prepare_comfort_order()
        self.routes_page.add_ice_cream(2)
        assert self.routes_page.get_ice_cream_amount() == 2

    # 8. Pedir o táxi e verificar o modal de busca de carro
    def test_car_search_model_appears(self):
        self._prepare_comfort_order()
        self.routes_page.set_phone(data.PHONE_NUMBER)
        self.routes_page.set_card(data.CARD_NUMBER, data.CARD_CODE)
        self.routes_page.set_message_for_driver(data.MESSAGE_FOR_DRIVER)
        self.routes_page.click_order_taxi_button()
        assert self.routes_page.get_order_popup().is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()