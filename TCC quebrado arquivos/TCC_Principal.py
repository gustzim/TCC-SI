from TCC_Selenium import *
from TCC_TextBlob_GoogleTrans import *
from TCC_Snscrape import *
from TCC_Flair_AnalySenti import *
from TCC_Azure import *
from time import sleep
import pandas as pd

#chama arquivo python que pega comentarios do twitter via SELENIUM e salva em CSV dentro da pasta

tipo_uso = int(input("\nDigite 1 testar frase\n"
                    "Digite 2 para extrair tweets\n"))
if tipo_uso == 2:
#1- para Webscrapping em Selenium, 2-para Webscrapping em Snscrape

    Selecao = int(input("\nDigite 1 para Webscrapping Selenium\n"
                        "Digite 2 para Webscrapping Snscrape\n"))

    if Selecao == 1:
        Parametros_Selenium()
    elif Selecao == 2:
        Parametros_Snscrape()
    else:
        "ERRO, NENHUMA OPÇÃO SELECIONADA"

#Recurso para testar Frase em analise de sentimentos
elif tipo_uso == 1:
    #Cria Dataframe que irá ser usada no modelo
    data = [['0', '0', '0', '0', '0', '0', '0']]
    df = pd.DataFrame(data, columns=['Usuario', 'TagNick',
                                     'DataPost', 'Texto', 'Comentarios', 'Likes', 'Retweets'])

    df.iat[0, 3] = input('Escreva uma frase para testar Solução')
    print(df.iat[0, 3])
    df.to_csv("ScrapperTwitterBase.csv", sep=';', encoding='utf-8', index=False)


sleep(5)
#Pega comentarios do twitter, traduz para ingles e realiza analise de sentimentos na LIB TextBlob
Executa_AnaliseSentimentos_TextBlob()
sleep(5)
# Realiza Analise de sentimentos com a solução da Azure
Executa_AnaliseSentimentos_Azure()
sleep(5)
# Realiza Analise de sentimentos com a lib Flair
Executa_AnaliseSentimentos_Flair()


