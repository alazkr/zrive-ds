import requests
import numpy as np
import matplotlib.pyplot as plt



API_URL = "https://climate-api.open-meteo.com/v1/climate?"

COORDINATES = {
    "Madrid": {"latitude": 40.416775, "longitude": -3.703790},
    "London": {"latitude": 51.507351, "longitude": -0.127758},
    "Rio": {"latitude": -22.906847, "longitude": -43.172896},
}
VARIABLES = "temperature_2m_mean,precipitation_sum,soil_moisture_0_to_10cm_mean"


#primera funcion, recogida de datos
#conceptos clave: definicion de la funcion con argumentos de entrada, diccionario (par clave-valor)

def get_data_meteo_api(city, start_year, end_year):
    params = {
        "latitude": COORDINATES[city]["latitude"],
        "longitude": COORDINATES[city]["longitude"],
        "start": f"{start_year}-01-01",
        "end": f"{end_year}-12-31",
        "models": ["MRI_AGCM3_2_S", "EC_Earth3P_HR"],
        "daily": VARIABLES
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    return data


#cooloff no lo he hecho aun 



#procesamiento de datos
def process_data(data)
    #creo diccionario vacio que contendra datos procesados
    processed_data = {}


    #itero sobre los elementos del diccionario data, city=nombre de la ciudad, city_data = dicc con los datos de cada ciudad
    for city, city_data in data.items():
        #inicializo listas para almacenar datos
        city_temperatures = []
        city_precipitations = []
        city_soil_moistures = []

        for year, year_data in city_data.items():
            city_temperatures.extend(year_data.get("temperature_2m_mean", []))
            city_precipitations.extend(year_data.get("precipitation_sum", []))
            city_soil_moistures.extend(year_data.get("soil_moisture_0_to_10cm_mean", []))

        #uso libreria numpy para calcular cosas
        city_average_temperature = np.mean(city_temperatures)
        city_average_precipitation = np.mean(city_precipitations)
        city_average_soil_moisture = np.mean(city_soil_moistures)

        city_std_temperature = np.std(city_temperatures)
        city_std_precipitation = np.std(city_precipitations)
        city_std_soil_moisture = np.std(city_soil_moistures)
        
        #almaceno en un diccionario
        city_data = {
            "average_temperature": city_average_temperature,
            "std_temperature": city_std_temperature,
            "average_precipitation": city_average_precipitation,
            "std_precipitation": city_std_precipitation,
            "average_soil_moisture": city_average_soil_moisture,
            "std_soil_moisture": city_std_soil_moisture
        }

        processed_data[city] = city_data

    return processed_data


#funcion de plotteo

def plot_data(processed_data):

    #formato del plotteo
    colors = {
        "temperature": "red",
        "precipitation": "blue",
        "soil_moisture": "green"
    }

    #bucle para plottear cada ciudad
    for city, city_data in processed_data.items():
        temperatures = city_data["average_temperature"]
        std_temperatures = city_data["std_temperature"]
        precipitations = city_data["average_precipitation"]
        std_precipitations = city_data["std_precipitation"]
        soil_moistures = city_data["average_soil_moisture"]
        std_soil_moistures = city_data["std_soil_moisture"]

        #temperatura
        plt.errorbar(range(len(temperatures)), temperatures, yerr=std_temperatures, fmt='o', color=colors["temperature"], label="Temperature")
        #precipitacion
        plt.errorbar(range(len(precipitations)), precipitations, yerr=std_precipitations, fmt='o', color=colors["precipitation"], label="Precipitation")
        #humedad
        plt.errorbar(range(len(soil_moistures)), soil_moistures, yerr=std_soil_moistures, fmt='o', color=colors["soil_moisture"], label="Soil Moisture")
        
        #ejes
        plt.xlabel("Years")
        plt.ylabel("Value")
        plt.title(f"Climate Data for {city}")
        plt.legend()
        plt.show()




def main():
    cities = ["Madrid", "London", "Rio"]
    start_year = 1950
    end_year = 2050
    processed_data = {}

    for city in cities:
        data = get_data_meteo_api(city, start_year, end_year)
        processed_data[city] = process_data(data)
    
    plot_data(processed_data)

if __name__ == "__main__":
    main()




