import xml.etree.ElementTree as ET
from xml.dom import minidom

# Create the root element
root = ET.Element("root")

# Define data
readings_data = [
    {"sensor_id": "3", "timestamp": "2021-01-01T00:00:00", "pm2_5": "10", "pm10": "20", "so2": "30", "no2": "40"},
    {"sensor_id": "3", "timestamp": "2021-01-01T00:00:00", "pm2_5": "10", "pm10": "20", "so2": "30", "no2": "40"}
]

# Populate the root element with data
for reading in readings_data:
    reading_element = ET.SubElement(root, "Reading")
    for key, value in reading.items():
        child = ET.SubElement(reading_element, key)
        child.text = value

# Convert the element tree to a string
xml_str = ET.tostring(root, encoding="unicode")

# Use minidom to prettify the XML string
pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent= " ")

filename = "test.xml"
with open(filename, "w") as f:
    f.write(pretty_xml_str)

print(f"XML data written to {filename}")