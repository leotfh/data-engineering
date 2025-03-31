import json

# Define the date
date = [{
    "sensor_id" : 2,
    "timestamp" : "2025-02-22T21:11:33.121623",
    "motion_detected" : True,
    "location": {
        "building": "Building 1",
        "floor": 3,
        "room": "Apartment 1"
    },
    "temperature": 24.5,
    "gps_coordinates": {
        "latitude": 40.7128,
        "longitude": -74.0060
    }
},
{
    "sensor_id" : 2,
    "timestamp" : "2025-02-22T21:11:33.121623",
    "motion_detected" : True,
    "temperature": 23.8,
    "gps_coordinates": {
        "latitude": 40.7128,
        "longitude": -74.0060
    }
},
{
    "test": 1,
    "gps_coordinates": {
        "latitude": 40.7128,
        "longitude": -74.0060
    }
}]

# Specify the filename 
filename = "test_json.json"

# Open the file in write mode
with open(filename, "w") as json_file:
    # Write the data to the file
    json.dump(date, json_file, indent=4)

# close the file
json_file.close()

print(f'JSON data written to {filename}')