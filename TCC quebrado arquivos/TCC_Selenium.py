import re
import csv
#from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import Edge, EdgeOptions
import pandas as pd

# Função para retirar o Card do Twitter

def pegar_tweet(card):
    # Retira nome de usuario
    usuario = card.find_element_by_xpath('.//span').text
    try:
        # nome contido no @
        tagnick = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except NoSuchElementException:
        return

    try:
        # data do post
        datapost = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return

    # Demais variaveis dentro do card do tweet
    # comentario = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    resposta = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    # texto = comentario + resposta
    texto = resposta
    reply_qtd = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_qtd = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_qtd = card.find_element_by_xpath('.//div[@data-testid="like"]').text

    # retorna tudo em uma variavel
    tweet = (usuario, tagnick, datapost, texto, reply_qtd, retweet_qtd, like_qtd)
    return tweet


def Selenium_abrir(qtd , palavra_busca , BuscaTW):
    # create instance of web driver
    options = EdgeOptions()
    options.use_chromium = True
    driver = Edge(options=options)

    # navigate to login screen
    driver.get('https://twitter.com/search')
    driver.maximize_window()
    sleep(5)

    # find search input and search for term
    busca_input = driver.find_element_by_xpath('//input[@aria-label="Consulta de busca"]')
    busca_input.send_keys(palavra_busca)
    busca_input.send_keys(Keys.RETURN)
    sleep(1)

    # navigate to historical 'latest' tab
    if BuscaTW == "recente":
        driver.find_element_by_link_text('Mais recentes').click()
    else:
        driver.find_element_by_link_text('Principais').click()

    # Retira todos os Tweets da Pagina
    x = int(qtd)
    conteudo = []
    tweet_ids = set()
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    while x > 0:
        cards_pagina = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')
        for card in cards_pagina[-15:]:
            tweet = pegar_tweet(card)
            if tweet:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    conteudo.append(tweet)

        scroll_attempt = 0
        while True:
            # Verifica posição do Scroll do Navegador
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                #  final do Scroll no Local
                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    sleep(2)  # Nova tentativa de descer o Scroll
            else:
                last_position = curr_position
                break
        x = x - 1
    # Fecha Navegador e Finaliza Driver do Selenium Edge
    driver.close()
    # Salva Base em csv
    '''with open('ScrapperTwitterBase.csv', 'w', newline='', encoding='utf-8') as f:
        header = ['Usuario', 'TagNick', 'DataPost', 'Texto', 'Comentarios', 'Likes', 'Retweets']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(conteudo)'''

    df = pd.DataFrame(conteudo, columns=['Usuario', 'TagNick', 'DataPost', 'Texto', 'Comentarios', 'Likes', 'Retweets'])
    print(df)
    df.to_csv("ScrapperTwitterBase.csv", sep=';', encoding='utf-8', index=False)

def Parametros_Selenium():
    qtd = int(input("Quantidade de paginas a ser buscada no Twitter: "))
    palavra_busca = input("Palavra buscada no Twitter: ")
    BuscaTW = input("recente ou principal: ")
    Selenium_abrir(qtd, palavra_busca, BuscaTW)

Parametros_Selenium()
