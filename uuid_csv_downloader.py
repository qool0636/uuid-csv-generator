import uuid
import pandas as pd
import os
from datetime import datetime

def generate_sample_data(uuid_str):
    """Generate sample data related to UUID"""
    # Generate some random data
    data1 = {
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 5,
        'value': [uuid.uuid4().int % 1000 for _ in range(5)],
        'category': ['A', 'B', 'C', 'D', 'E']
    }
    
    data2 = {
        'id': [uuid.uuid4().hex[:8] for _ in range(3)],
        'status': ['active', 'pending', 'completed'],
        'score': [85, 92, 78]
    }
    
    data3 = {
        'date': [datetime.now().strftime('%Y-%m-%d')] * 4,
        'amount': [1000, 2000, 3000, 4000],
        'type': ['income', 'expense', 'income', 'expense']
    }
    
    return data1, data2, data3

def download_csv_files(uuid_str):
    """Generate and download three related CSV files based on UUID"""
    # Create download directory
    download_dir = 'downloads'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Generate sample data
    data1, data2, data3 = generate_sample_data(uuid_str)
    
    # Create DataFrame and save as CSV
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)
    
    # Generate file names
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename1 = f'{download_dir}/data1_{uuid_str[:8]}_{timestamp}.csv'
    filename2 = f'{download_dir}/data2_{uuid_str[:8]}_{timestamp}.csv'
    filename3 = f'{download_dir}/data3_{uuid_str[:8]}_{timestamp}.csv'
    
    # Save CSV files
    df1.to_csv(filename1, index=False)
    df2.to_csv(filename2, index=False)
    df3.to_csv(filename3, index=False)
    
    return filename1, filename2, filename3

def main():
    print("Welcome to UUID CSV File Downloader!")
    while True:
        uuid_str = input("Please enter UUID (or enter 'q' to quit): ")
        if uuid_str.lower() == 'q':
            break
            
        try:
            # Validate UUID format
            uuid_obj = uuid.UUID(uuid_str)
            print(f"\nProcessing UUID: {uuid_str}")
            
            # Download files
            file1, file2, file3 = download_csv_files(uuid_str)
            
            print("\nFiles generated successfully:")
            print(f"1. {file1}")
            print(f"2. {file2}")
            print(f"3. {file3}")
            print("\nFiles saved in 'downloads' directory")
            
        except ValueError:
            print("Error: Invalid UUID format, please try again")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 