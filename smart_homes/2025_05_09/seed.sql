USE smart_home;

-- Insert a building
INSERT INTO buildings (name, address) VALUES 
('Smart City', 'Waagner-Biro-Straße 105, 8020 Graz');

-- Insert tenants
INSERT INTO tenants (name, apartment_number, lease_start, lease_end, building_id) VALUES 
('Alice Brown', 'A-302', '2024-02-01', '2026-02-01', 1),
('Max Mustermann', 'B-104', '2023-08-01', '2025-07-31', 1);

-- Insert rooms
INSERT INTO rooms (room_name, building_id) VALUES 
('Living Room', 1),
('Hallway', 1),
('Terrace', 1);

-- Insert sensors (linking to rooms)
INSERT INTO sensors (sensor_type, installation_date, room_id) VALUES 
('temperature_humidity', '2024-06-01', 1),
('motion_detection', '2024-06-05', 2),
('air_quality', '2024-06-10', 3);


