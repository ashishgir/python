from tkinter import *
import os
from tkinter import ttk
import tkinter as tk
import plotly.plotly as py
import plotly.graph_objs as go
from pandas import DataFrame
import pyodbc
import pandas as pd
from pygments.lexers import go
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import backend
import numpy as np


def delete2():
    screen3.destroy()
    home()

def delete3():
    screen4.destroy()

def delete4():
    screen5.destroy()

def login_success():
    global screen3
    screen3 = Toplevel(screen)
    screen3.title("Success")
    screen3.geometry("150x100")
    Label(screen3, text = "Login Success!").pack()
    Label(screen3, text = "").pack()
    Button(screen3, text = "OK", command = delete2).pack()

def home():
    global screen5
    arr=[]
    arr1=[]
    screen5 = Tk()
    screen5.geometry("1400x700")
    screen5.title("Home Page - COVID 19")
    Label(screen5, text="Home Page - COVID 19", bg="grey", width="300", height="2", font=("Calibri", 13)).pack()
    Label(screen5,text="").pack()
    Label(screen5, text="Please Select Country and State to generate COVID Report").pack()
    Label(screen5,text="").pack()
    variable = StringVar(screen5)
    variable.set("Select a Country")  # default value
    values=backend.GetCountry()
    for val in values:
        arr.append(val[0])
    w = OptionMenu(screen5, variable,*arr)
    w.config(width=40, font=('Helvetica', 12))
    w.pack()
    SelectedCountry=variable.get()
    Label(screen5, text="").pack()
    variable1 = StringVar(screen5)
    variable1.set("Select a State")  # default value
    values1 = backend.GetStates()
    arr1.append('Select a State')
    for val1 in values1:
        arr1.append(val1[0])
    w1 = OptionMenu(screen5, variable1, *arr1)
    w1.config(width=40, font=('Helvetica', 12))
    w1.pack()
    SelectedState=variable1.get()
    Label(screen5, text="").pack()

    def ViewData():
        SelectedState = variable1.get()
        SelectedCountry = variable.get()
        def new():

            rows = backend.GetListByCountryandState(SelectedCountry,SelectedState)
            for row in rows:
                print(row)  # it print all records in the database
                tree.insert("", tk.END, values=row)


        root = tk.Tk()
        root.geometry("1500x400")

        tree = ttk.Treeview(root, column=("column1", "column2", "column3","column4","column5","column6","column7","column8"), show='headings')
        tree.heading("#1", text="SNo")
        tree.heading("#2", text="ObservationDate")
        tree.heading("#3", text="State")
        tree.heading("#4", text="Country")
        tree.heading("#5", text="Last_Update")
        tree.heading("#6", text="Confirmed")
        tree.heading("#7", text="Deaths")
        tree.heading("#8", text="Recovered")
        tree.pack()
        b2 = tk.Button(root, text="view data", command=new)
        b2.pack()

        root.mainloop()

    def ShowGraph():
        SelectedState=variable1.get();
        SelectedCountry=variable.get()
        rows=backend.GetListByCountryandState(SelectedCountry,SelectedState)
        arr=[]
        con=[]
        for r in rows:
            arr.append(r[6])
            con.append(r[5])

        data1 = {'Deaths': arr,
                 'Confirmed': con}
        df1 = DataFrame(data1, columns=['Deaths', 'Confirmed'])
        df1 = df1.astype(float)
        print(df1)

        root = tk.Tk()

        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df1 = df1[['Deaths', 'Confirmed']].groupby('Deaths').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Deaths Vs. Confirmed')

        root.mainloop()
    def Download():
        SelectedState = variable1.get();
        SelectedCountry = variable.get()
        rows = backend.GetListByCountryandState(SelectedCountry, SelectedState)
        query="Select * from [Covid].[dbo].[covid_19_data] WHERE Country like '"+SelectedCountry+"' and State like '"+SelectedState+"'"
        sql_conn = pyodbc.connect("DRIVER={SQL Server};server=DESKTOP-SDDF15J;database=Covid;Trusted_Connection=yes;")
        df = pd.read_sql(query, sql_conn)
        print(df)
        df.to_excel(r'D:\Ashish MS FIles\Python\Project\files\export_dataframe.xlsx', index=False, header=True)
    def Reports():

    Label(screen5, text="").pack()
    Button(screen5, text="ShowDetails", height="2", width="30", command=ViewData).pack()
    Label(screen5, text="").pack()
    Button(screen5, text="ShowGraph", height="2", width="30", command=ShowGraph).pack()
    Label(screen5, text="").pack()
    Button(screen5, text="Download Data", height="2", width="30", command=Download).pack()
    Label(screen5, text="").pack()
    Button(screen5, text="Reports", height="2", width="30", command=Reports).pack()
    screen5.mainloop()

