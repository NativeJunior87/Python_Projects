import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from datetime import datetime

#Server Configuration
root = tk.Tk()
root.withdraw()
logo = tk.PhotoImage(file="z.png")
root.iconphoto(False, logo)
server_ip = simpledialog.askstring("Server Address", "Enter server IP address:")
username = simpledialog.askstring("Username", "Enter your username:")
PORT = 12345
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, PORT))

#GUI CONFIGURATION
root.deiconify()
root.title("Messenger")
root.configure(bg="#f0f0f0")

header = tk.Label(root, text="You're now in Chatroom", font=("Segoe UI", 14, "bold"), bg="#698194", fg="#0E1621")
header.pack(fill=tk.X, pady=(0, 5))

chat_box = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20, wrap=tk.WORD, font=("Consolas", 10))
chat_box.pack(padx=10, pady=(5, 0))

input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(padx=10, pady=10)

msg_entry = tk.Entry(input_frame, width=45, font=("Segoe UI", 10))
msg_entry.pack(side=tk.LEFT, padx=(0, 5))
msg_entry.bind("<Return>", lambda event: send())

send_button = tk.Button(input_frame, text="Send", command=lambda: send(), bg="#64b5f6", fg="white", width=10)
send_button.pack(side=tk.LEFT)

status = tk.Label(root, text=f"Connected to {server_ip}:{PORT} | User: {username}", anchor="w", bd=1, relief=tk.SUNKEN)
status.pack(fill=tk.X, side=tk.BOTTOM)

def send():
    msg = msg_entry.get().strip()
    if msg:
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {username}: {msg}"
        client.send(full_msg.encode())
        chat_box.config(state='normal')
        chat_box.insert(tk.END, full_msg + '\n')
        chat_box.config(state='disabled')
        chat_box.yview(tk.END)

        msg_entry.delete(0, tk.END)

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            chat_box.config(state='normal')
            chat_box.insert(tk.END, msg + '\n')
            chat_box.config(state='disabled')
            chat_box.yview(tk.END)
        except:
            break

threading.Thread(target=receive, daemon=True).start()
root.mainloop()

