#GITHUB da solução: https://github.com/JustAnotherArchivist/snscrape
#Tutorial de utilização em canal brasileiro: https://www.youtube.com/watch?v=ZxWx0nt3rPE
#Tutorial de utilização em canal estrangeiro: https://www.youtube.com/watch?v=jtIMnmbnOFo

#Importa webscrapping snscrape
import snscrape.modules.twitter as sntwitter
import pandas as pd

def Parametros_Snscrape():

    contador = 0

    #pesquisar tweet por usuario ou palavra
    condicao = int(input('1 - Pesquisar tweets de usuario\n'
          '2 - Pesquisar palavra:\n '))

    if condicao == 1:
        palavra = '(from:' + input('Digite o nome do usuario para pesquisar:\n ') + ')'
    elif condicao == 2:
        palavra = input('Digite a palavra para pesquisar: \n')
    else:
        print('Erro')


    #selecionar idioma do tweet ou sem idioma
    condicao = ''
    condicao = int(input('1 - Idioma Portugues\n'
                     '2 - Idioma Inglês\n'
                     '3 - Qualquer idioma:\n '))

    if condicao == 1:
        idioma = 'lang:pt'
        contador = 1
    elif condicao == 2:
        idioma = 'lang:en'
        contador = 1

    #periodo especifico do tweet ou sem periodo
    condicao = int(input('1 - Pesquisar em periodo especifico\n'
                     '2 - Qualquer periodo:\n '))

    if condicao == 1 and contador == 1:
        dt_inicio = 'since:'+input('(FORMATO YYYY-MM-DD) Digite a data de Inicio:\n ')
        dt_fim = 'until:'+input('(FORMATO YYYY-MM-DD) Digite a data de fim:\n ')
        contador = 2
    elif condicao == 1:
        dt_inicio = 'since:'+input('(FORMATO YYYY-MM-DD) Digite a data de Inicio:\n ')
        dt_fim = 'until:'+input('(FORMATO YYYY-MM-DD) Digite a data de fim:\n ')
        contador = 3

    #pesquisar palavra e idioma
    if contador == 1:
        query = palavra +" " + idioma

    #pesquisar palavra, idioma e data
    elif contador == 2:
        query = palavra +" " + idioma + " " + dt_fim + " " + dt_inicio

    #pesquisar palavra e data
    elif contador == 3:
        query = palavra +" " + dt_fim + " " + dt_inicio

    #pesquisar somente palavra
    else:
        query = palavra

    tweets = []
    limit = int(input("Quantos tweets deseja extrair?  "))

    #looping do webscrapping para retirar tweets
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():

        # print(vars(tweet))
        # break
        if len(tweets) == limit:
            break
        else:
            tweets.append([tweet.user.displayname, tweet.user.username, tweet.date, tweet.content, tweet.quoteCount,
                           tweet.likeCount,tweet.retweetCount])

    df = pd.DataFrame(tweets, columns=['Usuario', 'TagNick', 'DataPost' , 'Texto', 'Comentarios','Likes','Retweets'])
    print(df)
    df.to_csv("ScrapperTwitterBase.csv", sep=';', encoding='utf-8', index=False)

