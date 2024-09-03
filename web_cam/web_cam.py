import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import webbrowser

# Function to update the frame in the GUI
def update_frame():
    ret, frame = cap.read()
    if ret:
        # Resize the frame to fit the window
        frame = cv2.resize(frame, (root.winfo_width(), root.winfo_height()))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl.imgtk = imgtk
        lbl.configure(image=imgtk)
    lbl.after(10, update_frame)

# Function to start the camera
def start_camera():
    global cap
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        tk.messagebox.showerror("Error", "Unable to open the camera stream. Please check the URL or your network connection.")
        return
    update_frame()

# Function to stop the camera and close the application
def stop_camera():
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    root.quit()

# Function to capture an image with a file chooser
def capture_image():
    ret, frame = cap.read()
    if ret:
        # Open file dialog to choose the file path and name
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                               filetypes=[("JPEG files", "*.jpg"),
                                                          ("PNG files", "*.png"),
                                                          ("All files", "*.*")],
                                               title="Save Image As")
        if file_path:
            cv2.imwrite(file_path, frame)
            tk.messagebox.showinfo("Image Captured", f"Image has been saved as '{file_path}'")

# Function to show the 'About' window
def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    tk.Label(about_window, text="Smartphone Webcam\nVersion 1.0\nDeveloped by Ajay Chauhan").pack(pady=25)

# Function to show the 'Help' window
def show_help():
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    
    text_widget = tk.Text(help_window, bg='white', fg='black', borderwidth=0, height=28, width=80)
    text_widget.pack(pady=20)
    text_widget.insert(tk.END, "Connect your smartphone camera using IP Webcam or similar app.\n\n")
    text_widget.insert(tk.END, "1. First, install the OpenCV library in Python;\ncommand : pip install opencv-python.\n\n")
    text_widget.insert(tk.END, "2. Download and install the IP Webcam application on your smartphones.\n\n")
    text_widget.insert(tk.END, "3. Make sure your phone and PC are connected to the same network. Run the app on your phone and click Start Server.\n\n")
    text_widget.insert(tk.END, "4. Your camera will open with an IP address at the bottom. Copy the IP address to use in this application.\n\n")
    text_widget.insert(tk.END, "For more details, visit: https://chess.com", 'link')

    text_widget.tag_configure('link', foreground='blue', underline=True)
    text_widget.tag_bind('link', '<Button-1>', lambda e: webbrowser.open("https://chess.com"))
    text_widget.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("Smartphone Webcam")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.config(background='#ffffff')

# Label to display the camera feed
lbl = tk.Label(root)
lbl.pack(fill=tk.BOTH, expand=True)

# Create a menubar
menubar = tk.Menu(root)
menu = tk.Menu(menubar, fg='Yellow', bg='Black', tearoff=0)
menu.add_command(label="About", command=show_about)
menu.add_command(label="Help", command=show_help)
menubar.add_cascade(label="Menu", menu=menu)
root.config(menu=menubar)

# Frame to hold buttons
button_frame = tk.Frame(root, bg='#ffffff')
button_frame.pack(side=tk.TOP, fill=tk.X)

# Start, Stop, and Capture buttons
start_btn = tk.Button(button_frame, text="Start Camera", command=start_camera)
start_btn.pack(side=tk.LEFT, padx=10, pady=10)v

stop_btn = tk.Button(button_frame, text="Stop Camera", command=stop_camera)
stop_btn.pack(side=tk.LEFT, padx=10, pady=10)

capture_btn = tk.Button(button_frame, text="Capture", command=capture_image)
capture_btn.pack(side=tk.LEFT, padx=10, pady=10)

# Replace with your smartphone camera URL
url = "http://192.168.0.101:8080/video"

root.mainloop()
