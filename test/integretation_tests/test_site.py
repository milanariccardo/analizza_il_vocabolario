from django.contrib.auth.models import User
from django.test import Client
from selenium import webdriver

from Text_manipulation.TextAnalyzer import TextAnalyzer
from catalogo.models import Testo, Token
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

id_text = 0


class TestSite(StaticLiveServerTestCase):
    """Classe che testa tutte le possibili interazioni che l'utente può avere con la User Interface,
    di conseguenza testa la corretta interazione tra i moduli del sito."""

    def setUp(self):
        """Metodo per impostare l'ambiente in cui si svolge il test:
        viene creato uno user che verrà utilizzato nel corso del test,
        viene inoltre selezionato il browser su cui i test verranno eseguiti."""
        self.Browser = webdriver.Chrome('integretation_tests/chromedriver.exe')
        self.homepage = reverse('homepage')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()

    def login(self):
        """Metodo che carica la pagina di login e che ne compila i campi in modo da accedere al sito."""
        self.Browser.get(self.live_server_url)
        username = self.Browser.find_element_by_xpath('//*[@id="id_username"]')
        username.send_keys("testuser")
        password = self.Browser.find_element_by_xpath('//*[@id="id_password"]')
        password.send_keys("password")
        element = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div/form/div[3]/button')
        self.Browser.execute_script("arguments[0].click();", element)

    def createText(self):
        """Metodo utilizzato per creare un testo da inserire nel database in fase di testing.
        :return: riferimento al testo creato e inserito nel database"""
        testo = Testo.objects.create(
            titolo="Coronavirus 2020",
            autore="Giovanni Mucci",
            tipo="Tema Scolastico",
            descrizione="prima media",
            pubblicatore=self.user
        )
        testo.success = True
        testo.text_complete = 'afdasdf'
        testo.T = TextAnalyzer(testo.text_complete)
        testo.save()
        return testo

    def test_signup_page(self):
        """Test che verifica la corretta visualizzazione dell'homepage dopo il signup di un nuovo utente
        ed il seguente login."""
        expected_url = self.live_server_url + '/'

        # creazione dell'account
        self.Browser.get(self.live_server_url + '/accounts/signup/')
        username = self.Browser.find_element_by_xpath('//*[@id="id_username"]')
        username.send_keys("prvsignup")
        password = self.Browser.find_element_by_xpath('//*[@id="id_password1"]')
        password.send_keys("uhfncjwqeirflkqwer")
        conferma_password = self.Browser.find_element_by_xpath('//*[@id="id_password2"]')
        conferma_password.send_keys("uhfncjwqeirflkqwer")
        element = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div/form/center/button')
        self.Browser.execute_script("arguments[0].click();", element)

        # login
        username_log = self.Browser.find_element_by_xpath('//*[@id="id_username"]')
        username_log.send_keys("prvsignup")
        password_log = self.Browser.find_element_by_xpath('//*[@id="id_password"]')
        password_log.send_keys("uhfncjwqeirflkqwer")
        element = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div/form/div[3]/button')
        self.Browser.execute_script("arguments[0].click();", element)

        # raggiungimento login
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )


    ############ TEST SUL LOGIN REQUIRED ##############
    def test_login_redirection_from_homepage(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url)
        time.sleep(10)

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def test_no_redirection_homepage(self):
        """Test che verifica la corretta visualizzazione dell'homepage dopo che il login è stato effettuato."""
        self.login()

        self.Browser.get(self.live_server_url)
        # time.sleep(10)
        alert = self.Browser.find_element_by_id("site-main-page")
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/h1').text,
            'Analizza il vocabolario'
        )

    def test_login_redirection_from_insert_text(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url + '/catalogo/insert/')
        # time.sleep(60)

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def test_no_redirection_insert_text(self):
        """Test che verifica la corretta visualizzazione della pagina di inserimento del testo
        dopo che il login è stato effettuato."""
        self.login()
        self.Browser.get(self.live_server_url + '/catalogo/insert/')
        # time.sleep(10)
        alert = self.Browser.find_element_by_id("site-main-page")
        self.assertEqual(
            alert.find_element_by_tag_name('h4').text,
            'Inserisci informazioni:'
        )

    def test_login_redirection_from_search(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url + '/catalogo/search/')
        # time.sleep(60)

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def test_no_redirection_search(self):
        """Test che verifica la corretta visualizzazione della pagina di ricerca del testo
        dopo che il login è stato effettuato."""
        self.login()
        self.Browser.get(self.live_server_url + '/catalogo/search/')
        # time.sleep(10)
        alert = self.Browser.find_element_by_id("site-main-page")
        self.assertEqual(
            alert.find_element_by_tag_name('h4').text,
            'Ricerca'
        )

    def test_login_redirection_from_visualize_analysis(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url + '/catalogo/visualizza/1')
        # time.sleep(60)

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def test_no_redirection_visualize_analysis(self):
        """Test che verifica la corretta visualizzazione della pagina di visualizzazione dell'analisi del testo
        dopo che il login è stato effettuato."""
        self.login()
        self.createText()
        global id_text
        id_text += 1
        self.Browser.get(self.live_server_url + '/catalogo/visualizza/' + str(id_text))
        # time.sleep(10)
        alert = self.Browser.find_element_by_id("site-main-page")
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[1]/h4[1]').text,
            'Autore: Giovanni Mucci'
        )

    # ########### TEST SUL HOMEPAGE ##############
    def test_from_homepage_to_insert_text(self):
        """Test che verifica la corretta navigazione dalla homepage alla pagina di inserimento del testo
        dopo l'opportuno click sul bottone 'Inserisci Testo'."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + '/catalogo/insert/'
        # alert = self.Browser.find_element_by_id('Inserisci-testo-btn')
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[2]/a')
        self.Browser.execute_script("arguments[0].click();", element)
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def test_from_homepage_to_search(self):
        """Test che verifica la corretta navigazione dalla homepage alla pagina di ricerca del testo
        dopo l'opportuno click sul bottone 'Ricerca e analizza'."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + '/catalogo/search/'
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[3]/a')
        self.Browser.execute_script("arguments[0].click();", element)
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def test_from_homepage_to_logout(self):
        """Test che verifica l'avvenimento della disconnessione dal sito e della navigazione alla pagina di login
        dopo l'opportuno click sul bottone 'Logout'."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + '/accounts/login/'
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[5]/a')
        self.Browser.execute_script("arguments[0].click();", element)
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def test_from_homepage_to_account_elimination_confirmed(self):
        """Test che verifica la corretta eliminazione dell'account e della navigazione alla pagina di login
        dopo l'opportuno click sul bottone ' Eliminazione account' seguito dalla conferma."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + "/accounts/login/"
        # click al bottone di eliminazione dell'account
        element = self.Browser.find_element_by_xpath('/html/body/footer/div[1]/button')
        self.Browser.execute_script("arguments[0].click();", element)
        # conferma eliminazione
        element = self.Browser.find_element_by_xpath('//*[@id="removeModal"]/div/div/div[2]/a/button')
        self.Browser.execute_script("arguments[0].click();", element)
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def test_from_homepage_to_account_elimination_nulled(self):
        """Test che verifica l'annullamento dell'eliminazione dell'account e della permanenza nella pagina homepage
        dopo l'opportuno click sul bottone ' Eliminazione account' seguito dall'annullamento."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + "/"
        # click al bottone di eliminazione dell'account
        element = self.Browser.find_element_by_xpath('/html/body/footer/div[1]/button')
        self.Browser.execute_script("arguments[0].click();", element)
        # conferma eliminazione
        element = self.Browser.find_element_by_xpath('//*[@id="removeModal"]/div/div/div[2]/button')
        self.Browser.execute_script("arguments[0].click();", element)
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    ############ TEST SULL' INSERIMENTO ##############

    # # i campi inseriti saranno corretti (test sui campi fatto in catalogo/tests/test_form.py)
    def test_from_insert_text_to_visualize_analysis(self):
        """Test che verifica la corretta navigazione dalla pagina di inserimento del testo alla pagina
        di visualizzazione dell'analisi nel caso in cui la checkanalyze 'Visualizza risultati' sia abilitata."""
        self.login()
        self.Browser.get(self.live_server_url + "/catalogo/insert")
        global id_text
        id_text += 1
        expected_url = self.live_server_url + "/catalogo/visualizza/" + str(id_text)
        # inserimento titolo
        titolo = self.Browser.find_element_by_xpath('//*[@id="id_titolo"]')
        titolo.send_keys("La divina commedia")
        # inserimento autore
        autore = self.Browser.find_element_by_xpath('//*[@id="id_autore"]')
        autore.send_keys("Dante Alighieri")
        # inserimento testo
        testo = self.Browser.find_element_by_xpath('//*[@id="id_text_complete"]')
        testo.send_keys("Nel mezzo del cammin di nostra vita")
        # conferma di visualizzazione del risultato
        element = self.Browser.find_element_by_xpath('//*[@id="id_check_analyze"]')
        self.Browser.execute_script("arguments[0].click();", element)
        # inserimento
        element = self.Browser.find_element_by_xpath('//*[@id="submit-id-submit"]')
        self.Browser.execute_script("arguments[0].click();", element)
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    # i campi inseriti saranno corretti (test sui campi fatto in catalogo/tests/test_form.py)
    def test_from_insert_text_to_insert_text(self):
        """Test che verifica la corretta permanenza nella pagina di inserimento del testo
         nel caso in cui la checkanalyze 'Visualizza risultati' non sia abilitata."""
        self.login()
        self.Browser.get(self.live_server_url + "/catalogo/insert/")
        expected_url = self.live_server_url + "/catalogo/insert/"
        global id_text
        id_text += 1
        # inserimento titolo
        titolo = self.Browser.find_element_by_xpath('//*[@id="id_titolo"]')
        titolo.send_keys("La divina commedia")
        # inserimento autore
        autore = self.Browser.find_element_by_xpath('//*[@id="id_autore"]')
        autore.send_keys("Dante Alighieri")
        # inserimento testo
        testo = self.Browser.find_element_by_xpath('//*[@id="id_text_complete"]')
        testo.send_keys("Nel mezzo del cammin di nostra vita")
        # inserimento
        element = self.Browser.find_element_by_xpath('//*[@id="submit-id-submit"]')
        self.Browser.execute_script("arguments[0].click();", element)
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    ########### TEST SULLA RICERCA ##############

    # visualizza primo risultato della ricerca effettuata
    def test_from_search_to_visualize_analysis(self):
        """Test che verifica la corretta navigazione dalla pagina di ricerca alla pagina di visualizzazione
        dell'analisi selezionata, dopo l'inserimento di una query e la selezione del primo risultato."""
        self.login()
        self.createText()
        self.Browser.get(self.live_server_url + "/catalogo/search")
        global id_text
        id_text += 1
        expected_url = self.live_server_url + "/catalogo/visualizza/" + str(id_text)
        # inserimento titolo
        titolo = self.Browser.find_element_by_xpath('//*[@id="id_titolo"]')
        titolo.send_keys("Coronavirus 2020")
        # inserimento autore
        autore = self.Browser.find_element_by_xpath('//*[@id="id_autore"]')
        autore.send_keys("Giovanni Mucci")
        # ricerca
        element = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/form/div/button')
        self.Browser.execute_script("arguments[0].click();", element)
        # visualizza l'analisi
        element = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div/table/tbody/tr[2]/td[6]/a')
        self.Browser.execute_script("arguments[0].click();", element)
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )
