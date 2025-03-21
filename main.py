import streamlit as st
import pandas as pd

st.title('Transforme seus arquivos de dados com Streamlit')

st.write('Selecione um arquivo')

# Escolher a extensão da origem
extensao = st.radio('Qual a extensão do arquivo?', ['csv', 'xlsx', 'json'])

# Upload do arquivo
file = st.file_uploader(f'Escolha um arquivo {extensao.upper()}', type=extensao)

if file is not None:
    # Carregar o arquivo
    if extensao == 'csv':
        df = pd.read_csv(file)
    elif extensao == 'xlsx':
        df = pd.read_excel(file)
    else:
        df = pd.read_json(file)
    
    st.write(f'Quantidade de linhas: {df.shape[0]}')
    st.write(f'Quantidade de colunas: {df.shape[1]}')

    # Expander para editar colunas
    with st.expander('Editar colunas'):
        st.write("Altere o nome das colunas ou seus tipos de dados:")
        
        # Lista de tipos de dados suportados
        tipos_dados = ['object', 'int64', 'float64', 'bool', 'datetime64[ns]']

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
                    index=tipos_dados.index(str(df[coluna].dtype)),
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

    # Exibir uma prévia dos dados
    st.write("Prévia dos dados:")
    st.write(df.head())