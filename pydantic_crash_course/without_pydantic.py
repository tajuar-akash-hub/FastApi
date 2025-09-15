
def print_patient_data(name:str,age:int):
    # Suppose printing is equalvant to inserted to database
    if(type(name) == str and type(age) == int):
        print(name)
        print(age)
        print("Inserted into Database")
    else :
        raise TypeError("Please Insert valid data types")
    
def update_patient_data(name:str,age:int):
    # Suppose printing is equalvant to update
    if(type(name) == str and type(age) == int):
        print(name)
        print(age)
        print("Updated the Database")
    else :
        raise TypeError("Please Insert valid data types")

update_patient_data("Mahir",30)



