from django.contrib.auth.models import User
from selenium import webdriver

from textManipulation.textAnalyzer import TextAnalyzer
from catalogo.models import Testo
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
        self.Browser = webdriver.Chrome('integrationTests/chromedriver.exe')
        self.homepage = reverse('homepage')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('password')
        self.user.save()

    def login(self):
        """Metodo che carica la pagina di login e che ne compila i campi in modo da accedere al sito."""
        self.Browser.get(self.live_server_url)
        # inserisco lo username
        username = self.Browser.find_element_by_xpath('//*[@id="id_username"]')
        username.send_keys("testuser")
        # inserisco la password
        password = self.Browser.find_element_by_xpath('//*[@id="id_password"]')
        password.send_keys("password")
        # clicco su login
        element = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div/form/div[3]/button')
        self.Browser.execute_script("arguments[0].click();", element)

    def createText(self):
        """Metodo utilizzato per creare un testo da inserire nel database in fase di testing.
        :return: riferimento al testo creato e inserito nel database"""
        global id_text
        id_text += 1

        testo = Testo.objects.create(
            titolo="Coronavirus 2020",
            autore="Giovanni Mucci",
            tipo="Tema Scolastico",
            descrizione="prima media",
            pubblicatore=self.user
        )
        testo.success = True
        testo.text_complete = 'afdasdf il a ciao ciao ciao salutare salutare'
        testo.T = TextAnalyzer(testo.text_complete)
        testo.save()
        return testo

    def formFiller(self):
        self.login()
        self.Browser.get(self.live_server_url + "/catalogo/insert")
        # calcolo l'id del testo che sarà inserito attraverso il form della pagina
        global id_text
        id_text += 1

        # inserimento titolo
        titolo = self.Browser.find_element_by_xpath('//*[@id="id_titolo"]')
        titolo.send_keys("Prova filtro")
        # inserimento autore
        autore = self.Browser.find_element_by_xpath('//*[@id="id_autore"]')
        autore.send_keys("Prova")
        # inserimento testo
        testo = self.Browser.find_element_by_xpath('//*[@id="id_text_complete"]')
        testo.send_keys("di di di a a buongiorno buonasera")

    def newSetupBlacklist(self):
        self.login()
        self.Browser.get(self.live_server_url + "/accounts/blacklist")

        # inserisco una blackword nel textfield
        blackword = self.Browser.find_element_by_xpath('//*[@id="id_parola"]')
        blackword.send_keys("ciao")
        # inserimento della parola
        element = self.Browser.find_element_by_xpath('//*[@id="submit-id-submit"]')
        self.Browser.execute_script("arguments[0].click();", element)

    def testSignupPage(self):
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

        # raggiungimento homepage
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    # ############ TEST SUL LOGIN REQUIRED ##############
    def testLoginRedirectionFromHomepage(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url)
        time.sleep(10)

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def testNoRedirectionHomepage(self):
        """Test che verifica la corretta visualizzazione dell'homepage dopo che il login è stato effettuato."""
        self.login()

        self.Browser.get(self.live_server_url)
        alert = self.Browser.find_element_by_id("site-main-page")
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div/h1').text,
            'Analizza il vocabolario'
        )

    def testLoginRedirectionFromInsertText(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url + '/catalogo/insert/')

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def testNoRedirectionInsertText(self):
        """Test che verifica la corretta visualizzazione della pagina di inserimento del testo
        dopo che il login è stato effettuato."""
        self.login()
        self.Browser.get(self.live_server_url + '/catalogo/insert/')
        alert = self.Browser.find_element_by_id("site-main-page")
        self.assertEqual(
            alert.find_element_by_tag_name('h4').text,
            'Inserisci informazioni:'
        )

    def testLoginRedirectionFromSearch(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url + '/catalogo/search/')

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def testNoRedirectionSearch(self):
        """Test che verifica la corretta visualizzazione della pagina di ricerca del testo
        dopo che il login è stato effettuato."""
        self.login()
        self.Browser.get(self.live_server_url + '/catalogo/search/')
        alert = self.Browser.find_element_by_id("site-main-page")
        self.assertEqual(
            alert.find_element_by_tag_name('h4').text,
            'Ricerca'
        )

    def testLoginRedirectionFromVisualizeAnalysis(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url + '/catalogo/visualizza/1')

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def testNoRedirectionVisualizeAnalysis(self):
        """Test che verifica la corretta visualizzazione della pagina di visualizzazione dell'analisi del testo
        dopo che il login è stato effettuato."""
        self.login()
        self.createText()

        # controllo che si raggiunga la pagina di visualizzazione dell'analisi corretta
        self.Browser.get(self.live_server_url + f'/catalogo/visualizza/{id_text}')
        alert = self.Browser.find_element_by_id("site-main-page")
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[1]/div/div/div[1]/div[1]/p').text,
            'Autore: Giovanni Mucci'
        )

    def testLoginRedirectionFromCompare(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url + '/catalogo/compare')

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def testNoRedirectionCompare(self):
        """Test che verifica la corretta visualizzazione della pagina di comparazione dopo che il login è stato
        effettuato."""
        self.login()

        # controllo che si raggiunga la pagina di ricerca per la comparazione
        self.Browser.get(self.live_server_url + '/catalogo/compare')
        alert = self.Browser.find_element_by_id("site-main-page")
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/form/div/h4').text,
            'Compara'
        )

    def testLoginRedirectionFromCompareResults(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.createText()
        self.createText()
        self.Browser.get(self.live_server_url + f'/catalogo/compare/view/{id_text - 1}-{id_text}')

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def testNoRedirectionCompareResults(self):
        """Test che verifica la corretta visualizzazione della pagina di comparazione di 2 analisi dopo che il login è
        stato effettuato."""
        self.login()
        self.createText()
        self.createText()

        # controllo che si raggiunga la pagina di ricerca per la comparazione
        self.Browser.get(self.live_server_url + f'/catalogo/compare/view/{id_text - 1}-{id_text}')
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[1]')
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[1]/div/h5[1]/b').text,
            'Primo testo selezionato:'
        )

    def testLoginRedirectionFromGlobalStatistics(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url + '/catalogo/statistiche-globali')

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def testNoRedirectionGlobalStatistics(self):
        """Test che verifica la corretta visualizzazione della pagina di visualizzazione delle statistiche globali dopo
        che il login è stato effettuato."""
        self.login()
        self.createText()

        # controllo che si raggiunga la pagina delle statistiche globali del sito
        self.Browser.get(self.live_server_url + '/catalogo/statistiche-globali')
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div/div[1]')
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div/div[1]/p[1]/b').text,
            'Indice di complessità media:'
        )

    def testLoginRedirectionFromBlacklist(self):
        """Test che verifica il reindirizzamento alla pagina di login nel caso in cui non si fosse loggati."""
        self.Browser.get(self.live_server_url + '/accounts/blacklist')

        alert = self.Browser.find_element_by_xpath('/html/body/div[1]/div/div/div')
        self.assertEqual(
            alert.find_element_by_xpath('/html/body/div[1]/div/div/div/h2').text,
            'Login:'
        )

    def testNoRedirectionBlacklist(self):
        """Test che verifica la corretta visualizzazione della pagina di blacklist dopo che il log è stato
        effettuato. """
        self.login()
        self.createText()

        # controllo che si raggiunga la pagina di blacklist dell'account
        self.Browser.get(self.live_server_url + '/accounts/blacklist')
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[1]')
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[1]/p/b').text,
            'Inserisci le parole che non vuoi più visualizzare:'
        )

    # ########### TEST SUL HOMEPAGE ##############
    def testFromHomepageToInsertText(self):
        """Test che verifica la corretta navigazione dalla homepage alla pagina di inserimento del testo
        dopo l'opportuno click sul bottone 'Inserisci Testo'."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + '/catalogo/insert/'

        # click sul bottone "inserisci testo della navbar"
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[2]/a')
        self.Browser.execute_script("arguments[0].click();", element)
        # controllo di aver raggiunto la pagina d'inserimento
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def testFromHomepageToSearch(self):
        """Test che verifica la corretta navigazione dalla homepage alla pagina di ricerca del testo
        dopo l'opportuno click sul bottone 'Ricerca e analizza'."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + '/catalogo/search/'

        # click sul bottone di ricerca della navbar
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[3]/a')
        self.Browser.execute_script("arguments[0].click();", element)
        # controllo che si raggiunga la pagina di ricerca
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def testFromHomepageToLogout(self):
        """Test che verifica l'avvenimento della disconnessione dal sito e della navigazione alla pagina di login
        dopo l'opportuno click sul bottone 'Logout'."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + '/accounts/login/'

        # click al bottone di gestione account
        element = self.Browser.find_element_by_xpath('//*[@id="navbarDropdown"]')
        self.Browser.execute_script("arguments[0].click();", element)
        # click sul bottone di logout
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[7]/div/a[1]')
        self.Browser.execute_script("arguments[0].click();", element)
        # controllo che si raggiunga la pagina di login
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def testFromHomepageToAccountEliminationConfirmed(self):
        """Test che verifica la corretta eliminazione dell'account e della navigazione alla pagina di login
        dopo l'opportuno click sul bottone ' Eliminazione account' seguito dalla conferma."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + "/accounts/login/"

        # click al bottone di gestione account
        element = self.Browser.find_element_by_xpath('//*[@id="navbarDropdown"]')
        self.Browser.execute_script("arguments[0].click();", element)
        # click al bottone di eliminazione account
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[7]/div/a[2]')
        self.Browser.execute_script("arguments[0].click();", element)
        # conferma eliminazione
        element = self.Browser.find_element_by_xpath('//*[@id="removeModal"]/div/div/div[2]/a/button')
        self.Browser.execute_script("arguments[0].click();", element)
        # controllo che si ritorni alla pagina di signup
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def testFromHomepageToAccountEliminationNulled(self):
        """Test che verifica l'annullamento dell'eliminazione dell'account e della permanenza nella pagina homepage
        dopo l'opportuno click sul bottone ' Eliminazione account' seguito dall'annullamento."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + "/"

        # click al bottone di gestione account
        element = self.Browser.find_element_by_xpath('//*[@id="navbarDropdown"]')
        self.Browser.execute_script("arguments[0].click();", element)
        # click al bottone di eliminazione account
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[7]/div/a[2]')
        self.Browser.execute_script("arguments[0].click();", element)
        # annulla eliminazione
        element = self.Browser.find_element_by_xpath('//*[@id="removeModal"]/div/div/div[2]/button')
        self.Browser.execute_script("arguments[0].click();", element)
        # controllo che si rimanga nell'homepage
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def testFromHomepageToCompare(self):
        """Test che verifica la corretta navigazione dalla homepage alla pagina di comparazione."""
        self.login()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + '/catalogo/compare/'

        # click sul bottone di ricerca della navbar
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[4]/a')
        self.Browser.execute_script("arguments[0].click();", element)
        # controllo che si raggiunga la pagina di ricerca
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def testFromHomepageToGlobalStatistics(self):
        """Test che verifica la corretta navigazione dalla homepage alla pagina delle statistiche globali."""
        self.login()
        self.createText()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + '/catalogo/statistiche-globali/'

        # click sul bottone di ricerca della navbar
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[5]/a')
        self.Browser.execute_script("arguments[0].click();", element)
        # controllo che si raggiunga la pagina di ricerca
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def testFromHomepageToBlacklist(self):
        """Test che verifica la corretta navigazione dalla homepage alla pagina della blacklist."""
        self.login()
        self.createText()
        self.Browser.get(self.live_server_url)
        expected_url = self.live_server_url + '/accounts/blacklist/'

        # click sul bottone di ricerca della navbar
        element = self.Browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[6]/a')
        self.Browser.execute_script("arguments[0].click();", element)
        # controllo che si raggiunga la pagina di ricerca
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    # ############ TEST SULL' INSERIMENTO ##############

    # i campi inseriti saranno corretti (test sui campi fatto in catalogo/tests/testForm.py)
    def testFromInsertTextToVisualizeAnalysis(self):
        """Test che verifica la corretta navigazione dalla pagina di inserimento del testo alla pagina
        di visualizzazione dell'analisi."""

        self.formFiller()
        expected_url = self.live_server_url + f"/catalogo/visualizza/{id_text}"
        # inserimento
        element = self.Browser.find_element_by_xpath('//*[@id="submit-id-submit"]')
        self.Browser.execute_script("arguments[0].click();", element)
        # controllo il raggiungimento della corretta pagina di visualizzazione dei risultati
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    def testFromInsertTextToVisualizeAnalysisWithTwoCharactersFilter(self):
        """Test che verifica che le parole di lunghezza 2 caratteri o inferiore vengano rimosse dall'analisi del
        testo."""
        self.formFiller()
        # seleziono il filtro
        self.Browser.find_element_by_xpath('//*[@id="id_combo_filter"]').click()
        # seleziono il filtro da 2 lettere
        self.Browser.find_element_by_xpath('//*[@id="id_combo_filter"]/option[3]').click()
        # inserimento
        element = self.Browser.find_element_by_xpath('//*[@id="submit-id-submit"]')
        self.Browser.execute_script("arguments[0].click();", element)
        # controllo l'assenza delle parole di lunghezza minore di 2
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]')
        self.assertNotEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/tbody/tr[1]/td[1]').text,
            'di'
        )
        self.assertNotEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/tbody/tr[2]/td[1]').text,
            'a'
        )

    def testFromInsertTextToVisualizeAnalysisWithOneCharactersFilter(self):
        """Test che verifica che le parole di lunghezza 1 carattere o inferiore vengano rimosse dall'analisi del
        testo."""
        self.formFiller()
        self.Browser.find_element_by_xpath('//*[@id="id_combo_filter"]').click()
        # seleziono il filtro da 1 lettera
        self.Browser.find_element_by_xpath('//*[@id="id_combo_filter"]/option[2]').click()
        # inserimento
        element = self.Browser.find_element_by_xpath('//*[@id="submit-id-submit"]')
        self.Browser.execute_script("arguments[0].click();", element)

        # controllo l'assenza delle parole di lunghezza minore di 2
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]')
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/tbody/tr[1]/td[1]').text,
            'di'
        )
        self.assertNotEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/tbody/tr[2]/td[1]').text,
            'a'
        )

    def testFromBlacklistToVisualizeAnalysisWithBlacklist(self):
        """Test che verifica la scomparsa dei termini in seguito all'inserimento di una parola nella blacklist."""
        self.newSetupBlacklist()
        # creo un testo e raggiungo la pagina che ne contiene l'analisi
        self.createText()
        self.Browser.get(self.live_server_url + f'/catalogo/visualizza/{id_text}')
        # controllo che la parola ciao non sia presente nel risultato dell'analisi
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]')
        # controllo il raggiungimento della corretta pagina di visualizzazione dei risultati
        self.assertNotEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/tbody/tr[1]/td[1]').text,
            'ciao'
        )

    def testFromBlacklistToVisualizeAnalysisWithoutBlacklist(self):
        """Test che verifica la ricomparsa dei termini in seguito all'eliminazione di una parola dalla blacklist."""
        self.newSetupBlacklist()
        time.sleep(0.2)
        # rimuovo la blackword
        element = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/table/tbody/tr[2]/td[2]/button')
        self.Browser.execute_script("arguments[0].click();", element)
        # creo un testo e raggiungo la pagina che ne contiene l'analisi
        self.createText()
        self.Browser.get(self.live_server_url + f'/catalogo/visualizza/{id_text}')
        # controllo che la parola ciao sia presente nel risultato dell'analisi
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]')
        # controllo il raggiungimento della corretta pagina di visualizzazione dei risultati
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/tbody/tr[1]/td[1]').text,
            'ciao'
        )

    def testUniqueWordInBlacklist(self):
        """Test che verifica la non ripetizione di termini inseriti nella blacklist."""
        self.login()
        self.Browser.get(self.live_server_url + "/accounts/blacklist")

        # controllo il corretto funzionamento dell'inserimento nel form
        # inserisco una blackword nel textfield
        blackword = self.Browser.find_element_by_xpath('//*[@id="id_parola"]')
        blackword.send_keys("prova1")
        element = self.Browser.find_element_by_xpath('//*[@id="submit-id-submit"]')
        self.Browser.execute_script("arguments[0].click();", element)
        time.sleep(0.2)
        # la ripeto
        blackword = self.Browser.find_element_by_xpath('//*[@id="id_parola"]')
        blackword.send_keys("prova1")
        element = self.Browser.find_element_by_xpath('//*[@id="submit-id-submit"]')
        self.Browser.execute_script("arguments[0].click();", element)
        time.sleep(0.2)
        # ne inserisco una nuova
        blackword = self.Browser.find_element_by_xpath('//*[@id="id_parola"]')
        blackword.send_keys("prova2")
        element = self.Browser.find_element_by_xpath('//*[@id="submit-id-submit"]')
        self.Browser.execute_script("arguments[0].click();", element)
        time.sleep(0.2)

        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]')
        # controllo il raggiungimento della corretta pagina di visualizzazione dei risultati
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/table/tbody/tr[2]/td[1]').text,
            'prova1'
        )
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/table/tbody/tr[3]/td[1]').text,
            'prova2'
        )

    # ########### TEST SULLA RICERCA ##############

    # visualizza primo risultato della ricerca effettuata
    def testFromSearchToVisualizeAnalysis(self):
        """Test che verifica la corretta navigazione dalla pagina di ricerca alla pagina di visualizzazione
        dell'analisi selezionata, dopo l'inserimento di una query e la selezione del primo risultato."""
        self.login()
        self.createText()
        self.Browser.get(self.live_server_url + "/catalogo/search")
        expected_url = self.live_server_url + f"/catalogo/visualizza/{id_text}"

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
        # controllo il raggiungimento della corretta pagina di analisi
        self.assertEqual(
            self.Browser.current_url,
            expected_url
        )

    # ########### TEST SU ORDINAMENTO, TRADUZIONE E SINONIMI ##############
    def testMakeTokenSortByFrequencyVisualizeAnalysis(self):
        """Test che verifica il corretto ordinamento della tabella in seguito ad un click su frequenza."""
        self.login()
        self.createText()
        self.Browser.get(self.live_server_url + f"/catalogo/visualizza/{id_text}")

        # clicco sulla colonna per ordinarla
        element = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/thead/tr/th[2]')
        self.Browser.execute_script("arguments[0].click();", element)
        time.sleep(0.2)
        # controllo che sia comparsa una traduzione corretta
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]')
        # controllo il raggiungimento della corretta pagina di visualizzazione dei risultati
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/tbody/tr[1]/td[2]').text,
            '1'
        )

    def testMakeTokenSortByWordVisualizeAnalysis(self):
        """Test che verifica il corretto ordinamento della tabella in seguito ad un click su parola."""
        self.login()
        self.createText()
        self.Browser.get(self.live_server_url + f"/catalogo/visualizza/{id_text}")

        # clicco sulla colonna per ordinarla
        element = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/thead/tr/th[1]')
        self.Browser.execute_script("arguments[0].click();", element)
        time.sleep(0.2)
        # controllo che sia comparsa una traduzione corretta
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]')
        # controllo il raggiungimento della corretta pagina di visualizzazione dei risultati
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/tbody/tr[1]/td[1]').text,
            'a'
        )

    def testMakeTokenTranslationVisualizeAnalysis(self):
        """Test che verifica la corretta traduzione dei termini presenti in un'analisi di testo."""
        self.login()
        self.createText()
        self.Browser.get(self.live_server_url + f"/catalogo/visualizza/{id_text}")

        # traduzione
        element = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/form[1]/button')
        self.Browser.execute_script("arguments[0].click();", element)
        time.sleep(0.2)
        # controllo che sia comparsa una traduzione corretta
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]')
        # controllo il raggiungimento della corretta pagina di visualizzazione dei risultati
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/tbody/tr[1]/td[3]').text,
            'hi'
        )

    def testFindTokenSynonymsVisualizeAnalysis(self):
        """Test che verifica la corretta visualizzazione dei sinonimi dei termini presenti in un'analisi di testo."""
        self.login()
        self.createText()
        self.Browser.get(self.live_server_url + f"/catalogo/visualizza/{id_text}")

        # sinonimi
        element = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/form[2]/button')
        self.Browser.execute_script("arguments[0].click();", element)
        time.sleep(0.2)
        # controllo che sia comparsa una traduzione corretta
        alert = self.Browser.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/thead/tr/th[3]')
        # controllo il raggiungimento della corretta pagina di visualizzazione dei risultati
        self.assertEqual(
            alert.find_element_by_xpath('//*[@id="site-main-page"]/div[2]/div/table/tbody/tr[2]/td[3]').text,
            'Aggettivo: benefico, giovevole Verbo: accogliere,'
        )
