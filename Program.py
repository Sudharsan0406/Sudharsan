import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import smtplib
from email.mime.text import MIMEText

# Email config - replace with your info
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"  # For Gmail, consider App Passwords for 2FA

# Function to send email alert
def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS  # You can send to any email you want

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email alert sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# === Data and Model ===
CORRECT_PASSWORD = "secure123"
attempts = 0
MAX_ATTEMPTS = 3

X_train = np.array([
    [100, 0, 1],
    [2000, 1, 2],
    [50, 0, 1],
    [5000, 1, 3],
    [20, 0, 1],
    [3000, 1, 2],
    [10, 0, 1],
    [7000, 1, 3]
])
y_train = np.array([0, 1, 0, 1, 0, 1, 0, 1])

model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

def predict_fraud(amount, transaction_type, location_code):
    features = np.array([[amount, transaction_type, location_code]])
    prediction = model.predict(features)
    return prediction[0]

# === GUI ===
def check_password():
    global attempts
    entered_password = password_entry.get()
    
    if entered_password == CORRECT_PASSWORD:
        messagebox.showinfo("Access Granted", "Welcome! Transaction access granted.")
        attempts = 0
        root.withdraw()
        open_fraud_detection_window()
    else:
        attempts += 1
        messagebox.showwarning("Access Denied", f"Wrong password! Attempt {attempts} of {MAX_ATTEMPTS}.")
        if attempts >= MAX_ATTEMPTS:
            messagebox.showerror("ALERT 🚨", "Multiple failed attempts detected!\nThis attempt has been flagged as suspicious.")
            # Send email alert
            send_email_alert(
                subject="🚨 Alert: Multiple Failed Login Attempts",
                body=f"There have been {attempts} failed login attempts on your Fraud Detection app."
            )

def open_fraud_detection_window():
    fraud_window = tk.Toplevel()
    fraud_window.title("💼 Fraud Detection System")
    fraud_window.geometry("400x320")
    fraud_window.configure(bg="#f2f2f2")

    ttk.Label(fraud_window, text="Enter Transaction Amount:").pack(pady=5)
    amount_entry = ttk.Entry(fraud_window)
    amount_entry.pack()

    ttk.Label(fraud_window, text="Transaction Type (0=debit, 1=credit):").pack(pady=5)
    type_entry = ttk.Entry(fraud_window)
    type_entry.pack()

    ttk.Label(fraud_window, text="Location Code (1, 2, or 3):").pack(pady=5)
    location_entry = ttk.Entry(fraud_window)
    location_entry.pack()

    def on_predict():
        try:
            amount = float(amount_entry.get())
            transaction_type = int(type_entry.get())
            location_code = int(location_entry.get())
            if transaction_type not in [0, 1] or location_code not in [1, 2, 3]:
                messagebox.showerror("Input Error", "Transaction type must be 0 or 1, location code must be 1, 2, or 3.")
                return
            result = predict_fraud(amount, transaction_type, location_code)
            if result == 1:
                messagebox.showwarning("Fraud Detection Result", "⚠️ Warning: This transaction is likely FRAUDULENT!")
            else:
                messagebox.showinfo("Fraud Detection Result", "✅ This transaction appears LEGITIMATE.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

    ttk.Button(fraud_window, text="Check Fraud", command=on_predict).pack(pady=15)

# === Root Window ===
root = tk.Tk()
root.title("🔒 Secure Login")
root.geometry("320x200")
root.configure(bg="#e6f2ff")

# === Styling ===
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10), padding=6, foreground="white", background="#007acc")
style.configure("TLabel", font=("Segoe UI", 10), background="#e6f2ff")
style.configure("TEntry", padding=5)

# === Login Form ===
ttk.Label(root, text="Enter your password:").pack(pady=15)
password_entry = ttk.Entry(root, show="*", width=25)
password_entry.pack()

ttk.Button(root, text="Submit", command=check_password).pack(pady=20)

root.mainloop()

