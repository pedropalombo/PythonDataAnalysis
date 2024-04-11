import pandas as pd #importing pandas to Python
import plotly.express as px #importing Ploty Express (for the graphs)

# \ If you want to see the dataframe, just type its name after its creation /

#  || Getting each tab from excel into a dataframe ||
# ==| Principal |==
df_principal = pd.read_excel("/content/Imersão Python - Aula 1 + 2 [Cópia].xlsx", sheet_name="Principal")
df_principal.head(10) #getting the first 10 lines of a dataframe | 'df_principal' prints the entire dataframe


# ==| Total_de_acoes |==
df_total_acoes = pd.read_excel("/content/Imersão Python - Aula 1 + 2 [Cópia].xlsx", sheet_name="Total_de_acoes")
#df_total_acoes #printing the entire dataframe


# ==| Ticker |==
df_ticker = pd.read_excel("/content/Imersão Python - Aula 1 + 2 [Cópia].xlsx", sheet_name="Ticker")
#df_ticker #printing the entire dataframe


# ==| GPT |==
df_chat_gpt = pd.read_excel("/content/Imersão Python - Aula 1 + 2 [Cópia].xlsx", sheet_name="GPT")
#df_chat_gpt #printing the entire dataframe

# || / ||


#getting specific columns from dataframe | 'copy()' destroys original dataframe and create a new one
df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy()


#changing columns names
df_principal = df_principal.rename(columns={'Último (R$)': 'valor_final', 'Var. Dia (%)': 'var_dia_pct'}).copy()


#creating new column
df_principal['var_pct'] = df_principal['var_dia_pct']/100


#creating columns and using basic math to set the values
df_principal['valor_inicial'] = df_principal['valor_final']/ (df_principal['var_pct'] + 1)


#blueprint: dataFrame.merge(dataFrameToBeMerged, left_on="column from 'dataFrame'", right_on="column from 'dataFrameToBeMerged'", how="type of join")
df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Código', how='left') #going through dataframes' array [aka VLOOKUP] | Left Outer Join

#removing column from dataframe
df_principal = df_principal.drop(columns=['Código'])


#creating another column
df_principal['variacao_rs'] = (df_principal['valor_final'] - df_principal['valor_inicial']) * df_principal['Qtde. Teórica']


#formating dataframe to show all float values up until 2 digits
pd.options.display.float_format = "{:.2f}".format

#formating column to 'int' type
df_principal["Qtde. Teórica"] = df_principal["Qtde. Teórica"].astype(int)


#renaming column to standard format
df_principal = df_principal.rename(columns={"Qtde. Teórica": "qtd_teorica"}).copy()


#creating new column & applying data based on values | got from ChatGPT
# \-> PS: 'lambda' == foreach()
# \-> PSS: apply() is used to trigger arrow/lambda functions
df_principal['Resultado'] = df_principal['variacao_rs'].apply(lambda x: 'Subiu' if x > 0 else ('Neutro' if x == 0 else 'Desceu'))


#merging "Ticker" table into "Principal" ...
df_principal = df_principal.merge(df_ticker, left_on="Ativo", right_on="Ticker", how="left")

#... and dropping "Ticker" column, so only "Nome" stays
df_principal = df_principal.drop(columns=["Ticker"])



#merging "GPT" into "Nome da Empresa" ...
df_principal = df_principal.merge(df_chat_gpt, left_on="Nome", right_on="Nome da Empresa", how="left")

#... and dropping "Nome da Empresa" column
df_principal = df_principal.drop(columns=['Nome da Empresa'])



#changing column name
df_principal = df_principal.rename(columns={"Idade (anos)": "idade"}).copy()


# ' '
df_principal = df_principal.rename(columns={'idade': "Idade"}).copy()



# --/ made with GPT /--
#creating new column based on existing one
df_principal['Status'] = df_principal['Idade'].apply(lambda x: 'Centenária' if x > 100 else ('Mais de meio século' if x > 50 else 'Menos de 50'))


# --/ made with GPT /--
# Finding max value for column "variacao_rs"
maior = df_principal['variacao_rs'].max()

# Finding the minimun value ' '
menor = df_principal['variacao_rs'].min()

# Calculating the average of values for "variacao_rs"'s column
media = df_principal['variacao_rs'].mean()

# ' ' for the positive values of "variacao_rs"
media_positiva = df_principal[df_principal['variacao_rs'] > 0]['variacao_rs'].mean()

# ' ' for the negative values of "variacao_rs"
media_negativa = df_principal[df_principal['variacao_rs'] < 0]['variacao_rs'].mean()

# Printing results
print("Maior\t", "R$ {:,.2f}".format(maior))  # Max value formatted as currency
print("Menor\t", "R$ {:,.2f}".format(menor))  # Min value ' '
print("Média\t", "R$ {:,.2f}".format(media))  # Average value ''
print("Média Total Positiva\t", "R$ {:,.2f}".format(media_positiva))  # Average for positives ' '
print("Média Total Negativa\t", "R$ {:,.2f}".format(media_negativa))  # ' ' negatives ' '

# --/ | /--


#creating new dataframe based on only "Subiu" values
df_principal_subiu = df_principal[df_principal['Resultado'] == "Subiu"]


#creating new dataframe for uniquely group segments
# \-> PS: sum() would create a vector, but reset_index() forces it to stay as a dataframe
#blueprint: new_dataframe = dataFrame.groupby("first column")["column to be attached"].sum() |-> sum() joins every instance into a single summed-up row
df_analise_segmento = df_principal_subiu.groupby("Segmento")["variacao_rs"].sum().reset_index()

# ' '
df_analise_saldo = df_principal.groupby("Resultado")["variacao_rs"].sum().reset_index()


#generating bar graphs through Plotly
# graph = px.bar(dataFrame, x="column to be horizontal", y="column to be vertical", text="text input on 'y'", title="graph title")
fig = px.bar(df_analise_saldo, x="Resultado", y="variacao_rs", text="variacao_rs", title="Variacao Reais por Resultado")
fig.show() #printing graphs