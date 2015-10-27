# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class Dd(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://data.oecd.org"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_dd(self):
        indicator_list = ['Décès dus au cancer',
                          'Années potentielles de vie perdues',
                          'Espérance de vie à 65 ans',
                          'Espérance de vie à la naissance',
                          'Taux de mortalité infantile',
                          'Taux de suicide',
                          'Fumeurs quotidiens',
                          'Mammographes',
                          'Consommation d\'alcool',
                          'Ressources pour la santé',
'Années potentielles de vie perdues',
'Dépenses pharmaceutiques']
        url_list = ['https://data.oecd.org/fr/healthstat/deces-dus-au-cancer.htm',
                    'https://data.oecd.org/fr/healthstat/annees-potentielles-de-vie-perdues.htm',
                    'https://data.oecd.org/fr/healthstat/esperance-de-vie-a-65-ans.htm',
                    'https://data.oecd.org/fr/healthstat/esperance-de-vie-a-la-naissance.htm',
                    'https://data.oecd.org/fr/healthstat/taux-de-mortalite-infantile.htm',
                    'https://data.oecd.org/fr/healthstat/taux-de-suicide.htm',
                    'https://data.oecd.org/fr/healthrisk/fumeurs-quotidiens.htm',
                    'https://data.oecd.org/fr/healtheqt/mammographes.htm',
                    'https://data.oecd.org/fr/healthrisk/consommation-d-alcool.htm',
                    'https://data.oecd.org/fr/healthres/depenses-de-sante.htm',
                    'https://data.oecd.org/fr/healthstat/annees-potentielles-de-vie-perdues.htm',
                    'https://data.oecd.org/fr/healthres/depenses-pharmaceutiques.htm']


        index = 0
        for url in (url_list):
            driver = self.driver
            driver.get(url)
            driver.find_element_by_css_selector("span.download-btn-label").click()
            driver.find_element_by_link_text(u"données sélectionnées (.csv)").click()
            link = driver.find_element(By.CSS_SELECTOR, "a[href*='DP_LIVE']")
            for i in range(10):
                try:
                    if "" != link.get_attribute("href"):
                        print indicator_list[index]+';'+str(link.get_attribute("href"))
                        index += 1
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out" + 'DP_LIVE')

                # def is_element_present(self, how, what):
                #     try: self.driver.find_element(by=how, value=what)
                #     except NoSuchElementException, e: return False
                #     return True
                #
                # def is_alert_present(self):
                #     try: self.driver.switch_to_alert()
                #     except NoAlertPresentException, e: return False
                #     return True
                #
                # def close_alert_and_get_its_text(self):
                #     try:
                #         alert = self.driver.switch_to_alert()
                #         alert_text = alert.text
                #         if self.accept_next_alert:
                #             alert.accept()
                #         else:
                #             alert.dismiss()
                #         return alert_text
                #     finally: self.accept_next_alert = True
                #
                # def tearDown(self):
                #     self.driver.quit()
                #     self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
