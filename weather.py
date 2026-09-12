import requests

def get_weather(city: str) -> dict:
    geo_response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name":city, "count": 1}
    )
    geo_data = geo_response.json()

    first_result = geo_data["results"][0]
    lat = first_result["latitude"]
    lon = first_result["longitude"]
    location_name = first_result["name"]


    forecast = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "auto",
        }
    ).json()

    current = forecast["current"]
    daily = forecast["daily"]

    return {
        "city": location_name,
        "current_temp_f": current["temperature_2m"],
        "condition_code": current["weather_code"],
        "wind_mph": current["wind_speed_10m"],
        "high_f": daily["temperature_2m_max"][0],
        "low_f": daily["temperature_2m_min"][0],
        "precip_chance": daily["precipitation_probability_max"][0],
    }

if __name__ == "__main__":
    print(get_weather("Atlanta, GA"))