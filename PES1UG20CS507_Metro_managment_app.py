import streamlit as st
import mysql.connector
# from admin import *
# from user import *
from func import *
from pro import *
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='metro_managment'
)
c = mydb.cursor()
admin='admin123'
pas='pass'
username=''
pas=''
def app():
    st.title('Metro Managment')
    menu=['Add Card','Remove Card','New User','Card or User History','Topup','Travel','Card Balance','New Station','Update Station','Add Fare','Update Fare','New Card','View Cards','View Stations','View Fare','Query','Check cards','Function','Procedure']
    choice=st.sidebar.selectbox('Menu',menu)
    if choice=='New Station':
        st.subheader('Add Station details')
        newstation()
    elif choice=='Update Station':
        st.subheader('Update Station')
        updatestation()
    elif choice=='Add Fare':
        st.subheader('Add Fare')
        addfare()
    elif choice=='Update Fare':
        st.subheader('Update Fare')
        updatefare()
    elif choice=='New Card':
        st.subheader('Issue card')
        newcard()
    elif choice=='View Cards':
        st.subheader('Card')
        viewcard()
    elif choice=='View Stations':
        st.subheader('Stations')
        viewstation()
    elif choice=='Add Card':
        st.subheader('Attaching Card to User')
        addcard()
    elif choice=='Remove Card':
        st.subheader('Removing Card to User')
        removecard()
    elif choice=='New User':
        st.subheader('New User')
        newcard()
    elif choice=='Card or User History':
        st.subheader('History')
        history()
    elif choice=='Topup':
        st.subheader('Top Up')
        topup()
    elif choice=='Travel':
        st.subheader("relocate")
        travel()
    elif choice=='Card Balance':
        st.subheader('Balance')
        funds()
    elif choice=='View Fare':
        st.subheader('Fare')
        viewfare()
    elif choice=='Check cards':
        st.subheader('Cards')
        card()
    elif choice=='Function':
        st.subheader('No of travellers on a particular day')
        users_on_a_day()
    elif choice=='Procedure':
        st.subheader('No of users on a particular card')
        users_on_card()
    else:
        st.subheader('Enter Query')
        query()
        
if __name__=='__main__':
    app()
