import time

def trigger_job(data):
    # Perform the job operations using the data
    print("sleeping for 30 seconds")
    time.sleep(30)
    print(f"Job triggered with data: {data}")
    # Add your job logic here
