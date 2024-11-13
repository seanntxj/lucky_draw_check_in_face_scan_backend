'''
Organises the mess of images that Microsoft Forms creates.
Images are stored in folders of the employee's ID. 
'''

import csv
import os
import shutil

'''
Read csv files, return the first line (headers) and the rest of lines in this format
[[headers], [[line1], [line2], ...]
'''
def csv_read(file):
    f = open(file=file, mode='r')
    csv_f = csv.reader(f)
    csv_f_contents = [] 
    for line in csv_f: 
        csv_f_contents.append(line)
    f.close()
    return csv_f_contents[0], csv_f_contents[1:]

'''
Takes in the Microsoft Forms csv file and organizes the images into folders based on their employee ID
'''
def organize_dataset(images_file_path_root, training_dataset_path_root, csv_file_path, name_mapping):
    csv_contents = csv_read(csv_file_path)
    persons = csv_contents[1]
    headers = csv_contents[0]

    for person in persons:
        employee_id = person[5]
        wears_glasses = person[8] == 'Yes'
        
        column_to_start_from = 9 if wears_glasses else 14
        for i in range(column_to_start_from, len(person)):
            
            img_file_path = person[i].replace('%20', ' ').split('/') # Replace link spaces with actual spaces
            img_file_path = os.path.join(img_file_path[len(img_file_path)-2], img_file_path[len(img_file_path)-1]) # Get the image file path
            img_file_path = os.path.join(images_file_path_root, img_file_path)
            img_output_file_name, ext = os.path.splitext(os.path.basename(img_file_path))

            # Prepend if any employee id is wrong format
            if len(employee_id) == 4:
                employee_id = '0' + employee_id

            # check if person is in name_mapping dictionary
            if employee_id not in name_mapping:
                print(f'WARN: {employee_id} NO name')
                continue    


            person_dataset_folder_path = os.path.join(training_dataset_path_root, f'{employee_id}+{name_mapping[employee_id]}')
            if not os.path.exists(person_dataset_folder_path):
                os.makedirs(person_dataset_folder_path)
            
            if i == 9: 
                img_output_file_name = 'front_g'
            elif i == 10:
                img_output_file_name = 'left_g'
            elif i == 11:
                img_output_file_name = 'right_g'
            elif i == 12:
                img_output_file_name = 'top_g'
            elif i == 13:
                img_output_file_name = 'bottom_g'
            elif i == 14: 
                img_output_file_name = 'front'
            elif i == 15:
                img_output_file_name = 'left'
            elif i == 16:
                img_output_file_name = 'right'
            elif i == 17:
                img_output_file_name = 'top'
            elif i == 18:
                img_output_file_name = 'bottom'

            if person[i] == '':
                print(f'WARN: {employee_id} NO {img_output_file_name}')
                continue    

            # print(img_file_path)
            save_item = os.path.join(person_dataset_folder_path, img_output_file_name + ext) 
            os.path.exists(os.path.dirname(person_dataset_folder_path))
            try:
                shutil.copy(img_file_path, save_item)
            except FileNotFoundError as e:
                print('Cannot find ' + e.filename)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('csv_file_path', type=str, help='File path to CSV file from MS Forms')
    # parser.add_argument('images_file_path_root', type=str, help='Downloaded Onedrive folder from MS Forms')
    # parser.add_argument('training_dataset_path_root', type=str, help='Output folder')
    # args = parser.parse_args()
    # csv_file_path = args.csv_file_path
    # images_file_path_root = args.images_file_path_root
    # training_dataset_path_root = args.training_dataset_path_root


    csv_file_path_forms = "./msforms_organizer_files/forms.csv"
    images_file_path_root = "./msforms_organizer_files/forms_images"
    training_dataset_path_root = "./msforms_organizer_files/forms_images_output"
    csv_file_path_name_mapping = "./msforms_organizer_files/name_mapping.csv"

    # get name mapping
    raw_csv_output = csv_read(csv_file_path_name_mapping)

    name_mapping = {}
    for row in raw_csv_output[1]:
        empid = row[2]
        name = row[1]
        name_mapping[empid] = name

    print(name_mapping)
    organize_dataset(images_file_path_root, training_dataset_path_root, csv_file_path_forms, name_mapping)
    print('Done')