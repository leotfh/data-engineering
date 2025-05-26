USE smart_home;

-- Buildings Table (Stores building/apartment details)
CREATE TABLE buildings (
    building_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255)
);

-- Tenants Table (People who live in the building)
CREATE TABLE tenants (
    tenant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    apartment_number VARCHAR(10),
    lease_start DATE,
    lease_end DATE,
    building_id INT,
    FOREIGN KEY (building_id) REFERENCES buildings(building_id) ON DELETE CASCADE
);

-- Rooms Table (Where sensors are located)
CREATE TABLE rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(50),
    building_id INT,
    FOREIGN KEY (building_id) REFERENCES buildings(building_id) ON DELETE CASCADE
);

-- Sensors Table (Each sensor device and its location)
CREATE TABLE sensors (
    sensor_id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_type ENUM('temperature_humidity', 'motion_detection', 'air_quality'),
    installation_date DATE,
    room_id INT,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE
);

-- Temperature and Humidity Readings Table
CREATE TABLE temperature_humidity_readings (
    reading_id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT,
    timestamp DATETIME,
    temperature FLOAT,
    temperature_f FLOAT,
    humidity FLOAT,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id) ON DELETE CASCADE
);

-- Motion Sensor Readings Table
CREATE TABLE motion_detection_readings (
    reading_id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT,
    timestamp DATETIME,
    motion_detected BOOLEAN,
    day_of_week VARCHAR(20),
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id) ON DELETE CASCADE
);

-- Air Quality Readings Table
CREATE TABLE air_quality_readings (
    reading_id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT,
    timestamp DATETIME,
    pm2_5 FLOAT,
    pm10 FLOAT,
    so2 FLOAT,
    no2 FLOAT,
    health_environment VARCHAR(50),
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id) ON DELETE CASCADE
);

-- Grant read and write permissions to user 'student' on 'smart_home' database
GRANT SELECT, INSERT, UPDATE, DELETE
ON smart_home.*
TO 'student'@'%';

FLUSH PRIVILEGES;