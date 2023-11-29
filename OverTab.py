import webbrowser
import tkinter as tk
import threading

def open_html_file():
    url = 'GeoFence.html'  # Replace with the actual file path of the HTML file
    text.set("Getting your geofence location..")
    threading.Timer(1, start_timer).start()  # Start the timer in a separate thread
    webbrowser.open(url)

def start_timer():
    global counter
    counter = 0
    update_timer()

def update_timer():
    global counter
    timer.set(f"Elapsed Time: {counter} seconds")
    counter += 1
    timer_label.after(1000, update_timer)  # Update the timer label every second

root = tk.Tk()

text = tk.StringVar()
text_label = tk.Label(root, textvariable=text)
text_label.pack()

timer = tk.StringVar()
timer_label = tk.Label(root, textvariable=timer)
timer_label.pack()

button = tk.Button(root, text='Get My Geolocation', command=open_html_file)
button.pack()

root.mainloop()
