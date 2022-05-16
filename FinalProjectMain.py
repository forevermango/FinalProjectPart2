"""
Name:Raahima Ahmed
Student ID:1892523
    
"""

#   Importing required libraries
import sys
import datetime
import FinalProjectStudentClass
from FinalProjectInput import read_all_inputs
import FinalProjectOutput

#function that finds the closets gpa the user enters in the query
def closest(list, Number):
    aux = []
    for valor in list:
        aux.append(abs(Number-valor))
    
    return aux.index(min(aux))


if __name__ == "__main__":
    
    #   input csv file names
    #mentioning file names from project 1 and 2, initializing variable names for output files
    students_data_filename = "StudentsMajorsList.csv"
    gpa_filename = "GPAList.csv"
    graduation_date_filename = "GraduationDatesList.csv"
    
    #   output csv file names
    out_filename1 = 'FullRoster.csv'
    out_filename2 = 'ScholarshipCandidates.csv'
    out_filename3 = 'DisciplinedStudents.csv'
    
    #   creating lists and dictionary to hold data
    existing_majors = []
    student_objects = []
    students_dictionary = {}
    
    
    #   Reading data from csv files by calling function in FinalProjectInput.py
    students_data, gpa_data, graduation_date_data = read_all_inputs(students_data_filename, gpa_filename, graduation_date_filename)
    #not we have the data
    #   reading all rows in students_data
    for row in students_data:
        #   converting data types from string to required
        ID = int(row[0])
        last_name = row[1]
        first_name = row[2]
        major = row[3]
        disciplinary_action = row[4]

        #   getting and saving unique majors
        if major not in existing_majors:
            #if list does not exist then append to unique major name
            existing_majors.append(major)
            
        #   creating dictionary
        # key is the ID of the student
        students_dictionary[ID] = {'last_name': last_name,
                                   'first_name': first_name,
                                   'major': major,
                                   'disciplinary_action': disciplinary_action,
                                   'gpa': 0,
                                   #have to compare grad date with todays date
                                   'graduation_date': '',
                                   #converts graduation date to a format that can compare it to todays date
                                   'date_format': ''}
    
    
    #   reading all rows in gpa_data
    # moving through each for of GPA data file and gathering ID and gpa, and saving gpa attribute
    for row in gpa_data:
        #   converting data types from string to required
        ID = int(row[0])
        gpa = float(row[1])
        
        #   saving to dictionary
        try:
            students_dictionary[ID]['gpa'] = gpa
        except:
            print(f'No such student exist with ID: {ID}')
            sys.exit()
    
    
    #   reading all rows in graduation_date_data
    for row in graduation_date_data:
        #   converting data types from string to required
        ID = int(row[0])
        graduation_date = row[1]
        
        #   saving to dictionary
        try:
            students_dictionary[ID]['graduation_date'] = graduation_date
            
            #   converting date to date type object format
            # as we importaed the date time library we are converting the date into the date time object and getting another attribute that we created initially which is date format
            date = graduation_date.split('/')
            date_format = datetime.date(int(date[2]),int(int(date[0])),int(int(date[1])))
            students_dictionary[ID]['date_format'] = date_format
            
    
        except:
            print(f'No such student exist with ID: {ID}')
            sys.exit()
            
    
    #   creating Student class objects from data
    # student dictionary contains the key(ID) and values are the dictionaries which contain the attrbutes listing
    for ID in students_dictionary:
        student_obj = FinalProjectStudentClass.Student(ID,
                                                       students_dictionary[ID]['last_name'], 
                                                       students_dictionary[ID]['first_name'], 
                                                       students_dictionary[ID]['major'], 
                                                       students_dictionary[ID]['disciplinary_action'], 
                                                       students_dictionary[ID]['gpa'], 
                                                       students_dictionary[ID]['graduation_date'])
        #appending all the objects in students object list
        student_objects.append(student_obj)
    #   Creating Processed Inventory Reports
    #   (a) Creating FullRoster.csv 
    #   sorting alphabetically by student last name
    #   lambda was used in project 1
    #saving the sorted data on the basis of last_name into the full_roster_rows variable
