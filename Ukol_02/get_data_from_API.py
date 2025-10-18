# Získejte data pomocí veřejné API a zobrazte je pomocí Plotly nebo Seaborn a uložte data do souboru csv.
import requests
import json
import openmeteo_requests
import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests_cache   
from retry_requests import retry  

path_to_saved_csv =  "datasets\weather_data\weather_forecast.csv"

# Ziska verejnou adresu IP:
def get_ip_address(host_name):
    "Získá IP adresu z veřejného API "
    host_name_url = "api.ipify.org"
    try:
        response = requests.get(f"https://{host_name_url}/?format=json")
        if response.status_code == 200:
            data = response.json()
            return data['ip']
        else:
            print(f"Chyba při získávání IP adresy: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Výjimka při požadavku: {e}")
        return None

# Ziska lokaci zemepisnou z verrejne IP adresy z https://ip-api.com/docs:: 
def get_location_data(ip_address: str, format: str) :
    "Získá lokaci IP adresy z veřejného API "
    try:
        response = requests.get(f"http://ip-api.com/{format}/{ip_address}", timeout=5)  
        if response.status_code == 200:
            if format == "json":
                return response.json() # JSON data jako slovník
            elif format == "xml":
                return response.text  # XML data jako text
            elif format == "csv":
                return response.text  # CSV data jako text
        else:
            print(f"Chyba při získávání dat o lokaci: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Výjimka při požadavku: {e}")
        return None

# Ziska zemepisnou sirku a delku z dat o lokaci
def get_lat_lon(location_data: dict) -> tuple[float, float]:
    "Získá zeměpisnou šířku a délku z dat o lokaci"
    if location_data and 'lat' in location_data and 'lon' in location_data:
        return (location_data['lat'], location_data['lon'])
    else:
        print("Chyba: Data o lokaci neobsahují lat/lon.")
        return (None, None) 


# Ziska data o pocasi meteo API pomoci ziskane zemepisne sirky a delky
def get_weather_data(lat: float, lon: float) -> pd.DataFrame:
    "Získá data o počasí z Open-Meteo API"
    if lat is None or lon is None:
        print("Chyba: Neplatná zeměpisná šířka nebo délka.")
        return None
    else:
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "apparent_temperature"],
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
        hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
        hourly_data["precipitation_probability"] = hourly_precipitation_probability
        hourly_data["apparent_temperature"] = hourly_apparent_temperature

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        # print("\nHourly data\n", hourly_dataframe)
        return hourly_dataframe


def main():
    print("Získávání IP adresy pomocí veřejného API...")

    #Ziskej verejnou IP adresu
    ip_address = get_ip_address("api.ipify.org")
    if ip_address:
        print(f"Veřejná IP adresa: {ip_address}")

        # Ziskej lokaci IP adresy ve formatu JSON a z nej ziskej zemepisnou sirku a delku
        location_data_json = get_location_data(ip_address, "json")
        if location_data_json:
            print("Data o lokaci (JSON):")
            print(json.dumps(location_data_json, indent=4))
            lat, lon = get_lat_lon(location_data_json)
            print(f"Zeměpisná šířka: {lat}, Zeměpisná délka: {lon}")
            predpoved = get_weather_data(lat, lon)
        else:
            print("Nepodařilo se získat data o lokaci.")
    else:
        print("Nepodařilo se získat veřejnou IP adresu.")
    
    # Uloz data do CSV souboru
    if predpoved is not None:
        predpoved.to_csv(path_to_saved_csv, index=False)
        print("Data o počasí byla uložena do souboru weather_forecast.csv")
    
    # Vykresli data pomoci Plotly
    if predpoved is not None:
        # Vytvoření figure se 4 řádky (sdílená osa X)
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            subplot_titles=("Teplota vs Pocitová teplota", "Relativní vlhkost", "Pravděpodobnost deště"),
            vertical_spacing=0.07
        )

        # 1. Teplota
        fig.add_trace(go.Scatter(
            x=predpoved['date'], y=predpoved['temperature_2m'],
            mode='lines', name='Teplota (°C)', line=dict(color='red')
        ), row=1, col=1)

        # 1. Pocitová teplota
        fig.add_trace(go.Scatter(
            x=predpoved['date'], y=predpoved['apparent_temperature'],
            mode='lines', name='Pocitová teplota (°C)', line=dict(color='orange')
        ), row=1, col=1)

        # 2. Relativní vlhkost
        fig.add_trace(go.Scatter(
            x=predpoved['date'], y=predpoved['relative_humidity_2m'],
            mode='lines', name='Relativní vlhkost (%)', line=dict(color='blue')
        ), row=2, col=1)

        # 3. Pravděpodobnost deště
        fig.add_trace(go.Scatter(
            x=predpoved['date'], y=predpoved['precipitation_probability'],
            mode='lines', name='Pravděpodobnost deště (%)', line=dict(color='green')
        ), row=3, col=1)

        # Layout
        fig.update_layout(
            title={'text': 'Předpověď počasí na 7 dní', 'x': 0.5, 'xanchor': 'center'},
            height=900,
            template='plotly_dark',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5
            )
        )

        # Popisky os
        fig.update_yaxes(title_text="°C", row=1, col=1)
        fig.update_yaxes(title_text="%", row=2, col=1)
        fig.update_yaxes(title_text="%", row=3, col=1)
        fig.update_xaxes(title_text="Datum a čas", row=3, col=1)

        # Zobrazit graf
        fig.show()
        fig.write_html("predpoved_pocasi.html")   # interaktivní graf

    else:
        print("Data o počasí nejsou k dispozici pro zobrazení.")


if __name__ == "__main__":
    main()
