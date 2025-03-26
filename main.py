import streamlit as st
import pandas as pd
import pyarrow as pa
import sqlite3

# Define as configurações da página
st.set_page_config(
    page_title='Transforme seus arquivos de dados',
    page_icon='♨️',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Alguns estilos
st.markdown(
    """
    <style>
    .st-emotion-cache-1xw8zd0 {
    border: 1px solid rgba(250, 250, 250, 0.2);
    border-radius: 0.5rem;
    padding: calc(1em - 1px);
    background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header('Transforme seus arquivos de dados!')

tab1, tab2 = st.tabs(['Transformar arquivos ⚙️', 'Processar XLSX 🧮'])

with tab1:

    st.write('Faça o upload de um arquivo e visualize uma prévia dos dados. Você também pode editar o nome das colunas e os tipos de dados.')


    # Upload do arquivo
    file = st.file_uploader('Escolha um arquivo', type=['csv', 'xlsx', 'json', 'parquet', 'feather', 'db'])

    if file is not None:
        #if st.button('Executar leitura do arquivo'):
        # Obtem a extensão do arquivo
        extensao = file.name.split('.')[-1]

        # Carregar o arquivo
        try:
            if extensao == 'csv':
                df = pd.read_csv(file)
            
            elif extensao.lower() == 'xlsx':
                df = pd.read_excel(file)
            
            elif extensao == 'json':
                df = pd.read_json(file)
            
            elif extensao == 'parquet':
                df = pd.read_parquet(file)
            
            elif extensao == 'feather':
                df = pd.read_feather(file)
            
            elif extensao == 'db':
                conn = sqlite3.connect(file.name)
                df = pd.read_sql_query('SELECT * FROM dados', conn)
                conn.close()
            
            else:
                st.error(f'Extensão {extensao} inválida!')
                st.stop()


            # Mostrar informações sobre o arquivo

            with st.expander('Informações sobre o arquivo 📄'):
                st.write(f'Quantidade de linhas: {df.shape[0]}')
                st.write(f'Quantidade de colunas: {df.shape[1]}')
                st.write(f'Tipos de dados:')
                st.write(df.describe())

            with st.expander('Visualizar amostra dos dados 👀'):
                st.write(df.head(10))

            # Expander para editar colunas
            with st.expander('Editar colunas ✏️'):
                st.write("Altere o nome das colunas ou seus tipos de dados:")

                # Lista de tipos de dados suportados
                tipos_dados = ['object', 'str', 'int64', 'float64', 'bool', 'datetime64[ns]']

                # Dicionário para armazenar as alterações
                novas_colunas = {}
                novos_tipos = {}

                # Criar uma linha para cada coluna
                for coluna in df.columns:
                    col1, col2 = st.columns(2)

                    with col1:
                        # Campo para editar o nome da coluna
                        novo_nome = st.text_input(f"Nome da coluna '{coluna}'", value=coluna, key=f"nome_{coluna}")
                        novas_colunas[coluna] = novo_nome

                    with col2:
                        # Seletor para alterar o tipo de dado
                        novo_tipo = st.selectbox(
                            f"Tipo de dado para '{coluna}'",
                            options=tipos_dados,
                            index='str' if tipos_dados.index(str(df[coluna].dtype)) == 'object' else tipos_dados.index(str(df[coluna].dtype)),
                            key=f"tipo_{coluna}"
                        )
                        novos_tipos[coluna] = novo_tipo

                # Botão para aplicar as alterações
                if st.button('Aplicar alterações'):
                    # Renomear colunas
                    df.rename(columns=novas_colunas, inplace=True)

                    # Alterar tipos de dados
                    for coluna, tipo in novos_tipos.items():
                        try:
                            df[coluna] = df[coluna].astype(tipo)
                        except Exception as e:
                            st.error(f"Erro ao converter a coluna '{coluna}' para o tipo '{tipo}': {e}")

                    st.success("Alterações aplicadas com sucesso!")

            # Opções de conversão
            col1, col2 = st.columns(2)
            with col1:
                nome_arquivo = st.text_input('Nome do arquivo:', value='arquivo')
            with col2:
                formato_saida = st.selectbox('Escolha o formato de saída:', ['csv', 'xlsx', 'json', 'parquet', 'orc', 'feather', 'sql'])

            if st.button('Converter'):

                if formato_saida == 'csv':
                    st.download_button('Baixar CSV', df.to_csv(index=False).encode('utf-8'), file_name=f'{nome_arquivo}.csv')
                
                elif formato_saida == 'xlsx':
                    with pd.ExcelWriter('arquivo.xlsx', engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)
                    with open('arquivo.xlsx', 'rb') as f:
                        st.download_button('Baixar XLSX', f, file_name=f'{nome_arquivo}.xlsx')
                
                elif formato_saida == 'json':
                    st.download_button('Baixar JSON', df.to_json(orient='records'), file_name=f'{nome_arquivo}.json')
                
                elif formato_saida == 'parquet':
                    df.to_parquet('arquivo.parquet')
                    with open('arquivo.parquet', 'rb') as f:
                        st.download_button('Baixar Parquet', f, file_name=f'{nome_arquivo}.parquet')
                
                elif formato_saida == 'feather':
                    df.to_feather('arquivo.feather')
                    with open('arquivo.feather', 'rb') as f:
                        st.download_button('Baixar Feather', f, file_name=f'{nome_arquivo}.feather')
                
                elif formato_saida == 'sql':
                    conn = sqlite3.connect(f'{nome_arquivo}.db')
                    df.to_sql('dados', conn, if_exists='replace', index=False)
                    conn.close()
                    with open(f'{nome_arquivo}.db', 'rb') as f:
                        st.download_button('Baixar SQL', f, file_name=f'{nome_arquivo}.db')

        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

with tab2:
    st.write('Processar arquivos XLSX')
    st.write('Em breve...')
