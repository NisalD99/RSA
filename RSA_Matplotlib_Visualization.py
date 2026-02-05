import matplotlib.pyplot as plt
import numpy as np

# Sample data (you can replace this with your actual performance test results)
key_sizes = [1024, 2048, 3072, 4096]
encryption_times = [0.000395, 0.000668, 0.002188, 0.001946]
decryption_times = [0.001734, 0.003345, 0.009623, 0.017343]

data_sizes = [32, 100]
data_enc_times = [0.001145, 0.001256]
data_dec_times = [0.003330, 0.003340]

file_types = ['txt', 'png', 'pdf']
file_enc_times = [0.001234, 0.001345, 0.001456]
file_dec_times = [0.003456, 0.003567, 0.003678]

def create_performance_vs_key_size():
    """Create Performance vs Key Size chart"""
    plt.figure(figsize=(10, 6))
    
    # Plot lines for encryption and decryption times
    plt.plot(key_sizes, encryption_times, 'bo-', linewidth=2, markersize=8, label='Encryption Time')
    plt.plot(key_sizes, decryption_times, 'ro-', linewidth=2, markersize=8, label='Decryption Time')
    
    # Chart styling
    plt.title('RSA Performance vs Key Size', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Key Size (bits)', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Set x-axis ticks to show exact key sizes
    plt.xticks(key_sizes)
    
    # Remove top and right spines for cleaner look
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('performance_vs_key_size.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_performance_vs_data_size():
    """Create Performance vs Input Data Size chart"""
    plt.figure(figsize=(10, 6))
    
    # Plot lines for encryption and decryption times
    plt.plot(data_sizes, data_enc_times, 'bo-', linewidth=2, markersize=8, label='Encryption Time')
    plt.plot(data_sizes, data_dec_times, 'ro-', linewidth=2, markersize=8, label='Decryption Time')
    
    # Chart styling
    plt.title('RSA Performance vs Input Data Size (2048-bit Key)', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Data Size (bytes)', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Set x-axis ticks to show exact data sizes
    plt.xticks(data_sizes)
    
    # Remove top and right spines for cleaner look
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('performance_vs_data_size.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_performance_by_file_type():
    """Create Performance by File Type chart"""
    plt.figure(figsize=(10, 6))
    
    # Set the width of the bars and positions
    bar_width = 0.35
    x_pos = np.arange(len(file_types))
    
    # Create bars for encryption and decryption times
    plt.bar(x_pos - bar_width/2, file_enc_times, bar_width, label='Encryption Time', 
            color='blue', alpha=0.7)
    plt.bar(x_pos + bar_width/2, file_dec_times, bar_width, label='Decryption Time', 
            color='red', alpha=0.7)
    
    # Chart styling
    plt.title('RSA Performance by File Type', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('File Type', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, axis='y')
    
    # Set x-axis ticks to show file types
    plt.xticks(x_pos, file_types)
    
    # Remove top and right spines for cleaner look
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('performance_by_file_type.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    print("Generating RSA Performance Charts...")
    print("="*50)
    
    # Generate all three charts
    create_performance_vs_key_size()
    create_performance_vs_data_size()
    create_performance_by_file_type()
    
    print("All charts generated successfully!")
    print("Saved files:")
    print("- performance_vs_key_size.png")
    print("- performance_vs_data_size.png")
    print("- performance_by_file_type.png")

if __name__ == "__main__":
    main()