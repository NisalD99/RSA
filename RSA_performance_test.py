from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import base64
import time
import psutil
import os

class RSA_Performance_Tester:
    def __init__(self):
        self.process = psutil.Process()
        
    def get_cpu_memory_usage(self):
        """Get current CPU and memory usage"""
        cpu_percent = self.process.cpu_percent()
        memory_info = self.process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024  # Convert to MB
        return cpu_percent, round(memory_mb, 2)
    
    def generate_rsa_keys(self, key_size):
        """Generate RSA key pair with timing"""
        start_time = time.time()
        key_pair = RSA.generate(key_size)
        public_key = key_pair.publickey()
        end_time = time.time()
        return key_pair, public_key, end_time - start_time
    
    def encrypt_message(self, public_key, plaintext):
        """Encrypt message with timing"""
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode('utf-8')
        
        cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
        start_time = time.time()
        ciphertext = cipher.encrypt(plaintext)
        end_time = time.time()
        
        return base64.b64encode(ciphertext).decode('utf-8'), end_time - start_time
    
    def decrypt_message(self, private_key, encrypted_text):
        """Decrypt message with timing"""
        if isinstance(encrypted_text, str):
            encrypted_text = base64.b64decode(encrypted_text.encode('utf-8'))
        
        cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        start_time = time.time()
        plaintext = cipher.decrypt(encrypted_text)
        end_time = time.time()
        
        return plaintext.decode('utf-8'), end_time - start_time
    
    def test_key_sizes(self):
        """Test different key sizes with fixed data size"""
        print("| Varying Condition 1 | Key size (fixed data size)")
        print("| Key Size      | Data (B)      | Enc Time (s)    | Dec Time (s)   |    |")
        
        fixed_data = "A" * 32  # 32 bytes fixed data
        key_sizes = [1024, 2048, 3072, 4096]
        
        for key_size in key_sizes:
            try:
                # Get initial CPU/Memory
                cpu_before, mem_before = self.get_cpu_memory_usage()
                
                # Generate keys
                private_key, public_key, key_gen_time = self.generate_rsa_keys(key_size)
                
                # Encrypt
                encrypted, enc_time = self.encrypt_message(public_key, fixed_data)
                
                # Decrypt
                decrypted, dec_time = self.decrypt_message(private_key, encrypted)
                
                # Get final CPU/Memory
                cpu_after, mem_after = self.get_cpu_memory_usage()
                cpu_usage = max(cpu_before, cpu_after)
                
                # Verify correctness
                status = "OK" if decrypted == fixed_data else "FAIL"
                
                print(f"| {key_size}    | {len(fixed_data)}    | {enc_time:.6f}    | {dec_time:.6f}    | {cpu_usage}    | {mem_after}   {status}    |")
                
            except Exception as e:
                print(f"| {key_size}    | {len(fixed_data)}    | ERROR    | ERROR    | -    | -   FAIL    |")
    
    def test_data_sizes(self):
        """Test different input data sizes with fixed key size"""
        print("\n[ Varying Condition 2 ] Input data size ")
        print("Input Size    Enc Time (s)    Dec Time (s)    CPU (%)    Mem (MB)    Status")
        
        # Generate fixed key pair
        private_key, public_key, _ = self.generate_rsa_keys(2048)
        
        data_sizes = [32, 100, 500]  # bytes
        max_rsa_data_size = 214  # Maximum data size for RSA-2048 with OAEP padding
        
        for size in data_sizes:
            try:
                if size > max_rsa_data_size:
                    print(f"{size} B    -    -    -    -    Too long (max {max_rsa_data_size}B)")
                    continue
                
                # Get initial CPU/Memory
                cpu_before, mem_before = self.get_cpu_memory_usage()
                
                test_data = "A" * size
                
                # Encrypt
                encrypted, enc_time = self.encrypt_message(public_key, test_data)
                
                # Decrypt
                decrypted, dec_time = self.decrypt_message(private_key, encrypted)
                
                # Get final CPU/Memory
                cpu_after, mem_after = self.get_cpu_memory_usage()
                cpu_usage = max(cpu_before, cpu_after)
                
                # Verify correctness
                status = "OK" if decrypted == test_data else "FAIL"
                
                print(f"{size} B    {enc_time:.6f}    {dec_time:.6f}    {cpu_usage:.2f}    {mem_after}    {status}")
                
            except Exception as e:
                print(f"{size} B    -    -    -    -    ERROR")
    
    def test_file_types(self):
        """Test different file types with small file sizes"""
        print("\n[ Varying Condition 3 ] File type")
        print("Type    File    Enc Time (s)    Dec Time (s)    CPU (%)    Mem (MB)    Status")
        
        # Generate fixed key pair
        private_key, public_key, _ = self.generate_rsa_keys(2048)
        
        file_types = [
            ("txt", "small_sample.txt"),
            ("png", "small_sample.png"), 
            ("pdf", "small_sample.pdf")
        ]
        
        for file_type, filename in file_types:
            try:
                if not os.path.exists(filename):
                    print(f"{file_type}    {filename}    -    -    -    -    File not found")
                    continue
                
                # Read file content
                with open(filename, 'rb') as f:
                    file_content = f.read()
                
                # Check if file is too large for RSA
                if len(file_content) > 200:  # Leave some buffer for base64 encoding
                    print(f"{file_type}    {filename}    -    -    -    -    File too large ({len(file_content)}B)")
                    continue
                
                # Get initial CPU/Memory
                cpu_before, mem_before = self.get_cpu_memory_usage()
                
                # Encrypt (convert to base64 for text handling)
                file_content_b64 = base64.b64encode(file_content).decode('utf-8')
                encrypted, enc_time = self.encrypt_message(public_key, file_content_b64)
                
                # Decrypt
                decrypted, dec_time = self.decrypt_message(private_key, encrypted)
                
                # Get final CPU/Memory
                cpu_after, mem_after = self.get_cpu_memory_usage()
                cpu_usage = max(cpu_before, cpu_after)
                
                # Verify by comparing base64 decoded content
                decrypted_bytes = base64.b64decode(decrypted.encode('utf-8'))
                status = "OK" if file_content == decrypted_bytes else "FAIL"
                
                print(f"{file_type}    {filename}    {enc_time:.6f}    {dec_time:.6f}    {cpu_usage:.2f}    {mem_after}    {status}")
                
            except Exception as e:
                print(f"{file_type}    {filename}    -    -    -    -    ERROR: {str(e)}")
    
    def create_sample_files(self):
        """Create small sample test files that can be encrypted with RSA"""
        sample_files = {
            "small_sample.txt": "This is a small text file for RSA testing.",
            "small_sample.png": b"SmallPNG" * 10,  # 80 bytes
            "small_sample.pdf": b"SmallPDF" * 10   # 80 bytes
        }
        
        for filename, content in sample_files.items():
            if not os.path.exists(filename):
                try:
                    if isinstance(content, str):
                        with open(filename, 'w') as f:
                            f.write(content)
                    else:
                        with open(filename, 'wb') as f:
                            f.write(content)
                    print(f"Created sample file: {filename} ({len(content)} bytes)")
                except Exception as e:
                    print(f"Error creating {filename}: {e}")

def main():
    print("Microsoft Windows [Version 10.0.22631.5909]")
    print("(c) Microsoft Corporation. All rights reserved.")
    print()
    print("C:\\Users\\HP\\Desktop\\Crypto>python testing.py")
    print()
    
    tester = RSA_Performance_Tester()
    
    # Create sample files for testing
    tester.create_sample_files()
    print()
    
    # Run all tests
    tester.test_key_sizes()
    tester.test_data_sizes() 
    tester.test_file_types()
    
    print()
    print("C:\\Users\\HP\\Desktop\\Crypto>")

if __name__ == "__main__":
    main()