#    full_roster = sorted(students_dictionary.items(), key = lambda x: x[1]['last_name'])
    full_roster_rows = []
    #   getting required attributes
    # getting the full_roster data and sending it to FinalProjectOutput.py then creating a new csv file named as out_filename1
    """for row in full_roster:
        student_ID = row[0]
        major = row[1]['major']
        first_name = row[1]['first_name']
        last_name = row[1]['last_name']
        gpa = row[1]['gpa']
        graduation_date = row[1]['graduation_date']
        disciplinary_action = row[1]['disciplinary_action']
        full_roster_rows.append([student_ID, major, first_name, last_name, gpa, graduation_date, disciplinary_action])"""
    #   writing to FullRoster.csv 
    FinalProjectOutput.write_csv(out_filename1, full_roster_rows)
    #   (b) Creating List per major
    #   for each unique major
    for major in existing_majors:
        #   creating file name
        filename = major.replace(' ', '')
        filename += 'Students.csv'
        
        #   getting data of a particular major
        data = {}

        #looking through the dictionary and taking all the students data with this particular major
        for key in students_dictionary:
            if students_dictionary[key]['major'] == major:
                data[key] = students_dictionary[key]
          
        #   getting only required attributes
        major_rows = []
        for ID in sorted(data):
            last_name = data[ID]['last_name']
            first_name = data[ID]['first_name']
            graduation_date = data[ID]['graduation_date']
            disciplinary_action = data[ID]['disciplinary_action']
            
            major_rows.append([ID, last_name, first_name, graduation_date, disciplinary_action])
        
        #   Saving data of particular major to its particular csv file
        FinalProjectOutput.write_csv(filename, major_rows)

    #   (c) Creating ScholarshipCandidates.csv
    
    #   creating dict to hold scholarship_data, and list  scholarship_rows
    scholarship_data = {}
    scholarship_rows = []
    #   getting today's date
    todays_date = datetime.date.today()

    #looping through all the students who have not graduated
    #   checking if gpa is greater than 3.8
    for ID in students_dictionary:
        if students_dictionary[ID]['gpa'] > 3.8:
            
            #   checking if graduation_date is not passed yet and no disciplinary_action exists
            date = students_dictionary[ID]['graduation_date'].split('/')
            graduation_date = datetime.date(int(date[2]),int(int(date[0])),int(int(date[1])))
            
            #   then saving students data for scholarship
            if (graduation_date > todays_date) and (students_dictionary[ID]['disciplinary_action'] == ''):
                scholarship_data[ID] = students_dictionary[ID]
    
    #   sorting based on gpa
  #  scholarship_data_sorted = sorted(scholarship_data.items(), key = lambda x: x[1]['gpa'], reverse=True)

    #   Picking only required attributes
"""    for row in scholarship_data_sorted:
        student_ID = int(row[0])
        last_name = row[1]['last_name']
        first_name = row[1]['first_name']
        major = row[1]['major']
        gpa = row[1]['gpa']
"""
#       scholarship_rows.append([student_ID, last_name, first_name, major, gpa])

    #   writing data to ScholarshipCandidates.csv, calling csv function to save the data into out_filename2 csv file
 #   FinalProjectOutput.write_csv(out_filename2, scholarship_rows)


    #   (d) Creating DisciplinedStudents.csv

    #   Sorting data based on dates from old to new
 #   disciplined_rows = []
 #   date_sorted = sorted(students_dictionary.items(), key = lambda x: x[1]['date_format'])

    #   Iterating through each row
"""    for row in date_sorted:
        disciplinary_action = row[1]['disciplinary_action']"""
        
        #   checking if disciplinary_action exists
"""        if disciplinary_action != "":
            #   if yes then Picking only required attributes
            student_ID = int(row[0])
            last_name = row[1]['last_name']
            first_name = row[1]['first_name']
            graduation_date = row[1]['graduation_date']
            
            disciplined_rows.append([student_ID, last_name, first_name, graduation_date])"""
    
    #   writing to DisciplinedStudents.csv
   # FinalProjectOutput.write_csv(out_filename3, disciplined_rows)
    
    ###################Final Project Starts###############

    #   Creating header to display results    
#    header = ["ID", "first name", "last item", "GPA"]
    
    #   Displaying Inventory area to screen
print("\n\n===========================================")
print("             Inventory Query               ")
print("===========================================")
    
    #   creating query menu
    #infinite file loop until user enters q
query_prompt = ("\n1. Make a query\n"
                "q. Quit\n\n"
                "Enter your choice: ")

