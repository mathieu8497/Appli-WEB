import serial
import time
import psycopg2
import os

# Retrieve database configuration from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DB = os.getenv('DB_DB')
DB_PORT = '5432'  # Default PostgreSQL port. Change if different.

# Database connection string
DB_CONNECTION = f"dbname='{DB_DB}' user='{DB_USER}' password='{DB_PASSWORD}' host='{DB_HOST}' port='{DB_PORT}'"

# Configuration for serial communication
COM_PORT = 'COM7'  # Update this to your actual COM port
BAUD_RATE = 19200  # Update this to match your device's baud rate

def parse_data(data):
    """Parse the input data and return id_flower, humidity, and temperature."""
    id_flower = int(data[:2])
    humidity = int(data[4:6])
    temperature = int(data[-2:])
    return id_flower, humidity, temperature

def insert_data(id_flower, humidity, temperature):
    """Insert the data into the database."""
    conn = None
    try:
        conn = psycopg2.connect(DB_CONNECTION)
        cur = conn.cursor()
        cur.execute("INSERT INTO measures (id_flower, measure_date, humidity, temperature) VALUES (%s, NOW(), %s, %s)",
                    (id_flower, humidity, temperature))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

try:
    # Initialize serial connection
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {COM_PORT} at {BAUD_RATE} baud rate.")

    # Continuous reading loop
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            print(f"Data received: {data}")
            id_flower, humidity, temperature = parse_data(data)
            insert_data(id_flower, humidity, temperature)
        time.sleep(0.1)  # Small delay to reduce CPU usage

except serial.SerialException as e:
    print(f"Error opening the serial port: {e}")

except KeyboardInterrupt:
    print("\nProgram terminated by user.")

finally:
    if 'ser' in locals() or 'ser' in globals():
        ser.close()
        print("Serial connection closed.")
