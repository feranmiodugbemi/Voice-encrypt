import tkinter as tk
from tkinter import filedialog
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
#####
# Key and initialization vector (IV) for encryption
key = b'0123456789abcdef0123456789abcdef'  # 32 bytes
iv = b'0123456789abcdef'  # 16 bytes

def encrypt_file(file_path):
    # Create a cipher object with AES-CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Open the file for reading and writing
    with open(file_path, 'rb+') as f:
        # Read the original data
        data = f.read()

        # Encrypt the data
        padded_data = pad_data(data, algorithms.AES.block_size)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Overwrite the file with the encrypted data
        f.seek(0)
        f.truncate()
        f.write(encrypted_data)
        # Rename the file with .encrypted between the name and extension
        dir_path, file_name = os.path.split(file_path)
        base_name, ext = os.path.splitext(file_name)
        encrypted_file_name = f"{base_name}.encrypted{ext}"
        encrypted_file_path = os.path.join(dir_path, encrypted_file_name)
        os.rename(file_path, encrypted_file_path)
        print("File successfullly encrypted")
        
def decrypt_file(file_path):
    # Split the file name and check for .encrypted
    dir_path, file_name = os.path.split(file_path)
    base_name, ext = os.path.splitext(file_name)
    if ".encrypted" not in base_name:
        print("File not decryptable")
        return

    # Remove .encrypted from the file name
    base_name = base_name.replace(".encrypted", "")
    decrypted_file_name = f"{base_name}{ext}"
    decrypted_file_path = os.path.join(dir_path, decrypted_file_name)

    # Create a cipher object with AES-CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Open the file for reading and writing
    with open(file_path, 'rb+') as f:
        # Read the encrypted data
        encrypted_data = f.read()

        # Decrypt the encrypted data
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadded_data = unpad_data(decrypted_data)

        # Overwrite the file with the decrypted data
        f.seek(0)
        f.truncate()
        f.write(unpadded_data)

    # Rename the file to its decrypted name
    os.rename(file_path, decrypted_file_path)
    print("File successfully decrypted")

def pad_data(data, block_size):
    padding_len = block_size - (len(data) % block_size)
    return data + bytes([padding_len]) * padding_len

def unpad_data(padded_data):
    if not padded_data:
        return padded_data
    padding_len = padded_data[-1]
    return padded_data[:-padding_len]

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.config(text=file_path)

def encrypt_selected_file():
    file_path = file_label.cget("text")
    if file_path:
        encrypt_file(file_path)

def decrypt_selected_file():
    file_path = file_label.cget("text")
    if file_path:
        decrypt_file(file_path)

# Create the main window
root = tk.Tk()
root.title("File Encryption/Decryption")

# Create a label to display the selected file
file_label = tk.Label(root, text="No file selected", anchor="w")
file_label.pack(fill="x", padx=10, pady=5)

# Create buttons
browse_button = tk.Button(root, text="Browse File", command=browse_file)
browse_button.pack(fill="x", padx=10, pady=5)

encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt_selected_file)
encrypt_button.pack(fill="x", padx=10, pady=5)

decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_selected_file)
decrypt_button.pack(fill="x", padx=10, pady=5)

# Start the main event loop
root.mainloop()