#   asking query until user quits
while True:
        
    #   Displaying query menu from lines 253 to 255
    command = input(query_prompt).lower().strip()
        
    #   if user selects 1, take single query from user
    if command == "1":
            
        #   asking query from user
        major_gpa = input("Enter the space separated major and GPA for query (e.g “Computer Science 3.5”): ").strip()
        #seperating major and gpa
        major_gpa = major_gpa.split(" ")
            
        #   getting gpa part from entered query
        try:
            #converting gpa to a floating point number
            gpa_entered = float(major_gpa[-1])
        except:
            print('Invalid GPA entered.')
            sys.exit()
                
                
        #   getting entered major from query
        major_entered = major_gpa[:-1]
        major_entered = " ".join(major_entered)
            
        selected_major = ""
        count = 0
        
        #   checking if query contains more than 1 major or gpa
        #looping through all the majors and keeping track of what major the user entered
        for major in existing_majors:
            if major in major_entered:
                count += 1
                selected_major = major
                    
            
            #   finding students from roster based on query
            # making sure major is not empty and only one major is mentioned
            if (selected_major != "") and (count == 1):

                # creating a new list to keep track of majors mentioned
                #   lists to hold matched students
                actual_students = []
                may_consider_students = []
                
                existing_gpas = {}
                
                #   looping through each student
                for ID in students_dictionary:
                    
                    #   checking if has same major
                    if students_dictionary[ID]['major'] == selected_major:
                        
                        #   checking if no disciplinary action is taken and haven't graduated yet
                        if (students_dictionary[ID]['disciplinary_action'] == '') and (students_dictionary[ID]['date_format'] > todays_date):


                            #   getting gpa if requiremnts are satisfied
                            current_gpa = students_dictionary[ID]['gpa']

                            #storing the gpas
                            if current_gpa not in existing_gpas.keys():
                                existing_gpas[current_gpa] = [ID]
                            else:
                                existing_gpas[current_gpa].append(ID)
                            
                            #   checking if gpa exactly matches withing gpa entered in the query or within 0.1 to keep them in the actual_students list created previously
                            if (current_gpa == gpa_entered) or (current_gpa == gpa_entered+0.1) or ((current_gpa == gpa_entered-0.1)):
                                fname = students_dictionary[ID]['first_name']
                                lname = students_dictionary[ID]['last_name']
                                gpa = students_dictionary[ID]['gpa']
                                
                                #   getting student's data
                                actual_students.append([ID, fname, lname, gpa])
                            
                            #   or checking if gpa is within 0.25
                            if (current_gpa == gpa_entered+0.25) or ((current_gpa == gpa_entered-0.25)):
                                fname = students_dictionary[ID]['first_name']
                                lname = students_dictionary[ID]['last_name']
                                gpa = students_dictionary[ID]['gpa']
                                
                                #   getting student's data who we may also consider for scholorship
                                may_consider_students.append([ID, fname, lname, gpa])
                        
                        
                #   If there were no students who satisfied neither ii nor iii
                # taking the student name that has the closest gpa from the entered gpa
                if (len(actual_students)==0) and (len(may_consider_students)==0):
                    
                    #   getting all students gpas where major is same 
                    #   and no disciplinary action is taken and haven't graduated yet
                    existing_gpas_list = list(existing_gpas.keys())
                    
                    if len(existing_gpas_list) > 0:
                        
                        #   finding closest gpa, calling the function created above
                        index_closest = closest(existing_gpas_list, gpa_entered)
                        
                        closest_gpa = existing_gpas_list[index_closest]
                        
                        #   getting students with this gpa and criteria
                        # taking all the students who have this closest gpa
                        closest_students = existing_gpas[closest_gpa]
                        closest_students_lists = []
                        for ID in closest_students:
                            fname = students_dictionary[ID]['first_name']
                            lname = students_dictionary[ID]['last_name']
                            gpa = students_dictionary[ID]['gpa']
                            
                            closest_students_lists.append([ID, fname, lname, gpa])
                            
                        #   Displaying students meeting the criteria
                        # formating into a table
                        print("\n\nClosest student:")
                        print("-"*85)
                        print("{: >20} {: >20} {: >20} {: >20}".format(*header))
                        for row in closest_students_lists:
                            print("{: >20} {: >20} {: >20} {: >20}".format(*row))
                            
                    #   Otherwise displaying no such student exists      
                    else:
                        print("\nNo such student.")
                
                #   If there exist students who satisfied either ii or iii
                else:
                    #   Displaying students who are exact same gpa or within 0.1
                    print("\n\nYour student(s):")
                    print("-"*85)
                    print("{: >20} {: >20} {: >20} {: >20}".format(*header))
                    for row in actual_students:
                        print("{: >20} {: >20} {: >20} {: >20}".format(*row))
                    
                    #   Displaying students whose gpa is within 0.25
                    print("\n\nYou may, also, consider::")
                    print("-"*85)
                    print("{: >20} {: >20} {: >20} {: >20}".format(*header))
                    for row in may_consider_students:
                        print("{: >20} {: >20} {: >20} {: >20}".format(*row))
            #   Otherwise displaying no such student exists               
            else:
                print("\nNo such student.")
        #   Quitting the program if user enters q
        
    elif command == "q":
        break
        
        #   Displaying this message if user enters wrong choice
    else:
        print("Invalid choice!")
            
    
    







        
        
        
        
        
        
        
        
    


    


