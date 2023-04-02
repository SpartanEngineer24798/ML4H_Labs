import os
import csv
import shutil

# Path to the folder where the patient folders will be created
output_folder_path = '/home/nyuad/Desktop/ovarian'

# Open the CSV file and create a dictionary to store the patient data
with open('Ovarian_labels.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    patient_data = {}
    for row in reader:
        patient_id = row['Patient ID']
        if patient_id not in patient_data:
            patient_data[patient_id] = []
        patient_data[patient_id].append(row)

# Loop through the patient data dictionary and create a folder for each patient
for patient_id, data in patient_data.items():
    folder_path = os.path.join(output_folder_path, patient_id)
    os.makedirs(folder_path, exist_ok=True)

    # Loop through the patient data and move the corresponding image file into the folder
    for row in data:
    	# Remove the file extension from the image filename
        image_filename = os.path.splitext(row['Image No.'])[0]
        
        # Check if the image file exists in the images folder
        image_path = os.path.join('/home/nyuad/Desktop/ovarian_features/h5_files', f"{image_filename}.h5")

        if os.path.exists(image_path):
            # Move the image file to the patient folder
            image_dest_path = os.path.join(folder_path, f"{row['Image No.']}.h5")
            shutil.move(image_path, image_dest_path)
        else:
            print(f"Image file {image_filename}.h5 not found.")
