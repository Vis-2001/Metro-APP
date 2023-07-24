import mysql.connector
import streamlit as st
def users_on_card():
    mydb=mysql.connector.connect(
    host='localhost',
    username='root',
    password=''
    )
    cursor=mydb.cursor()
    cursor.execute('use metro_managment')
    card=st.text_input('Enter Card Number:')
    if st.button('Find Total users on card'):
        q1='call card_users(\''+card+'\')'
        cursor.execute(q1)
        data=cursor.fetchall()
        for i in data:
            st.text(i)
        cursor.close()