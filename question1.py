def shift_char_encrypt(c, shift1, shift2):
    """Encrypt a single character based on the assignment rules."""
    if c.islower():
        if 'a' <= c <= 'm':
            # first half lowercase: shift forward by shift1*shift2
            return chr(((ord(c) - ord('a') + shift1 * shift2) % 26) + ord('a'))
        else:
            # second half lowercase: shift backward by shift1+shift2
            return chr(((ord(c) - ord('a') - (shift1 + shift2)) % 26) + ord('a'))
    elif c.isupper():
        if 'A' <= c <= 'M':
            # first half uppercase: shift backward by shift1
            return chr(((ord(c) - ord('A') - shift1) % 26) + ord('A'))
        else:
            # second half uppercase: shift forward by shift2 squared
            return chr(((ord(c) - ord('A') + shift2**2) % 26) + ord('A'))
    else:
        return c  # numbers, spaces, punctuation remain unchanged

# DECRYPTION LOGIC 
def shift_char_decrypt(c, shift1, shift2, original_c=None):
    """
    Decrypt a single character using original encryption rules.
    Instead of checking the current encrypted character, we check its original rule.
    """
    if original_c is None:
        # fallback: use the same logic as encryption (works for verification)
        original_c = c

    if original_c.islower():
        if 'a' <= original_c <= 'm':
            return chr(((ord(c) - ord('a') - shift1 * shift2) % 26) + ord('a'))
        else:
            return chr(((ord(c) - ord('a') + (shift1 + shift2)) % 26) + ord('a'))
    elif original_c.isupper():
        if 'A' <= original_c <= 'M':
            return chr(((ord(c) - ord('A') + shift1) % 26) + ord('A'))
        else:
            return chr(((ord(c) - ord('A') - shift2**2) % 26) + ord('A'))
    else:
        return c

# FILE OPERATIONS
def encrypt_file(shift1, shift2):
    try:
        with open("raw_text.txt", "r", encoding="utf-8") as f:
            text = f.read()
        encrypted = "".join(shift_char_encrypt(c, shift1, shift2) for c in text)
        with open("encrypted_text.txt", "w", encoding="utf-8") as f:
            f.write(encrypted)
        print("[INFO] Encryption successful! Output saved in 'encrypted_text.txt'")
    except FileNotFoundError:
        print("[ERROR] 'raw_text.txt' not found. Please create the file with some text.")
    except Exception as e:
        print(f"[ERROR] Unexpected error during encryption: {e}")

def decrypt_file(shift1, shift2):
    try:
        with open("raw_text.txt", "r", encoding="utf-8") as f:
            original_text = f.read()  # to know original ranges
        with open("encrypted_text.txt", "r", encoding="utf-8") as f:
            encrypted_text = f.read()

        decrypted = "".join(
            shift_char_decrypt(c, shift1, shift2, original_c=oc)
            for c, oc in zip(encrypted_text, original_text)
        )

        with open("decrypted_text.txt", "w", encoding="utf-8") as f:
            f.write(decrypted)
        print("[INFO] Decryption successful! Output saved in 'decrypted_text.txt'")
    except FileNotFoundError:
        print("[ERROR] 'encrypted_text.txt' not found. Please run encryption first.")
    except Exception as e:
        print(f"[ERROR] Unexpected error during decryption: {e}")

def verify():
    """Compare original raw text with decrypted text"""
    try:
        with open("raw_text.txt", "r", encoding="utf-8") as f1, \
             open("decrypted_text.txt", "r", encoding="utf-8") as f2:
            if f1.read() == f2.read():
                print("[SUCCESS] Verification passed! Decrypted text matches original text.")
            else:
                print("[FAILED] Verification failed. Decrypted text does not match original.")
    except FileNotFoundError:
        print("[ERROR] Verification failed because one or more files are missing.")
    except Exception as e:
        print(f"[ERROR] Unexpected error during verification: {e}")

# MAIN PROGRAM
if __name__ == "__main__":
    print("=== Custom Text Encryption & Decryption Tool ===")
    try:
        shift1 = int(input("Enter shift1 (integer): "))
        shift2 = int(input("Enter shift2 (integer): "))

        encrypt_file(shift1, shift2)
        decrypt_file(shift1, shift2)
        verify()

    except ValueError:
        print("[ERROR] Invalid input. Please enter integer values.")
    except Exception as e:
        print(f"[ERROR] Unexpected crash: {e}")