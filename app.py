from flask import Flask, request, jsonify
import cohere
from flask_cors import CORS
import os

app = Flask(__name__)

# Setup CORS to allow localhost and Vercel domains
CORS(app, origins=["http://localhost:5173"])

# Initialize Cohere client
api_key = "KRQgPTqXpE3pgOs89dY82DX4eEgdb4D75YWi8qYW"  # It's better to store API keys securely, not hard-coded
co = cohere.Client(api_key)

@app.route('/get_farming_alert', methods=['POST'])
def get_farming_alert():
    data = request.json  # Expecting a JSON payload with weather and crop data

    # Extracting weather data and crop details from the input
    weather = data.get("weather", {})
    crop_details = data.get("crop_details", {})
    
    # Handle missing keys gracefully
    temperature = weather.get('temperature', 'N/A')
    precipitation = weather.get('precipitation', 'N/A')
    pressure = weather.get('pressure', 'N/A')
    wind_speed = weather.get('wind_speed', 'N/A')  # Use a default value if missing
    
    # If any crucial crop detail is missing, return an error
    if not crop_details.get('crop_name') or not crop_details.get('growth_stage'):
        return jsonify({"error": "Missing crop details. Please provide crop name and growth stage."}), 400

    # Prepare the prompt for the Cohere model
    prompt = f"""
    The current weather details are:
    Temperature: {temperature}°C
    Precipitation: {precipitation} mm
    Pressure: {pressure} hPa
    Wind Speed: {wind_speed} km/h

    The current crop is: {crop_details['crop_name']}, at stage {crop_details['growth_stage']}.
    
    Based on these factors, generate short and actionable farming alerts to minimize risk, 
    including sowing, harvesting tips, and weather-related warnings.
    """

    # Calling Cohere API to generate farming recommendations
    response = co.generate(
        model="command",  # Using the "command" model for actionable recommendations
        prompt=prompt,
        max_tokens=150,  # Limit output length for crisp points
        temperature=0.5  # Ensure the response is direct and factual
    )

    # Extract the generated text from Cohere's response
    farming_alerts = response.generations[0].text.strip()

    return jsonify({"alerts": farming_alerts})

if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, request, jsonify
# import cohere
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Initialize Cohere client
# api_key = "KRQgPTqXpE3pgOs89dY82DX4eEgdb4D75YWi8qYW"
# co = cohere.Client(api_key)


# @app.route('/get_farming_alert', methods=['POST'])
# def get_farming_alert():
#     data = request.json  # Expecting a JSON payload with weather and crop data

#     # Extracting weather data and crop details from the input
#     weather = data.get("weather", {})
#     crop_details = data.get("crop_details", {})
    
#     # Handle missing keys gracefully
#     temperature = weather.get('temperature', 'N/A')
#     precipitation = weather.get('precipitation', 'N/A')
#     pressure = weather.get('pressure', 'N/A')
#     wind_speed = weather.get('wind_speed', 'N/A')  # Use a default value if missing
    
#     # If any crucial crop detail is missing, return an error
#     if not crop_details.get('crop_name') or not crop_details.get('growth_stage'):
#         return jsonify({"error": "Missing crop details. Please provide crop name and growth stage."}), 400

#     # Prepare the prompt for the Cohere model
#     prompt = f"""
#     The current weather details are:
#     Temperature: {temperature}°C
#     Precipitation: {precipitation} mm
#     Pressure: {pressure} hPa
#     Wind Speed: {wind_speed} km/h

#     The current crop is: {crop_details['crop_name']}, at stage {crop_details['growth_stage']}.
    
#     Based on these factors, generate short and actionable farming alerts to minimize risk, 
#     including sowing, harvesting tips, and weather-related warnings.
#     """

#     # Calling Cohere API to generate farming recommendations
#     response = co.generate(
#         model="command",  # Using the "command" model for actionable recommendations
#         prompt=prompt,
#         max_tokens=150,  # Limit output length for crisp points
#         temperature=0.5  # Ensure the response is direct and factual
#     )

#     # Extract the generated text from Cohere's response
#     farming_alerts = response.generations[0].text.strip()

#     return jsonify({"alerts": farming_alerts})

# if __name__ == '__main__':
#     app.run(debug=True)
