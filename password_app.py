import random
import string
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext

# --- CONFIGURATION & DATA FILE ---
DATA_FILE = "passwords.json"

# --- CORE LOGIC FUNCTIONS (Unchanged) ---
def check_strength(password):
    """Rates the password strength based on length and character diversity."""
    score = len(password) * 2
    
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digits = any(c in string.digits for c in password)
    has_symbols = any(c in string.punctuation for c in password)
    
    score += 5 * (has_lower + has_upper + has_digits + has_symbols)
        
    if len(password) < 8:
        strength = "Weak (Too Short)"
    elif score < 30:
        strength = "Medium"
    elif score < 45:
        strength = "Strong"
    else:
        strength = "Excellent"
        
    return strength

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """Generates a random password."""
    characters = ""
    if use_lower: characters += string.ascii_lowercase
    if use_upper: characters += string.ascii_uppercase
    if use_digits: characters += string.digits
    if use_symbols: characters += string.punctuation
    
    if not characters or length <= 0:
        return "Error: Check length/options."

    password = ''.join(random.choice(characters) for i in range(length))
    return password

# --- DATA STORAGE FUNCTIONS (Unchanged) ---
def load_passwords():
    """Loads passwords from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_password(password, strength, source="Generated"):
    """Saves a single password entry to the JSON file."""
    passwords = load_passwords()
    new_entry = {
        "password": password,
        "strength": strength,
        "source": source
    }
    passwords.append(new_entry)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(passwords, f, indent=4)
    
    return f"Saved '{password[:5]}...' with strength: {strength}"

# ====================================================================
# --- VAULT VIEW WINDOW CLASS (Unchanged) ---
# ====================================================================

class VaultWindow:
    def __init__(self, master):
        self.master = master
        self.vault_window = tk.Toplevel(master)
        self.vault_window.title("Password Vault")
        
        passwords = load_passwords()
        
        tk.Label(self.vault_window, text="--- Saved Passwords ---", font=("Arial", 12, "bold")).pack(pady=10)

        if not passwords:
            tk.Label(self.vault_window, text="No passwords saved yet.", fg="red").pack(pady=20)
            return

        text_area = scrolledtext.ScrolledText(
            self.vault_window,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=('Courier', 10)
        )
        text_area.pack(padx=10, pady=10)
        
        display_text = "INDEX | STRENGTH    | PASSWORD\n"
        display_text += "------------------------------------------------\n"
        
        for i, entry in enumerate(passwords):
            # Format the output for clean alignment
            line = f"{i+1:5} | {entry['strength']:11} | {entry['password']}\n"
            display_text += line
        
        text_area.insert(tk.INSERT, display_text)
        text_area.configure(state='disabled')
        
        tk.Button(self.vault_window, text="Close", command=self.vault_window.destroy).pack(pady=10)


# ====================================================================
# --- MAIN APPLICATION CLASS (Changes below in `check_frame`) ---
# ====================================================================

class PasswordApp:
    def __init__(self, master):
        self.master = master
        master.title("Password Tool & Vault")

        # --- Variables ---
        self.length_var = tk.StringVar(value="12")
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.output_var = tk.StringVar(value="Generated password will appear here.")
        self.status_var = tk.StringVar(value="Ready.")

        # --- UI Elements ---
        
        # Frame for Generator Controls
        gen_frame = tk.LabelFrame(master, text="Generate Password", padx=10, pady=10)
        gen_frame.pack(padx=10, pady=5, fill="x")

        # Length Input
        tk.Label(gen_frame, text="Length:").grid(row=0, column=0, sticky="w")
        tk.Entry(gen_frame, textvariable=self.length_var, width=5).grid(row=0, column=1, sticky="w")
        
        # Character Checkboxes (Simplified layout for brevity)
        tk.Checkbutton(gen_frame, text="Lowercase", variable=self.lower_var).grid(row=1, column=0, sticky="w")
        tk.Checkbutton(gen_frame, text="Uppercase", variable=self.upper_var).grid(row=1, column=1, sticky="w")
        tk.Checkbutton(gen_frame, text="Digits", variable=self.digits_var).grid(row=2, column=0, sticky="w")
        tk.Checkbutton(gen_frame, text="Symbols", variable=self.symbols_var).grid(row=2, column=1, sticky="w")
        
        # Generate Button
        tk.Button(gen_frame, text="GENERATE", command=self.handle_generate).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Output and Save
        output_label = tk.Label(master, textvariable=self.output_var, wraplength=350, fg="blue", font=("Arial", 10, "bold"))
        output_label.pack(pady=5)
        
        # Save Button for GENERATED passwords
        tk.Button(master, text="SAVE LAST GENERATED PASSWORD", command=self.handle_save_generated).pack(pady=5)
        
        # Frame for Strength Check
        check_frame = tk.LabelFrame(master, text="Check Existing Password", padx=10, pady=10)
        check_frame.pack(padx=10, pady=5, fill="x")
        
        # Row 0: Input Field
        self.check_entry = tk.Entry(check_frame, width=30)
        self.check_entry.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew") # Spans across columns
        
        # Row 1: Action Buttons
        tk.Button(check_frame, text="CHECK STRENGTH", command=self.handle_check).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        # NEW BUTTON: Save for entered password
        tk.Button(check_frame, text="SAVE ENTERED PASSWORD", fg="darkgreen", command=self.handle_save_checked).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # VIEW VAULT BUTTON
        tk.Button(master, text="VIEW SAVED PASSWORDS (VAULT)", fg="darkblue", command=self.handle_view_vault).pack(pady=10)
        
        # Status Bar
        tk.Label(master, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w").pack(side="bottom", fill="x")

    def handle_generate(self):
        """Called when the GENERATE button is pressed."""
        # Logic to generate password and save it temporarily to self.last_password
        try:
            length = int(self.length_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Length must be a number.")
            return

        password = generate_password(
            length,
            self.upper_var.get(),
            self.lower_var.get(),
            self.digits_var.get(),
            self.symbols_var.get()
        )
        
        if password and not password.startswith("Error"):
            strength = check_strength(password)
            self.last_password_generated = password # Store generated password
            self.last_strength_generated = strength # Store generated strength
            self.output_var.set(f"Password: {password}\nStrength: {strength}")
            self.status_var.set("Password generated. Ready to save.")
        else:
            self.output_var.set(password)
            self.status_var.set("Generation failed.")

    def handle_save_generated(self):
        """Called when saving the password from the generator."""
        try:
            password = self.last_password_generated
            strength = self.last_strength_generated
        except AttributeError:
            self.status_var.set("Error: Generate a password first.")
            return

        save_message = save_password(password, strength, source="Generated")
        self.status_var.set(save_message)
        messagebox.showinfo("Save Success", f"Generated password saved to {DATA_FILE}")

    def handle_check(self):
        """Called when the CHECK STRENGTH button is pressed."""
        password = self.check_entry.get()
        if not password:
            messagebox.showerror("Input Error", "Please enter a password to check.")
            return

        strength = check_strength(password)
        # Store checked details for the new save button
        self.last_password_checked = password
        self.last_strength_checked = strength
        self.status_var.set(f"Password checked. Strength: {strength}. Ready to save.")
        messagebox.showinfo("Strength Check Result", f"The password is: {strength}")

    def handle_save_checked(self):
        """NEW METHOD: Called when saving the password entered for checking."""
        try:
            password = self.last_password_checked
            strength = self.last_strength_checked
        except AttributeError:
            # If the user hasn't hit CHECK yet, get the password straight from the entry field
            password = self.check_entry.get()
            if not password:
                 self.status_var.set("Error: Enter or check a password first.")
                 return
            strength = check_strength(password)
            
        # The actual saving function call
        save_message = save_password(password, strength, source="Manual Entry")
        self.status_var.set(save_message)
        messagebox.showinfo("Save Success", f"Entered password saved to {DATA_FILE}")


    def handle_view_vault(self):
        """Opens the separate window to view all saved passwords."""
        VaultWindow(self.master)


# --- RUN THE APP ---

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()
