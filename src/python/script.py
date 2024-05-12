import serial
import time
import psycopg2
import os
import logging
import numpy as np
import cv2

# Set up logging
logging.basicConfig(filename='data_insertion.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve database configuration from environment variables
DB_HOST = 'localhost'
DB_USER = 'acu'
DB_PASSWORD = 'acu'
DB_DB = 'acudb'
DB_PORT = '55432'  # Default PostgreSQL port. Change if different.

# Database connection string
DB_CONNECTION = f"dbname='{DB_DB}' user='{DB_USER}' password='{DB_PASSWORD}' host='{DB_HOST}' port='{DB_PORT}'"

# Configuration for serial communication
COM_PORT = 'COM2'  # Update this to your actual COM port
BAUD_RATE = 19200  # Update this to match your device's baud rate
#Link_IP = 'http://192.168.61.27:8086/' # Link for showing videostream from camera
Link_IP = 'http://localhost:8080/playlist.m3u8'

def parse_data(data):
    """Parse the input data and return id_flower, humidity, temperature, and brightness."""
    try:
        id_flower = int(data[:2])
        humidity = int(data[4:6])
        temperature = int(data[7:9])
        brightness = int(data[10:13])
        return id_flower, humidity, temperature, brightness
    except ValueError as e:
        logging.error(f"Error parsing data: {data}", exc_info=True)
        raise

def insert_data(id_flower, humidity, temperature, brightness, flower_state):
    """Insert the data into the database including brightness and flower state."""
    conn = None
    try:
        conn = psycopg2.connect(DB_CONNECTION)
        cur = conn.cursor()
        cur.execute("INSERT INTO measures (id_flower, measure_date, humidity, temperature, brightness, state_flower) VALUES (%s, NOW(), %s, %s, %s, %s)",
                    (id_flower, humidity, temperature, brightness, flower_state))
        conn.commit()
        cur.close()
        logging.info(f"Inserted: Flower ID {id_flower}, Humidity {humidity}, Temperature {temperature}, Brightness {brightness}, State {flower_state}")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error inserting data: {error}", exc_info=True)
    finally:
        if conn is not None:
            conn.close()

def show_video_capture(Link_IP):
    """Get video from Link and take a picture."""
    # Attempt to connect to the video stream
    cap = cv2.VideoCapture(Link_IP)
    if not cap.isOpened():
        logging.info("Cannot open the stream.")
        return
    
    # Read one frame from the video stream
    ret, frame = cap.read()
    if not ret:
        logging.info("Failed to capture a frame from the stream.")
        cap.release()
        return
    
    # Define the path to save the screenshot with the flower ID in the filename
    save_path = os.path.join('image_processing', f'flower_{id_flower}.jpg')
        
    # Save the captured frame as an image
    cv2.imwrite(save_path, frame)
    logging.info(f'Screenshot saved to {save_path}')
    
    # Release the video capture object
    cap.release()

def evaluate_flower_state(image_path):
    """Dummy function to evaluate the flower state. Implement actual logic here."""
    # Actual image processing logic to determine the state of the flower should be implemented here
    return

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    logging.info(f"Connected to {COM_PORT} at {BAUD_RATE} baud rate.")

    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            logging.info(f"Raw data received: {data}")
            try:
                id_flower, humidity, temperature, brightness = parse_data(data)
                show_video_capture(Link_IP)
                #flower_state = evaluate_flower_state('../../image_processing/screenshot.jpg')
                flower_state ='wilted'
                insert_data(id_flower, humidity, temperature, brightness, flower_state)

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
