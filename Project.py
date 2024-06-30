from picamera import PiCamera
from telegram.ext import Updater
import subprocess
import RPi.GPIO as GPIO
import time

# GPIO pin connected to the button
BUTTON_PIN = 5

# Replace with your Telegram Bot Token and target user ID
BOT_TOKEN = "6703526385:AAHW3tYtunhdJSLukCdx8oaIZm7-Re3ssXU"   # Replace with your actual token
TARGET_USER_ID = 1562061108 # Replace with your Telegram user ID

def capture_and_send_image():
    # Capture image with PiCamera
    with PiCamera() as camera:
        camera.capture("captured_image.jpg")

    # Send image via Telegram
    updater = Updater(token=BOT_TOKEN, use_context=True, request_kwargs={'connect_timeout': 60, 'read_timeout': 60})
    chat_id = TARGET_USER_ID

    try:
        with open("captured_image.jpg", "rb") as f:
            image_data = f.read()
        updater.bot.send_photo(chat_id=chat_id, photo=image_data, caption="Captured Image")
        print("Image sent successfully!")
    except Exception as e:
        print(f"Error sending image: {e}")

def capture_and_send_audio():
    # Record audio message
    try:
        subprocess.run(["arecord", "-D", "plughw:1", "-f", "cd", "-d", "5", "-r", "22050", "captured_audio.wav"], check=True)
        print("Audio message recorded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error recording audio: {e}")

    # Send audio message via Telegram
    updater = Updater(token=BOT_TOKEN, use_context=True, request_kwargs={'connect_timeout': 60, 'read_timeout': 60})
    chat_id = TARGET_USER_ID

    try:
        with open("captured_audio.wav", "rb") as f:
            audio_data = f.read()
        updater.bot.send_audio(chat_id=chat_id, audio=audio_data, caption="Audio Message")
        print("Audio message sent successfully!")
    except Exception as e:
        print(f"Error sending audio message: {e}")

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
    print("Button pressed!")
    capture_and_send_image()
    capture_and_send_audio()
    # Remove event listener after button press
    GPIO.remove_event_detect(BUTTON_PIN)

# Add event listener for button press
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

# Keep the script running
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()