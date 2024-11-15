import streamlit as st
import mysql.connector
import re

# Database connection
con = mysql.connector.connect(
    host="localhost", user="root", password="", database="employee"
)
mycursor = con.cursor()

# Regular expressions for validation
regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex_phone = r"(0|91)?[7-9][0-9]{9}"


def add_employee():
    st.subheader("Add Employee")
    with st.form("Add Employee Form"):
        Id = st.text_input("Enter Employee ID")
        Name = st.text_input("Enter Employee Name")
        Email_Id = st.text_input("Enter Employee Email")
        Phone_no = st.text_input("Enter Employee Phone Number")
        Address = st.text_input("Enter Employee Address")
        Post = st.text_input("Enter Employee Post")
        Salary = st.text_input("Enter Employee Salary")
        submitted = st.form_submit_button("Add Employee")

        if submitted:
            # Validation
            if not re.fullmatch(regex_email, Email_Id):
                st.error("Invalid Email Address!")
                return
            if not re.fullmatch(regex_phone, Phone_no):
                st.error("Invalid Phone Number!")
                return
            # Check if Employee ID exists
            if check_employee_id(Id):
                st.error("Employee ID already exists!")
                return
            # Insert data
            sql = 'INSERT INTO empdata VALUES (%s, %s, %s, %s, %s, %s, %s)'
            data = (Id, Name, Email_Id, Phone_no, Address, Post, Salary)
            mycursor.execute(sql, data)
            con.commit()
            st.success("Employee added successfully!")


def display_employees():
    st.subheader("Display Employees")
    mycursor.execute("SELECT * FROM empdata")
    records = mycursor.fetchall()
    if records:
        for record in records:
            st.write(f"**ID:** {record[0]}")
            st.write(f"**Name:** {record[1]}")
            st.write(f"**Email:** {record[2]}")
            st.write(f"**Phone:** {record[3]}")
            st.write(f"**Address:** {record[4]}")
            st.write(f"**Post:** {record[5]}")
            st.write(f"**Salary:** {record[6]}")
            st.write("---")
    else:
        st.warning("No employees found.")


def update_employee():
    st.subheader("Update Employee")
    with st.form("Update Employee Form"):
        Id = st.text_input("Enter Employee ID to Update")
        Email_Id = st.text_input("Enter New Email")
        Phone_no = st.text_input("Enter New Phone Number")
        Address = st.text_input("Enter New Address")
        submitted = st.form_submit_button("Update Employee")

        if submitted:
            if not check_employee_id(Id):
                st.error("Employee ID does not exist!")
                return
            if not re.fullmatch(regex_email, Email_Id):
                st.error("Invalid Email Address!")
                return
            if not re.fullmatch(regex_phone, Phone_no):
                st.error("Invalid Phone Number!")
                return
            sql = "UPDATE empdata SET Email_Id = %s, Phone_no = %s, Address = %s WHERE Id = %s"
            data = (Email_Id, Phone_no, Address, Id)
            mycursor.execute(sql, data)
            con.commit()
            st.success("Employee updated successfully!")


def promote_employee():
    st.subheader("Promote Employee")
    with st.form("Promote Employee Form"):
        Id = st.text_input("Enter Employee ID")
        Increase_Salary = st.number_input("Enter Increase in Salary", step=1.0)
        submitted = st.form_submit_button("Promote Employee")

        if submitted:
            if not check_employee_id(Id):
                st.error("Employee ID does not exist!")
                return
            sql = "SELECT Salary FROM empdata WHERE Id = %s"
            mycursor.execute(sql, (Id,))
            current_salary = mycursor.fetchone()
            if current_salary:
                new_salary = current_salary[0] + Increase_Salary
                sql_update = "UPDATE empdata SET Salary = %s WHERE Id = %s"
                mycursor.execute(sql_update, (new_salary, Id))
                con.commit()
                st.success("Employee promoted successfully!")
            else:
                st.error("Error fetching employee salary.")


def remove_employee():
    st.subheader("Remove Employee")
    with st.form("Remove Employee Form"):
        Id = st.text_input("Enter Employee ID to Remove")
        submitted = st.form_submit_button("Remove Employee")

        if submitted:
            if not check_employee_id(Id):
                st.error("Employee ID does not exist!")
                return
            sql = "DELETE FROM empdata WHERE Id = %s"
            mycursor.execute(sql, (Id,))
            con.commit()
            st.success("Employee removed successfully!")


def search_employee():
    st.subheader("Search Employee")
    with st.form("Search Employee Form"):
        Id = st.text_input("Enter Employee ID to Search")
        submitted = st.form_submit_button("Search Employee")

        if submitted:
            sql = "SELECT * FROM empdata WHERE Id = %s"
            mycursor.execute(sql, (Id,))
            record = mycursor.fetchone()
            if record:
                st.write(f"**ID:** {record[0]}")
                st.write(f"**Name:** {record[1]}")
                st.write(f"**Email:** {record[2]}")
                st.write(f"**Phone:** {record[3]}")
                st.write(f"**Address:** {record[4]}")
                st.write(f"**Post:** {record[5]}")
                st.write(f"**Salary:** {record[6]}")
            else:
                st.error("Employee not found.")


def check_employee_id(employee_id):
    sql = "SELECT * FROM empdata WHERE Id = %s"
    mycursor.execute(sql, (employee_id,))
    return mycursor.fetchone() is not None


# Streamlit App Interface
st.title("Employee Management System")

menu_options = [
    "Add Employee",
    "Display Employees",
    "Update Employee",
    "Promote Employee",
    "Remove Employee",
    "Search Employee",
]
choice = st.sidebar.selectbox("Menu", menu_options)

if choice == "Add Employee":
    add_employee()
elif choice == "Display Employees":
    display_employees()
elif choice == "Update Employee":
    update_employee()
elif choice == "Promote Employee":
    promote_employee()
elif choice == "Remove Employee":
    remove_employee()
elif choice == "Search Employee":
    search_employee()
