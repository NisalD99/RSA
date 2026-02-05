from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import base64
import time
import psutil
import os

class RSA_Crypto:
    def __init__(self, key_size=2048):
        """Initialize RSA with specified key size"""
        self.key_size = key_size
        self.key_pair = None
        self.public_key = None
        self.private_key = None
        self.process = psutil.Process()
        
    def get_cpu_memory_usage(self):
        """Get current CPU and memory usage"""
        cpu_percent = self.process.cpu_percent()
        memory_info = self.process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024  # Convert to MB
        return cpu_percent, round(memory_mb, 2)
    
    def generate_keys(self):
        """Generate RSA key pair"""
        print(f"Generating RSA-{self.key_size} key pair...")
        start_time = time.time()
        
        self.key_pair = RSA.generate(self.key_size)
        self.public_key = self.key_pair.publickey()
        self.private_key = self.key_pair
        
        end_time = time.time()
        generation_time = end_time - start_time
        print(f"Key generation completed in {generation_time:.4f} seconds")
        return generation_time
    
    def encrypt_message(self, plaintext):
        """Encrypt message using RSA public key"""
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode('utf-8')
        
        # Get CPU/Memory usage before encryption
        cpu_before, mem_before = self.get_cpu_memory_usage()
        
        # Use PKCS1_OAEP for secure encryption
        cipher = PKCS1_OAEP.new(self.public_key, hashAlgo=SHA256)
        
        start_time = time.time()
        ciphertext = cipher.encrypt(plaintext)
        end_time = time.time()
        
        # Get CPU/Memory usage after encryption
        cpu_after, mem_after = self.get_cpu_memory_usage()
        cpu_usage = max(cpu_before, cpu_after)
        
        encryption_time = end_time - start_time
        return base64.b64encode(ciphertext).decode('utf-8'), encryption_time, cpu_usage, mem_after
    
    def decrypt_message(self, encrypted_text):
        """Decrypt message using RSA private key"""
        if isinstance(encrypted_text, str):
            encrypted_text = base64.b64decode(encrypted_text.encode('utf-8'))
        
        # Get CPU/Memory usage before decryption
        cpu_before, mem_before = self.get_cpu_memory_usage()
        
        cipher = PKCS1_OAEP.new(self.private_key, hashAlgo=SHA256)
        
        start_time = time.time()
        plaintext = cipher.decrypt(encrypted_text)
        end_time = time.time()
        
        # Get CPU/Memory usage after decryption
        cpu_after, mem_after = self.get_cpu_memory_usage()
        cpu_usage = max(cpu_before, cpu_after)
        
        decryption_time = end_time - start_time
        return plaintext.decode('utf-8'), decryption_time, cpu_usage, mem_after

def test_basic_functionality():
    """Test basic RSA encryption/decryption functionality"""
    print("=== Basic RSA Functionality Test ===")
    
    # Get message from user
    test_message = input("Enter your message to encrypt: ")
    
    # Initialize RSA crypto system with 2048-bit key
    rsa = RSA_Crypto(2048)
    key_gen_time = rsa.generate_keys()
    
    print(f"Original message: {test_message}")
    print(f"Message length: {len(test_message)} bytes")
    
    # Encryption test
    encrypted_msg, enc_time, enc_cpu, enc_mem = rsa.encrypt_message(test_message)
    print(f"Encrypted message (base64): {encrypted_msg[:100]}...")
    print(f"Encryption time: {enc_time:.6f} seconds")
    print(f"CPU Usage: {enc_cpu}%")
    print(f"Memory Usage: {enc_mem} MB")
    
    # Decryption test
    decrypted_msg, dec_time, dec_cpu, dec_mem = rsa.decrypt_message(encrypted_msg)
    print(f"Decrypted message: {decrypted_msg}")
    print(f"Decryption time: {dec_time:.6f} seconds")
    print(f"CPU Usage: {dec_cpu}%")
    print(f"Memory Usage: {dec_mem} MB")
    
    # Verify correctness
    if test_message == decrypted_msg:
        print("✓ Encryption/Decryption test: PASSED")
    else:
        print("✗ Encryption/Decryption test: FAILED")
    
    return key_gen_time, enc_time, dec_time

if __name__ == "__main__":
    # Run basic functionality test with user input
    key_time, enc_time, dec_time = test_basic_functionality()