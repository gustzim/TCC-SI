import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from wordcloud import WordCloud, STOPWORDS

#Links importantes: https://rknagao.medium.com/streamlit-101-o-b%C3%A1sico-para-colocar-seu-projeto-no-ar-38a71bd641eb
#https://www.youtube.com/watch?v=iJWUynPVAIE&t=750s

visao = False


#Importa base de sentimentos analisadas
#data = pd.read_csv(file, low_memory=False, sep=';')


#Cria barra lateral
with st.sidebar:
    st.image('https://imagensemoldes.com.br/wp-content/uploads/2020/07/%C3%8Dcone-Olho-PNG-1280x720.png',width=70)
    st.text(" \n")
    st.header('Analise de dados \n Solutions Sentiments')
    st.text(" \n")
    st.text(" \n")
    st.text(" \n")
    st.header('.\nProjeto para TCC realizado por alunos do 8° semestre de Sistemas de Informação - ANO 2022')
    st.text(" \n")
    st.text(" \n")
    with st.expander("Carregar Arquivo CSV"):
        file = st.file_uploader("Insira Aqui o CSV", type='CSV')

        if file is not None:
            # To read file as bytes:
            bytes_data = file.getvalue()

            # To convert to a string based IO:
            stringio = StringIO(file.getvalue().decode("utf-8"))

            # To read file as string:
            string_data = stringio.read()

            # Can be used wherever a "file-like" object is accepted:
            data = pd.read_csv(file, low_memory=False, sep=';')
            visao = True
    st.text(" \n")
    st.text(" \n")
    st.text(" \n")
    st.text(" \n")
    st.image('https://logodownload.org/wp-content/uploads/2021/06/unip-logo.png', width=150)



