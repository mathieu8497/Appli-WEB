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
COM_PORT = 'COM4'  # Update this to your actual COM port
BAUD_RATE = 19200  # Update this to match your device's baud rate
Link_IP = 'http://192.168.173.27:8086/' # Link for showing videostream from camera
# Link_IP = 'http://localhost:8080/playlist.m3u8'

def parse_data(data):
    """Parse the input data and return id_flower, humidity, temperature, and brightness."""
    try:
        id_flower = int(data[:2])
        humidity = int(data[4:6])
        temperature = int(data[7:9])
        brightness = int(data[10:14])
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
    save_path = os.path.join('image_processing', f'flower_{id_flower}.png')
        
    # Save the captured frame as an image
    cv2.imwrite(save_path, frame)
    logging.info(f'Screenshot saved to {save_path}')
    
    # Release the video capture object
    cap.release()


##################
# Pré-traitement #
##################

# Fonction pour masquer les images 
def process_image(image_path, dossier_resultats):
    # Lecture de l'image
    image = cv2.imread(image_path)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Définition des plages de couleurs HSV pour différentes couleurs
      # Définition des plages de couleurs HSV pour différentes couleurs
    lower_green = np.array([25, 30, 10])
    upper_green = np.array([85, 255, 255])

    # Pour le noir/marron
    lower_brown = np.array([0, 0, 0])
    upper_brown = np.array([30, 255, 100])

    # Pour le gris
    lower_gray = np.array([0, 0, 50])
    upper_gray = np.array([180, 50, 200])

    # Pour le noir
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])

    # Création des masques pour les différentes couleurs
    mask_green = cv2.inRange(image_hsv, lower_green, upper_green)
    mask_brown = cv2.inRange(image_hsv, lower_brown, upper_brown)
    mask_black = cv2.inRange(image_hsv, lower_black, upper_black)
    mask_gray = cv2.inRange(image_hsv, lower_gray, upper_gray)

    # Combinaison des masques pour obtenir un masque final
    mask_final = cv2.bitwise_or(mask_green, mask_brown)
    mask_final = cv2.bitwise_or(mask_final, mask_black)
    mask_final = cv2.bitwise_or(mask_final, mask_gray)

    # Inversion du masque pour exclure les couleurs spécifiées
    mask_inverse = cv2.bitwise_not(mask_final)

    # Conversion de l'image en format RGBA pour appliquer le masque d'opacité
    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image_rgba[:, :, 3] = mask_inverse

    # Génération du chemin de sauvegarde de l'image traitée
    image_file = os.path.basename(image_path)
    nom_fichier_traite = os.path.splitext(image_file)[0] + ".png"
    chemin_sauvegarde = os.path.join(dossier_resultats, nom_fichier_traite)
    # Enregistrement de l'image traitée
    cv2.imwrite(chemin_sauvegarde, image_rgba)
    print(f"Image traitée enregistrée sous : {chemin_sauvegarde}")

def process_folder(dossier_images, dossier_resultats):
    # Traitement de chaque image dans le dossier
    for image_file in os.listdir(dossier_images):
        image_path = os.path.join(dossier_images, image_file)
        if os.path.isfile(image_path) and image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            process_image(image_path, dossier_resultats)



# Analyse de chaque image dans le dossier
# for image_file in liste_images:
#     image_path = os.path.join(dossier_images, image_file)
#     image = cv2.imread(image_path)
    
#     if is_faded(image):
#         print(f"La fleur dans {image_file} est probablement fanée.")
#     else:
#         print(f"La fleur dans {image_file} est fraîche.")


##################
# Fanée ou non ? #
##################

def load_image_as_grayscale(image_path):
    """ Charge une image et la convertit en niveaux de gris. """
    image = cv2.imread(image_path)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale_image

def calculate_histogram(image, bins=256):
    """ Calcule l'histogramme d'une image. """
    hist = cv2.calcHist([image], [0], None, [bins], [0, 256])
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    return hist

def calculate_average_histogram(directory):
    """ Calcule l'histogramme moyen pour toutes les images dans un dossier. """
    histograms = []
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Assurez-vous que ce sont des images JPEG
            image_path = os.path.join(directory, filename)
            img = load_image_as_grayscale(image_path)
            hist = calculate_histogram(img)
            histograms.append(hist)
    average_hist = np.mean(histograms, axis=0)
    return average_hist

def compare_flower_health(test_image_path, healthy_hist, threshold=0.5):
    """ Compare une image de test avec l'histogramme de référence pour déterminer la santé de la fleur. """
    test_img = load_image_as_grayscale(test_image_path)
    test_hist = calculate_histogram(test_img)
    similarity = cv2.compareHist(healthy_hist, test_hist, cv2.HISTCMP_CORREL)
    health_status = "not wilted" if similarity > threshold else "wilted"
    return health_status, similarity

# Exemple d'utilisation
def evaluate_flower_state1() :
    # fleurs à traiter (au début, dossier contenant une seule image)
    dossier_images = 'image_processing'#../image_processing
    # dossier contenant les images pré-traitées
    dossier_resultats = 'src/resultats'#../src/resultats
    process_folder(dossier_images, dossier_resultats)

def evaluate_flower_state2(path_flower_evaluate) :
    healthy_directory = 'src/images'#../src/images
    test_directory = "src/resultats/" + path_flower_evaluate# Image de test unique  #../src/resultats/
    healthy_hist = calculate_average_histogram(healthy_directory)
    status, score = compare_flower_health(test_directory, healthy_hist)
    print("state: ", status)
    return(status)

# Main loop

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
                path_flower_evaluate = f'flower_{id_flower}.png'
                evaluate_flower_state1()
                flower_state = evaluate_flower_state2(path_flower_evaluate)
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
