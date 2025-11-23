import random
import string

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """Generates a random password based on specified criteria."""
    
    # 1. Define the character pool based on user input
    characters = ""
    if use_lower:
        characters += string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        # Punctuation set that is generally safe for most systems
        characters += string.punctuation
    
    # Check if the character set is empty (user chose no options)
    if not characters:
        print("Error: You must select at least one character type (e.g., lowercase, digits).")
        return None

    # 2. Generate the password
    # random.choice selects a random character from the 'characters' string
    # A list comprehension and .join is used to efficiently create the final string
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def check_strength(password):
    """Rates the password strength based on length and character diversity."""
    
    # Initial score based on length (e.g., 2 points per character)
    score = len(password) * 2
    
    # Check for character types
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digits = any(c in string.digits for c in password)
    has_symbols = any(c in string.punctuation for c in password)
    
    # Add bonus points for diverse character types
    if has_lower:
        score += 5
    if has_upper:
        score += 5
    if has_digits:
        score += 5
    if has_symbols:
        score += 5
        
    # --- Determine the Strength Rating ---
    if len(password) < 8:
        strength = "Weak (Too Short)"
    elif score < 30:
        strength = "Medium"
    elif score < 45:
        strength = "Strong"
    else:
        strength = "Excellent"
        
    return strength

def main():
    """The main application loop."""
    print("✨ Welcome to the Python Password Tool! ✨")
    
    while True:
        print("\n--- Menu ---")
        print("1. Generate a new password")
        print("2. Check the strength of an existing password")
        print("3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            try:
                length = int(input("Enter desired password length (e.g., 12): "))
                if length <= 0:
                    print("Length must be a positive number.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            # Get complexity options (y/n input)
            use_lower = input("Include lowercase letters? (y/n): ").lower() == 'y'
            use_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
            use_digits = input("Include numbers? (y/n): ").lower() == 'y'
            use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
            
            # Generate and check
            password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
            if password:
                strength = check_strength(password)
                print("\n🔐 Generated Password: **{}**".format(password))
                print("💪 Strength Rating: **{}**".format(strength))

        elif choice == '2':
            password = input("Enter the password you want to check: ")
            strength = check_strength(password)
            print("\n💪 Strength Rating for '{}': **{}**".format(password, strength))

        elif choice == '3':
            print("Thank you for using the tool. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
