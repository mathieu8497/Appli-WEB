import serial
import time
import psycopg2
import os
import logging

# Set up logging
logging.basicConfig(filename='data_insertion.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
    try:
        id_flower = int(data[:2])
        humidity = int(data[4:6])
        temperature = int(data[-2:])
        return id_flower, humidity, temperature
    except ValueError as e:
        logging.error(f"Error parsing data: {data}", exc_info=True)
        raise

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
        logging.info(f"Inserted: Flower ID {id_flower}, Humidity {humidity}, Temperature {temperature}")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error inserting data: {error}", exc_info=True)
    finally:
        if conn is not None:
            conn.close()

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    logging.info(f"Connected to {COM_PORT} at {BAUD_RATE} baud rate.")

    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            logging.info(f"Raw data received: {data}")  # Log raw data received
            try:
                id_flower, humidity, temperature = parse_data(data)
                insert_data(id_flower, humidity, temperature)
            except Exception as e:
                logging.error(f"Error processing data: {data}", exc_info=True)
        time.sleep(0.1)  # Small delay to reduce CPU usage

except serial.SerialException as e:
    logging.error(f"Error opening the serial port: {e}")

except KeyboardInterrupt:
    logging.info("Program terminated by user.")

finally:
    if 'ser' in locals() or 'ser' in globals():
        ser.close()
        logging.info("Serial connection closed.")
