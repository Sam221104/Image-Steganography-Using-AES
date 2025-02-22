import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import encrypt
import decrypt

def load_cover_image():
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    cover_image_entry.delete(0, tk.END)
    cover_image_entry.insert(0, filename)
    display_image(filename, cover_image_label)

def display_image(image_path, label):
    image = Image.open(image_path)
    image.thumbnail((150, 150))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo 

def encrypt_message():
    secret_message = secret_message_entry.get()
    password = password_entry.get()
    cover_image = cover_image_entry.get()
    output_image = "encrypted_image.png"
    if secret_message and password and cover_image:
        encrypt.hide_text_in_image(secret_message, cover_image, output_image, encrypt.SHA256.new(password.encode()).digest())
        messagebox.showinfo("Success", "Message encrypted and hidden in the image successfully!")
    else:
        messagebox.showerror("Error", "All fields are required for encryption!")

def load_encrypted_image():
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    encrypted_image_entry.delete(0, tk.END)
    encrypted_image_entry.insert(0, filename)
    display_image(filename, encrypted_image_label)

def decrypt_message():
    password = decrypt_password_entry.get()
    encrypted_image = encrypted_image_entry.get()
    if password and encrypted_image:
        key = decrypt.SHA256.new(password.encode()).digest()
        decrypted_text = decrypt.reveal_text_from_image(encrypted_image, key)
        decrypted_message_text.delete("1.0", tk.END)
        decrypted_message_text.insert(tk.END, decrypted_text if decrypted_text else "Decryption failed!")
    else:
        messagebox.showerror("Error", "All fields are required for decryption!")

def show_encryption_page():
    notebook.select(encryption_frame)

def show_decryption_page():
    notebook.select(decryption_frame)

root = tk.Tk()
root.title("Image Steganography")
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Start Page
start_frame = ttk.Frame(notebook)
notebook.add(start_frame, text="Start")
ttk.Label(start_frame, text="Choose an option:").pack(pady=7)
ttk.Button(start_frame, text="Encrypt", command=show_encryption_page).pack(pady=5)
ttk.Button(start_frame, text="Decrypt", command=show_decryption_page).pack(pady=5)

# Encryption Page
encryption_frame = ttk.Frame(notebook)
notebook.add(encryption_frame, text="Encryption")
ttk.Label(encryption_frame, text="Load Image (For Encryption)").pack()
cover_image_entry = ttk.Entry(encryption_frame, width=50)
cover_image_entry.pack(pady=3)
ttk.Button(encryption_frame, text="Select Image To Encrypt", command=load_cover_image).pack(pady=5)
cover_image_label = tk.Label(encryption_frame)
cover_image_label.pack(pady=5)

ttk.Label(encryption_frame, text="Secret Message:").pack(pady=2)
secret_message_entry = ttk.Entry(encryption_frame, width=50)
secret_message_entry.pack()

ttk.Label(encryption_frame, text="Passcode:").pack(pady=2)
password_entry = ttk.Entry(encryption_frame, width=50, show="*")
password_entry.pack()

ttk.Button(encryption_frame, text="Encrypt", command=encrypt_message).pack(pady=10)

# Decryption Page
decryption_frame = ttk.Frame(notebook)
notebook.add(decryption_frame, text="Decryption")
ttk.Label(decryption_frame, text="Load Encrypted Image (For Decryption)").pack()
encrypted_image_entry = ttk.Entry(decryption_frame, width=50)
encrypted_image_entry.pack(pady=3)
ttk.Button(decryption_frame, text="Load Encrypted Image", command=load_encrypted_image).pack(pady=5)
encrypted_image_label = tk.Label(decryption_frame)
encrypted_image_label.pack(pady=5)

ttk.Label(decryption_frame, text="Passcode:").pack(pady=2)
decrypt_password_entry = ttk.Entry(decryption_frame, width=50, show="*")
decrypt_password_entry.pack()
ttk.Button(decryption_frame, text="Decrypt", command=decrypt_message).pack(pady=10)

ttk.Label(decryption_frame, text="Decrypted Message:").pack(pady=2)
decrypted_message_text = tk.Text(decryption_frame, height=5, width=50)
decrypted_message_text.pack(pady=2)

root.mainloop()
