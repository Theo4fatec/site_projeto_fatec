from django.shortcuts import render
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from .models import  Teste
import pandas as pd

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


def grafico_banco(request):
    df = pd.DataFrame(list(Teste.objects.all().values('categoria','quantidade')))
    sns.barplot(data=df, x = 'categoria', y = 'quantidade')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    grafico = base64.b64encode(image_png)
    grafico = grafico.decode('utf-8')
    return render(request, 'colab/grafico_banco.html', {'grafico':grafico})