def incorrect_password():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title("Error")
    screen4.geometry("150x100")
    Label(screen4, text = "Incorrect Password").pack()
    Label(screen4, text = "").pack()
    Button(screen4, text = "OK", command = delete3).pack()

def user_not_found():
    global screen5
    screen5 = Toplevel(screen)
    screen5.title("Error")
    screen5.geometry("150x100")
    Label(screen5, text = "User is not found!").pack()
    Label(screen5, text = "").pack()
    Button(screen5, text = "OK", command = delete4).pack()

def register_user():
    username_info = username.get()
    password_info = password.get()
    SelectedRadio=var.get()
    backend.InsertUser(username_info,password_info,SelectedRadio)

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(screen1, text = "Registration Success", fg = "green", font = ("Calibri", 11)).pack()

def login_verify():
    count=0
    username1 = username_verify.get()
    password1 = password_verify.get()

    dbcheck=backend.VerifyUser(username1,password1)
    for rows in dbcheck:
        count=count+1

    if count == 0:
        user_not_found()
    else:
        login_success()

    username_entry1. delete(0, END)
    password_entry1.delete(0, END)
def login_verify_admin():
    count = 0
    username1 = username_verify.get()
    password1 = password_verify.get()
    IsAdmin=0

    dbcheck = backend.VerifyUser(username1, password1)
    for rows in dbcheck:
        count = count + 1
        if rows[3] ==1:
            IsAdmin=1
    if IsAdmin==0:
        count=0
    if count == 0 :
        user_not_found()
    else:
        register()
    username_entry1.delete(0, END)
    password_entry1.delete(0, END)

def register():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("375x300")

    global var
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(screen1, text = "Please enter details below").pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Username *").pack()
    username_entry = Entry(screen1, textvariable = username)
    username_entry.pack()
    Label(screen1, text = "Password *").pack()
    password_entry = Entry(screen1, textvariable = password)
    password_entry.pack()
    var = IntVar()
    R1 = Radiobutton(screen1, text="Admin", variable=var, value=1)
    R1.pack(anchor=W)

    R2 = Radiobutton(screen1, text="SpecailUser", variable=var, value=2)
    R2.pack(anchor=W)

    R3 = Radiobutton(screen1, text="User", variable=var, value=3)
    R3.pack(anchor=W)
    var.set(1)

    Label(screen1, text = "").pack()
    Button(screen1, text = "Register", width = 10, height = 1, command = register_user).pack()


def login():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("375x300")
    Label(screen2, text = "Please enter details below").pack()
    Label(screen2, text = "").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1

    Label(screen2, text = "Username *").pack()
    username_entry1 = Entry(screen2, textvariable = username_verify)
    username_entry1.pack()
    Label(screen2, text = "").pack()
    Label(screen2, text = "Password *").pack()
    password_entry1 = Entry(screen2, textvariable = password_verify)
    password_entry1.pack()
    Label(screen2, text="").pack()
    Button(screen2, text = "Login", width = 10, height = 1, command = login_verify).pack()
    Label(screen2,text="").pack()
    Button(screen2,text="Register (Only Admin)", height="2", width="30", command=login_verify_admin).pack()

def main_screen():
    global screen
    screen = Tk()
    screen.geometry("400x300")
    screen.title("Main Page")
    Label(text = "Welcome to Main Page", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Login", height = "2", width = "30", command = login).pack()


    screen.mainloop()

main_screen()
