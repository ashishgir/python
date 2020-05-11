import pyodbc
import pandas as pd

def ViewAllUsers():
    con=pyodbc.connect("DRIVER={SQL Server};server=DESKTOP-SDDF15J;database=Covid;Trusted_Connection=yes;")
    cur=con.cursor()
    cur.execute("Select * from Login")
    rows = cur.fetchall()
    return rows

def VerifyUser(username , password):
    con = pyodbc.connect("DRIVER={SQL Server};server=DESKTOP-SDDF15J;database=Covid;Trusted_Connection=yes;")
    cur = con.cursor()
    cur.execute("Select * from Login where Username = '"+username+"' and Password = '"+password+"'")
    rows = cur.fetchall()
    return rows

def GetCountry():
    con = pyodbc.connect("DRIVER={SQL Server};server=DESKTOP-SDDF15J;database=Covid;Trusted_Connection=yes;")
    cur = con.cursor()
    cur.execute("Select DISTINCT(Country) from [Covid].[dbo].[covid_19_data]")
    rows = cur.fetchall()
    return rows

def GetStates(SelectedCountry):
    con = pyodbc.connect("DRIVER={SQL Server};server=DESKTOP-SDDF15J;database=Covid;Trusted_Connection=yes;")
    cur = con.cursor()
    cur.execute("Select DISTINCT(State) from [Covid].[dbo].[covid_19_data] WHERE Country like '"+SelectedCountry+"'")
    rows = cur.fetchall()
    return rows

def GetStates():
    con = pyodbc.connect("DRIVER={SQL Server};server=DESKTOP-SDDF15J;database=Covid;Trusted_Connection=yes;")
    cur = con.cursor()
    cur.execute("Select DISTINCT(State) from [Covid].[dbo].[covid_19_data]")
    rows = cur.fetchall()
    return rows

def GetListByCountryandState(SelectedCountry,SelectedState):
    con = pyodbc.connect("DRIVER={SQL Server};server=DESKTOP-SDDF15J;database=Covid;Trusted_Connection=yes;")
    cur = con.cursor()
    cur.execute("Select * from [Covid].[dbo].[covid_19_data] WHERE Country like '"+SelectedCountry+"' and State like '"+SelectedState+"'")
    rows = cur.fetchall()
    return rows

def InsertUser(username_info,password_info,SelectedRadio):
    con = pyodbc.connect("DRIVER={SQL Server};server=DESKTOP-SDDF15J;database=Covid;Trusted_Connection=yes;")
    cur = con.cursor()
    if SelectedRadio==1:
        cur.execute("Insert into Login values ('"+username_info+"','"+password_info+"','true','true')")
    if SelectedRadio==2:
        cur.execute("Insert into Login values ('"+username_info+"','"+password_info+"','false','true')")
    if SelectedRadio==3:
        cur.execute("Insert into Login values ('"+username_info+"','"+password_info+"','false','false')")
    con.commit()