if visao == True:
    #Separa indicadores por abas
    tab1, tab4, tab3, tab5, tab6 = st.tabs(["Classificações","Nuvem de Plavras", "Top Hates / Likes", "Tabela Analitica" , "Baixar base analitica"])

    # Ordena Comentarios por maiores rates positivos
    data_mask = data['Class_final'] == "Positivo"
    pos_df = data[data_mask]
    pos_df = pos_df.sort_values(by=['Percent_Media_final'], ascending=False)
    pos_df = pos_df.reset_index()
    pos_df.drop('index', axis=1, inplace=True)

    # Ordena Comentarios por maiores rates Negativos
    data_mask = data['Class_final'] == "Negativo"
    neg_df = data[data_mask]
    neg_df = neg_df.sort_values(by=['Percent_Media_final'], ascending=True)
    neg_df = neg_df.reset_index()
    neg_df.drop('index', axis=1, inplace=True)

    #Aba 1: total de comentarios negativos, positivos e neutros
    with tab1:
        data_Count = data.groupby('Class_final')['Percent_Media_final'].count()
        st.title("Classificação de comentários:")
        st.markdown("Os comentarios foram analisados utilizando **3 Analises de Sentimentos**")
        st.text("O resultado foi calculado com base nas 3 avaliações.")

        st.markdown("Total de comentarios analisados : **"+str(data['Class_final'].count())+"**")

        plt.barh(data_Count.index,data_Count, color = "gray")
        for index, value in enumerate(data_Count):
            plt.text(value, index,
                     str(value))
        plt.title('Classificação de Sentimentos por Comentario')
        plt.show()
        st.pyplot(plt)

    #Top Comentarios Positivos e Negativos
    with tab3:
        st.title("Top 3 Comentarios Positivos")
        st.markdown('**- Top 1:**')
        st.markdown('Nickname: **'+pos_df.iat[0, 1]+"** Data de Publicação: **"+pos_df.iat[0, 2]+"**")
        st.markdown("Rate da classificação: **{:.2%}".format(pos_df.iat[0, 18])+"**")
        st.markdown("**Tweet:** "+pos_df.iat[0, 3])
        st.markdown("**Quantidade de Likes:** "+str(pos_df.iat[0, 5])+" **Quantidade de Retweets:** "+str(pos_df.iat[0, 6])+
                    " **Quantidade de Comentarios:** "+ str(+pos_df.iat[0, 4]))
        st.text("______________________________________________________________________")

        st.markdown('**- Top 2:**')
        st.markdown('Nickname: **'+pos_df.iat[1, 1]+"** Data de Publicação: **"+pos_df.iat[1, 2]+"**")
        st.markdown("Rate da classificação: **{:.2%}".format(pos_df.iat[1, 18])+"**")
        st.markdown("**Tweet:** "+pos_df.iat[1, 3])
        st.markdown("**Quantidade de Likes:** "+str(pos_df.iat[1, 5])+" **Quantidade de Retweets:** "+str(pos_df.iat[1, 6])+
                    " **Quantidade de Comentarios:** "+ str(+pos_df.iat[1, 4]))
        st.text("______________________________________________________________________")

        st.markdown('**- Top 3:**')
        st.markdown('Nickname: **'+pos_df.iat[2, 1]+"** Data de Publicação: **"+pos_df.iat[2, 2]+"**")
        st.markdown("Rate da classificação: **{:.2%}".format(pos_df.iat[2, 18])+"**")
        st.markdown("**Tweet:** "+pos_df.iat[2, 3])
        st.markdown("**Quantidade de Likes:** "+str(pos_df.iat[2, 5])+" **Quantidade de Retweets:** "+str(pos_df.iat[2, 6])+
                    " **Quantidade de Comentarios:** "+ str(+pos_df.iat[2, 4]))
        st.text("______________________________________________________________________")

        st.title("Top 3 Comentarios Negativos")
        st.markdown('**- Top 1:**')
        st.markdown('Nickname: **'+neg_df.iat[0, 1]+"** Data de Publicação: **"+neg_df.iat[0, 2]+"**")
        st.markdown("Rate da classificação: **{:.2%}".format(neg_df.iat[0, 18])+"**")
        st.markdown("**Tweet:** "+neg_df.iat[0, 3])
        st.markdown("**Quantidade de Likes:** "+str(neg_df.iat[0, 5])+" **Quantidade de Retweets:** "+str(neg_df.iat[0, 6])+
                    " **Quantidade de Comentarios:** "+ str(+neg_df.iat[0, 4]))
        st.text("______________________________________________________________________")
        st.markdown('**- Top 2:**')
        st.markdown('Nickname: **'+neg_df.iat[1, 1]+"** Data de Publicação: **"+neg_df.iat[1, 2]+"**")
        st.markdown("Rate da classificação: **{:.2%}".format(neg_df.iat[1, 18])+"**")
        st.markdown("**Tweet:** "+neg_df.iat[1, 3])
        st.markdown("**Quantidade de Likes:** "+str(neg_df.iat[1, 5])+" **Quantidade de Retweets:** "+str(neg_df.iat[1, 6])+
                    " **Quantidade de Comentarios:** "+ str(+neg_df.iat[1, 4]))
        st.text("______________________________________________________________________")

        st.markdown('**- Top 3:**')
        st.markdown('Nickname: **'+neg_df.iat[2, 1]+"** Data de Publicação: **"+neg_df.iat[2, 2]+"**")
        st.markdown("Rate da classificação: **{:.2%}".format(neg_df.iat[2, 18])+"**")
        st.markdown("**Tweet:** "+neg_df.iat[2, 3])
        st.markdown("**Quantidade de Likes:** "+str(neg_df.iat[2, 5])+" **Quantidade de Retweets:** "+str(neg_df.iat[2, 6])+
                    " **Quantidade de Comentarios:** "+ str(+neg_df.iat[2, 4]))

    #Nuvem de palavras dos comentarios do twitter
    with tab4:
        st.title("Nuvem de Palavras dos tweets")
        st.markdown("Exibe as palavras com maior frequencia dentro dos tweets extraidos")
        #Retira textos nulos
        summary = data.dropna(subset=['Texto'], axis=0)['Texto']
        # concatenar as palavras
        all_summary = " ".join(s for s in summary)
        # lista de stopword
        stopwords = set(STOPWORDS)
        #Retira stopword... Exemplo: que, não, mas , é, no...
        stopwords.update(
            ['tá', 'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os', 'no', 'se',
             'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou',
             'ser', 'quando','muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela',
             'entre', 'era','depois', 'sem','mesmo', 'aos', 'ter', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'estão',
             'você', 'tinha', 'foram', 'essa', 'num', 'nem','suas', 'meu', 'às', 'minha', 'têm', 'numa', 'pelos', 'elas',
             'havia', 'seja', 'qual', 'será', 'nós', 'tenho','lhe', 'deles','essas', 'esses', 'pelas', 'este', 'fosse',
             'dele', 'tu', 'te', 'vocês', 'vos', 'lhes', 'meus', 'minhas','teu', 'tua', 'teus','tuas', 'nosso', 'nossa',
             'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela','aqueles','aquelas', 'isto',
             'aquilo', 'estou', 'está', 'estamos', 'estão', 'estive', 'esteve', 'estivemos', 'estiveram','estava',
             'estávamos', 'estavam', 'estivera', 'estivéramos', 'esteja', 'estejamos', 'estejam', 'estivesse',
             'estivéssemos', 'estivessem','estiver', 'estivermos', 'estiverem', 'hei', 'há', 'havemos', 'hão', 'houve',
             'houvemos', 'houveram','houvera', 'houvéramos','haja', 'hajamos', 'hajam', 'houvesse', 'houvéssemos',
             'houvessem', 'houver', 'houvermos', 'houverem','houverei', 'houverá','houveremos', 'houverão', 'houveria',
             'houveríamos', 'houveriam', 'sou', 'somos', 'são', 'era', 'éramos','eram', 'fui','foi', 'fomos', 'foram',
             'fora', 'fôramos', 'seja', 'sejamos', 'sejam', 'fosse', 'fôssemos', 'fossem', 'for','formos', 'forem', 'serei',
             'será', 'seremos', 'serão', 'seria', 'seríamos', 'seriam', 'tenho', 'tem', 'temos','tém', 'tinha',
             'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 'tiveram', 'tivera', 'tivéramos', 'tenha', 'tenhamos',
             'tenham', 'tivesse','tivéssemos', 'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei', 'terá', 'teremos','q',
             'terão', 'teria','teríamos', 'teriam', 'pra','muita','nao'])
        # gerar uma wordcloud
        wordcloud = WordCloud(stopwords=stopwords,
                              background_color="white",
                              width=1600, height=1000).generate(all_summary)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_axis_off()
        plt.imshow(wordcloud)
        st.pyplot(plt)

    #Tabela analitica
    with tab5:
        st.title("Tabela de dados extraidos do Twitter")
        st.markdown("Os dados abaixo apresentam os **Tweets** extraidos da rede social, contendo informações como:")
        st.markdown("- Nome de conta , nome de perfil , Data de publicação , texto publicado , quantidade de likes ,"
                    " retweets e quantidade de comentarios em sua publicação")
        st.markdown("Tambem é exibido as porcentagens do comentario ser Negativo e Positivo de cada analise de sentimento"
                    "inclusa, bem como o resultado final gerado a partir de um calculo matematico")
        st.dataframe(data)

    #Baixar base analitica
    with tab6:
        st.title("Base de dados extraida do Twitter")
        st.text("Clique no botão para baixar a base e visualizar os comentarios")
        st.text("extraidos em nossa solução")
        st.text("")
        st.markdown("**OBS:** arquivo em formato CSV, separado por Ponto e Virgula ( ; )")
        st.text("")
        def convert_df(df):
            return df.to_csv(sep=";").encode('utf-8')


        csv = convert_df(data)

        st.download_button(
            "Clique para Baixar",
            csv,
            "TCC_AnaliseSentimentos_Base.csv",
            "text/csv",
            key='download-csv'
        )
