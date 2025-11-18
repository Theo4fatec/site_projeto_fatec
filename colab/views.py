from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from .models import  Teste
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
#from pmdarima import ARIMA
from django.db import connections

def teste(request):
    data = sns.load_dataset("iris")
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x="sepal_length", y="sepal_width", hue="species", data=data)
    plt.title("Iris Sepal Length vs. Width")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    grafico = base64.b64encode(image_png)
    grafico = grafico.decode('utf-8')
    return render(request, 'colab/teste.html', {'grafico':grafico})

# @login_required
# def grafico_banco(request):
#     df = pd.DataFrame(list(Teste.objects.all().values('categoria','quantidade')))
#     sns.barplot(data=df, x = 'categoria', y = 'quantidade')
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     plt.close()
#     image_png = buffer.getvalue()
#     grafico = base64.b64encode(image_png)
#     grafico = grafico.decode('utf-8')
#     return render(request, 'colab/grafico_banco.html', {'grafico':grafico})

@login_required
def grafico_banco(request):
    df = pd.DataFrame(list(Teste.objects.all().values('categoria','quantidade')))
    df["categoria"] = df["categoria"].astype(str)
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
    sns.barplot(data=df, x='categoria', y='quantidade')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    grafico = base64.b64encode(buffer.getvalue()).decode()
    return render(request, 'colab/grafico_banco.html', {'grafico': grafico})

@login_required
def grafico_1(request):
    #Carregar dados do banco
    query = """
        SELECT registro, produto, maquina, oee
        FROM colab_ega_kpis_prod
        WHERE produto = 2027 AND maquina = 23
        ORDER BY registro
    """

    df733 = pd.read_sql(query, connections['default'])
    df733["registro"] = pd.to_datetime(df733["registro"])
    #Calcular intervalos
    df733["intervalo"] = df733["registro"].diff().dt.days
    intervalos = df733["intervalo"].dropna()
    intervalos.index = df733["registro"][1:]
    #ARIMA - previsão do intervalo
    model_int = ARIMA(intervalos, order=(2,1,1))
    fit_int = model_int.fit()
    proximo_intervalo = float(fit_int.forecast(steps=1))

    ultima_data = df733["registro"].max()
    data_prevista = ultima_data + pd.Timedelta(days=proximo_intervalo)
    #Previsão do OEE
    serie_oee = df733.set_index("registro")["oee"]
    model_oee = ARIMA(serie_oee, order=(2,1,1))
    fit_oee = model_oee.fit()
    oee_previsto = float(fit_oee.forecast(steps=1))
    #Criar gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(serie_oee.index, serie_oee, label="oee", color="blue")
    plt.scatter([data_prevista], [oee_previsto], color="red", s=120, label="Previsão do OEE")
    plt.plot([serie_oee.index[-1], data_prevista],
             [serie_oee.iloc[-1], oee_previsto],
             linestyle="--", color="gray")
    plt.title("Previsão do OEE do Produto 2027 na Máquina 23 na próxima execução")
    plt.xlabel("Data")
    plt.ylabel("OEE (%)")
    plt.grid(True)
    plt.legend()

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    grafico_png = base64.b64encode(buffer.getvalue()).decode()
    # Retornar ao template
    return render(request, "colab/grafico_1.html", {
        "grafico": grafico_png,
        "data_prevista": data_prevista,
        "oee_previsto": round(oee_previsto, 2)
    })


##############forma correta

# @login_required
# def grafico_1(request):
#     #Carregar dados do banco
#     query = """
#         SELECT registro, produto, maquina, oee
#         FROM colab_ega_kpis_prod
#         WHERE produto = 2027 AND maquina = 23
#         ORDER BY registro
#     """

