from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from .models import  Teste
import pandas as pd
import numpy as np
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
    
    #Carregar dados
    query = """
        SELECT registro, produto, maquina, oee
        FROM colab_ega_kpis_prod
        WHERE produto = 2027 AND maquina = 23
        ORDER BY registro
    """

    df733 = pd.read_sql(query, connections['default'])
    df733["registro"] = pd.to_datetime(df733["registro"])

    #Calcular INTERVALO entre execuções
    df733["intervalo"] = df733["registro"].diff().dt.days
    intervalos = df733["intervalo"].dropna()

    #Criar eixo X como números sequenciais
    x_int = np.arange(len(intervalos))
    y_int = intervalos.values

    #REGRASSÃO LINEAR SIMPLES para prever intervalo
    coef = np.polyfit(x_int, y_int, 1)   # linha: y = ax + b
    a, b = coef

    proximo_intervalo = a * (len(intervalos)) + b

    #Calcular data prevista
    ultima_data = df733["registro"].max()
    data_prevista = ultima_data + pd.Timedelta(days=float(proximo_intervalo))

    #Previsão do OEE também usando regressão linear simples
    serie_oee = df733.set_index("registro")["oee"]

    x_oee = np.arange(len(serie_oee))
    y_oee = serie_oee.values

    coef_oee = np.polyfit(x_oee, y_oee, 1)
    a2, b2 = coef_oee

    oee_previsto = a2 * len(serie_oee) + b2

    #Criar gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(serie_oee.index, serie_oee, label="OEE", color="blue")

    # ponto previsto
    plt.scatter([data_prevista], [oee_previsto], color="red", s=120, label="Previsão do OEE")

    # linha tracejada até previsão
    plt.plot(
        [serie_oee.index[-1], data_prevista],
        [serie_oee.iloc[-1], oee_previsto],
        linestyle="--",
        color="gray"
    )

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

    return render(request, "colab/grafico_1.html", {
        "grafico": grafico_png,
        "data_prevista": data_prevista,
        "oee_previsto": round(float(oee_previsto), 2)
    })


@login_required
def powerbi(request):
    powerbi_link = "https://app.powerbi.com/view?r=eyJrIjoiZjA5OGEyOTktNzU5Yi00YzUxLThmYTItMTQxZGI1ZmY1MWUxIiwidCI6ImNmNzJlMmJkLTdhMmItNDc4My1iZGViLTM5ZDU3YjA3Zjc2ZiIsImMiOjR9"
    return render(request, "colab/powerbi.html", {
        "powerbi_url": powerbi_link
    })

@login_required
def powerbi_2(request):
    powerbi_link_2 = "https://app.powerbi.com/view?r=eyJrIjoiMWE2Y2I5YzMtZWU3My00ODI0LWE5MWQtN2VmMDg4MGIxN2E2IiwidCI6ImNmNzJlMmJkLTdhMmItNDc4My1iZGViLTM5ZDU3YjA3Zjc2ZiIsImMiOjR9"
    return render(request, "colab/powerbi_2.html", {
        "powerbi_url_2": powerbi_link_2
    })

@login_required
def powerbi_3(request):
    powerbi_link_3 = "https://app.powerbi.com/view?r=eyJrIjoiZjA5OGEyOTktNzU5Yi00YzUxLThmYTItMTQxZGI1ZmY1MWUxIiwidCI6ImNmNzJlMmJkLTdhMmItNDc4My1iZGViLTM5ZDU3YjA3Zjc2ZiIsImMiOjR9"
    return render(request, "colab/powerbi_3.html", {
        "powerbi_url_3": powerbi_link_3
    })

@login_required
def powerbi_4(request):
    powerbi_link_4 = "https://app.powerbi.com/view?r=eyJrIjoiZjA5OGEyOTktNzU5Yi00YzUxLThmYTItMTQxZGI1ZmY1MWUxIiwidCI6ImNmNzJlMmJkLTdhMmItNDc4My1iZGViLTM5ZDU3YjA3Zjc2ZiIsImMiOjR9"
    return render(request, "colab/powerbi_4.html", {
        "powerbi_url_4": powerbi_link_4
    })


