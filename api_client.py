import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv

def get_astrological_chart(birth_date, birth_time, latitude, longitude, timezone):
    url = "https://jyotish-api.onrender.com/api/calculate"
    
    # Parse the date and time
    dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    
    params = {
        "latitude": str(latitude),
        "longitude": str(longitude),
        "year": dt.year,
        "month": dt.month,
        "day": dt.day,
        "hour": dt.hour,
        "min": dt.minute,
        "sec": 0,
        "time_zone": timezone,
        "dst_hour": 0,
        "dst_min": 0,
        "nesting": 0,
        "varga": "D1,D9",
        "infolevel": "basic,panchanga"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Pretty print the JSON response
        formatted_response = json.dumps(response.json(), indent=2, ensure_ascii=False)
        return formatted_response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def save_response_to_file(response_data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        # If response_data is already a string, write directly
        if isinstance(response_data, str):
            file.write(response_data)
        else:
            # If it's still a dict/object, format it
            json.dump(response_data, file, ensure_ascii=False, indent=2)
    print(f"Response saved to {filename}")

def print_planetary_positions(chart_data):
    """Print planetary positions in a readable format"""
    if isinstance(chart_data, str):
        chart_data = json.loads(chart_data)
    
    print("\nPlanetary Positions:")
    print("-" * 50)
    
    # Planet name mappings for better readability
    planet_names = {
        "Sy": "Sun (Surya)",
        "Ch": "Moon (Chandra)",
        "Ma": "Mars (Mangal)",
        "Bu": "Mercury (Buddha)",
        "Gu": "Jupiter (Guru)",
        "Sk": "Venus (Shukra)",
        "Sa": "Saturn (Shani)",
        "Ra": "Rahu",
        "Ke": "Ketu"
    }
    
    # Rashi (zodiac sign) mappings
    rashi_names = {
        1: "Mesha (Aries)",
        2: "Vrishabha (Taurus)",
        3: "Mithuna (Gemini)",
        4: "Karka (Cancer)",
        5: "Simha (Leo)",
        6: "Kanya (Virgo)",
        7: "Tula (Libra)",
        8: "Vrishchika (Scorpio)",
        9: "Dhanu (Sagittarius)",
        10: "Makara (Capricorn)",
        11: "Kumbha (Aquarius)",
        12: "Meena (Pisces)"
    }
    
    for planet_code, data in chart_data['chart']['graha'].items():
        print(f"\n{planet_names.get(planet_code, planet_code)}:")
        print(f"  Longitude: {data.get('longitude', 'N/A')}°")
        rashi_num = data.get('rashi')
        print(f"  Sign (Rashi): {rashi_names.get(rashi_num, f'Rashi {rashi_num}')}")
        if 'nakshatra' in data:
            print(f"  Nakshatra: {data['nakshatra'].get('name', 'N/A')}")
            print(f"  Pada: {data['nakshatra'].get('pada', 'N/A')}")
        if 'speed' in data:
            print(f"  Speed: {data.get('speed', 'N/A')}")
        if 'rashiAvastha' in data:
            print(f"  Dignity: {data.get('rashiAvastha', 'N/A').title()}")

def print_panchanga(chart_data):
    """Print panchanga details in a readable format"""
    if isinstance(chart_data, str):
        chart_data = json.loads(chart_data)
    
    if 'panchanga' in chart_data['chart']:
        print("\nPanchanga Details:")
        print("-" * 50)
        panchanga = chart_data['chart']['panchanga']
        
        # Tithi details
        tithi = panchanga['tithi']
        print(f"Tithi: {tithi.get('name', 'N/A')} ({tithi.get('paksha', 'N/A')} Paksha)")
        print(f"  Remaining: {tithi.get('left', 'N/A')}%")
        
        # Nakshatra details
        nakshatra = panchanga['nakshatra']
        print(f"\nNakshatra: {nakshatra.get('name', 'N/A')}")
        print(f"  Pada: {nakshatra.get('pada', 'N/A')}")
        print(f"  Remaining: {nakshatra.get('left', 'N/A')}%")
        
        # Yoga details
        yoga = panchanga['yoga']
        print(f"\nYoga: {yoga.get('name', 'N/A')}")
        print(f"  Remaining: {yoga.get('left', 'N/A')}%")
        
        # Karana details
        karana = panchanga['karana']
        print(f"\nKarana: {karana.get('name', 'N/A')}")
        print(f"  Remaining: {karana.get('left', 'N/A')}%")
        
        # Vara (weekday) details
        vara = panchanga['vara']
        print(f"\nVara: {vara.get('name', 'N/A')}")

def print_rising_setting_times(chart_data):
    """Print rising and setting times for the Sun"""
    if isinstance(chart_data, str):
        chart_data = json.loads(chart_data)
    
    if 'rising' in chart_data['chart']:
        print("\nRising and Setting Times:")
        print("-" * 50)
        for day in chart_data['chart']['rising']['Sy']:
            print(f"\nDate:")
            print(f"  Sunrise: {day.get('rising', 'N/A')}")
            print(f"  Sunset: {day.get('setting', 'N/A')}")

# Example usage
if __name__ == "__main__":
    birth_date = "1990-01-01"
    birth_time = "12:00"
    latitude = 37.28077
    longitude = 49.583057
    timezone = "Asia/Tehran"
    
    chart = get_astrological_chart(birth_date, birth_time, latitude, longitude, timezone)
    if chart:
        # Save raw JSON
        save_response_to_file(chart, "chart_response.json")
        
        # Print formatted sections
        chart_data = json.loads(chart)
        print_planetary_positions(chart_data)
        print_panchanga(chart_data)
        print_rising_setting_times(chart_data) 