#     df733 = pd.read_sql(query, connections['default'])
#     df733["registro"] = pd.to_datetime(df733["registro"])
#     #Calcular intervalos
#     df733["intervalo"] = df733["registro"].diff().dt.days
#     intervalos = df733["intervalo"].dropna()
#     intervalos.index = df733["registro"][1:]
#     #ARIMA - previsão do intervalo
#     model_int = ARIMA(order=(2,1,1))
#     model_int.fit(intervalos)
#     proximo_intervalo = float(model_int.predict(n_periods=1))

#     ultima_data = df733["registro"].max()
#     data_prevista = ultima_data + pd.Timedelta(days=proximo_intervalo)
#     #Previsão do OEE
#     serie_oee = df733.set_index("registro")["oee"]
#     model_oee = ARIMA(order=(2,1,1))
#     model_oee.fit(serie_oee)
#     oee_previsto = float(model_oee.predict(n_periods=1))
#     #Criar gráfico
#     plt.figure(figsize=(12, 6))
#     plt.plot(serie_oee.index, serie_oee, label="oee", color="blue")
#     plt.scatter([data_prevista], [oee_previsto], color="red", s=120, label="Previsão do OEE")
#     plt.plot([serie_oee.index[-1], data_prevista],
#              [serie_oee.iloc[-1], oee_previsto],
#              linestyle="--", color="gray")
#     plt.title("Previsão do OEE do Produto 2027 na Máquina 23 na próxima execução")
#     plt.xlabel("Data")
#     plt.ylabel("OEE (%)")
#     plt.grid(True)
#     plt.legend()

#     buffer = io.BytesIO()
#     plt.tight_layout()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)

#     grafico_png = base64.b64encode(buffer.getvalue()).decode()
#     # Retornar ao template
#     return render(request, "colab/grafico_1.html", {
#         "grafico": grafico_png,
#         "data_prevista": data_prevista,
#         "oee_previsto": round(oee_previsto, 2)
#     })


# @login_required
# def grafico_1(request):
#     #Carregar dados do banco
#     query = """
#         SELECT registro, produto, maquina, oee
#         FROM colab_ega_kpis_prod
#         WHERE produto = 2027 AND maquina = 23
#         ORDER BY registro
#     """

#     df733 = pd.read_sql(query, connections['default'])
#     df733["registro"] = pd.to_datetime(df733["registro"])

#     #Calcular intervalos
#     df733["intervalo"] = df733["registro"].diff().dt.days
#     intervalos = df733["intervalo"].dropna().astype(float)
#     intervalos.index = df733["registro"][1:]

#     #ARIMA - previsão do intervalo
#     model_int = ARIMA(order=(2,1,1))
#     model_int.fit(intervalos)
#     proximo_intervalo = float(model_int.predict(n_periods=1))

#     ultima_data = df733["registro"].max()
#     data_prevista = ultima_data + pd.Timedelta(days=proximo_intervalo)

#     #Previsão do OEE
#     serie_oee = df733.set_index("registro")["oee"].astype(float)

#     model_oee = ARIMA(order=(2,1,1))
#     model_oee.fit(serie_oee)
#     oee_previsto = float(model_oee.predict(n_periods=1))

#     #Criar gráfico
#     plt.figure(figsize=(12, 6))
#     plt.plot(serie_oee.index, serie_oee, label="oee", color="blue")
#     plt.scatter([data_prevista], [oee_previsto], color="red", s=120, label="Previsão do OEE")
#     plt.plot([serie_oee.index[-1], data_prevista],
#              [serie_oee.iloc[-1], oee_previsto],
#              linestyle="--", color="gray")

#     plt.title("Previsão do OEE do Produto 2027 na Máquina 23 na próxima execução")
#     plt.xlabel("Data")
#     plt.ylabel("OEE (%)")
#     plt.grid(True)
#     plt.legend()

#     buffer = io.BytesIO()
#     plt.tight_layout()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)

#     grafico_png = base64.b64encode(buffer.getvalue()).decode()

#     return render(request, "colab/grafico_1.html", {
#         "grafico": grafico_png,
#         "data_prevista": data_prevista,
#         "oee_previsto": round(oee_previsto, 2)
#     })