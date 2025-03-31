import streamlit as st
import pandas as pd
import numpy as np
import pymysql
import mysql.connector

#SQL Connection
mydb = mysql.connector.connect(
         host="127.0.0.1",
        port=3306,
        user='root',
        password="root",
       database="red_bus",
        autocommit = True)

mycursor = mydb.cursor()

st.title("RED BUS")
# Create the form
form = st.form(key='BUS_DATA')

# Set of fare range
tiket_rate = form.selectbox("Select Fare Range", [500, 600,800,900,1017,350,255,450,])

if tiket_rate == 500 - 600:
      tiket_min, tiket_max = 500,600
elif tiket_rate == 800 - 900:
        tiket_min, tiket_max = 900, 900
else:
    tiket_min, tiket_max = 900, 1000

# Seat type
seats_type = form.selectbox("Select Seat Type", ["seater", "semi sleeper", "sleeper"])

if seats_type == "seater":
    seats_type_condition = "bustype 'seater'"
elif seats_type == "semi sleeper":
    seats_type_condition = "bustype  'semisleeper'"
else:
    seats_type_condition = "bustype 'sleeper'"

# Star rating
star_rating = form.selectbox("Select Star Rating", ["3.4","4.4", "3.4 "," 4.1", "4.3"," 4.5"])

if star_rating == "4.5 to 4.4":
    rating_min, rating_max = 4.5, 4.4
elif star_rating == "3.4 to 4.1":
    rating_min, rating_max = 4.3, 4.3
else:
    rating_min, rating_max = 4.3,4.5

#Route time
route_times = form.selectbox("Select Route Time", ["10.15", "12.30", "3.30", "10.30"])
if route_times == "Morning":
    route_time_condition = "route_times BETWEEN '06:00' AND '12:00'"
elif route_times == "Afternoon":
    route_times_condition = "route_times BETWEEN '12:00' AND '18:00'"


# Duration
duration = form.selectbox("Select Duration", ["5.30","6.30","7.45","12.10" ])
duration_condition = "duration BETWEEN 0 AND 24"

#reaching
reching=form.selectbox("select reching",["7.30","22.10","6.00","4.30","5.30","19.30",])
reching_time_contion="reching_time between 0 and  24" 

mycursor.execute("SELECT DISTINCT route_name FROM bus_data")
result=mycursor.fetchall()
route_select=[i[0]for i in result]
select_route=form.selectbox("route",route_select)
#st.write(result)
if  "STATE and Routes":

 with st.form(key="bus_form"):
  
  selectstate=form.selectbox("STATE",
                                            ["KERALA",
                                            "ANTHARA" ,
                                            "TELUNGANA",
                                            "KADAMBA",
                                            "south bengal",
                                            "Himachal pradesh",
                                            "Assam",
                                            "Uttaraprathesh",
                                            "Bhigar",
                                            "Chandigrap"
                                                    ])

submit_button = form.form_submit_button(label="Submit")
if submit_button:   

    qurey=f"""select * from bus_data where state='{selectstate}'                  
            AND '{select_route}'
            AND '{seats_type_condition}'
            AND star_rating BETWEEN '{rating_min} 'AND '{rating_max}'
            AND '{route_times}'
            AND '{duration_condition}'
            AND'{star_rating} '
            AND'{reching_time_contion} '
            AND'{duration}' """

    query = "SELECT * FROM bus_data WHERE state = %s AND route_name = %s"
    params = (selectstate, select_route)
    mycursor.execute(query, params)     
   
    #mycursor.execute(qurey)
    result=mycursor.fetchall()
    mycursor.execute("describe bus_data")
    cloumns=mycursor.fetchall()
    finallcolumns=[i[0]for i in cloumns]
    df=pd.DataFrame(result,columns=finallcolumns)
    st.write(df)

#st.error('Error message')
#st.balloons() 


