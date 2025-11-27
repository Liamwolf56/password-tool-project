# Password Tool & Vault

## 🔑 Project Overview

This is a comprehensive desktop application developed in Python that provides a robust solution for password security. It features a strong random password generator, a real-time strength checker for user-defined passwords, and a secure vault for storing all entries locally.

The application utilizes the `tkinter` library for a user-friendly graphical interface (GUI) and the built-in `json` module for persistent data storage.

---

## ✨ Features

* **Strong Password Generation:** Creates random passwords based on user-defined length and complexity (uppercase, lowercase, digits, symbols).
* **Strength Checker:** Evaluates existing passwords based on length and character diversity, providing ratings like "Weak," "Medium," "Strong," or "Excellent."
* **Secure Data Vault:** Saves both generated and manually entered passwords, along with their strength rating, to a local `passwords.json` file.
* **Vault Viewer:** A dedicated secondary screen to load and display all saved entries from the vault in a clear, scrollable format.

---

## 🚀 Getting Started

### Prerequisites

To run this application, you need Python 3 installed. You will also need the `tkinter` module, which is not always included with the standard Python installation on Linux/WSL.

You can install it in your environment using the following command:

```bash
sudo apt install python3-tk
