import requests # Fazemos chamadas http para APIs
import streamlit as st
import matplotlib.pyplot as plt
import datetime
from config import config # Importamos a classe Config com a chave

API_KEY = config.get_api_key()
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

st.title("Clima")
st.write("Consumimos a API do OpenWeather para a previsao na cidade.")

cidade = st.text_input("Digite o nome da cidade: ")
estado = st.text_input("Digite o nome do seu estado: ")
pais = st.text_input("Digite a sigla do seu pais: ")

if cidade and pais:
    q = f'{cidade}, {estado}, {pais}' if estado else f'{cidade}, {pais}'
    geo_params = {
        "q": q,
        "limit": 1,
        "appid": API_KEY
    }

    geo_response = requests.get("http://api.openweathermap.org/geo/1.0/direct", params=geo_params)

    if geo_response.status_code == 200 and len(geo_response.json()) > 0:
        location = geo_response.json()[0]
        lat = location['lat']
        lon = location['lon']

    forecast_params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt"
    }

    forecast_reponse = requests.get(BASE_URL, params=forecast_params)

    if forecast_reponse.status_code == 200:
        forecast_data = forecast_reponse.json()

        st.subheader(f"Previsao para {cidade}, {estado}, {pais}")
        st.write(f"🌡️ Temperatura atual: {forecast_data['list'][0]['main']['temp']}°C")
        st.write(f"☁️ Clima: {forecast_data['list'][0]['weather'][0]['description'].capitalize()}")

        # Gráfico de temperatura nas próximas 24h (8 previsões de 3h)
        horas = []
        temps = []
        for item in forecast_data['list'][:8]:
            hora = datetime.datetime.fromtimestamp(item['dt'])
            temp = item['main']['temp']
            horas.append(hora)
            temps.append(temp)

        fig, ax = plt.subplots()
        ax.plot(horas, temps, marker="o")
        ax.set_title("Temperatura nas próximas 24h")
        ax.set_xlabel("Hora")
        ax.set_ylabel("°C")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.error("Erro ao buscar a previsão de clima.")
else:
    st.error("Cidade/Estado/País não encontrados.")
