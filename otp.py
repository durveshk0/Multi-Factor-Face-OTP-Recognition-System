import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(otp):
    print(f"OTP sent to the user: {otp}")

def generate_and_send_new_otp():
    global otp, countdown
    otp = generate_otp()
    send_otp(otp)
    countdown = 30  
    countdown_label.config(text=f"Time Remaining: {countdown} seconds")
    update_countdown()
    messagebox.showinfo("New OTP", f"New OTP sent to the user: {otp}")

def validate_otp(user_input, otp):
    return user_input == otp

def validate_and_display_result():
    user_input = otp_entry.get()
    if validate_otp(user_input, otp):
        messagebox.showinfo("Success", "OTP is valid. Access granted.")
        success_label.config(text="Access Granted", foreground="green")
    else:
        messagebox.showerror("Error", "Invalid OTP. Access denied.")
        success_label.config(text="Access Denied", foreground="red")


def update_countdown():
    global countdown
    if countdown > 0:
        countdown_label.config(text=f"Time Remaining: {countdown} seconds")
        root.after(1000, update_countdown)  
        countdown -= 1
    else:
        countdown_label.config(text="Time's Up")
        validate_button.config(state="disabled")  

root = tk.Tk()
root.title("OTP Authentication")

otp = generate_otp()
send_otp(otp)
countdown = 30 

style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), padding=10)

label = ttk.Label(root, text="Enter the OTP you received:")
label.config(font=("Arial", 14))
label.pack(pady=10)

otp_entry = ttk.Entry(root, font=("Arial", 14))
otp_entry.pack(pady=10)

validate_button = ttk.Button(root, text="Validate OTP", command=validate_and_display_result)
validate_button.pack(pady=10)

new_otp_button = ttk.Button(root, text="Resend New OTP", command=generate_and_send_new_otp)
new_otp_button.pack(pady=10)

success_label = ttk.Label(root, text="", font=("Arial", 16))
success_label.pack(pady=10)

countdown_label = ttk.Label(root, text=f"Time Remaining: {countdown} seconds", font=("Arial", 12))
countdown_label.pack(pady=10)
update_countdown()

root.mainloop()
