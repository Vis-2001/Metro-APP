# %%
import mysql.connector
import streamlit as st
import pandas as pd
# %%
mydb=mysql.connector.connect(
    host='localhost',
    username='root',
    password=''
)

# %%
cursor=mydb.cursor()

# %%
cursor.execute('use metro_managment')

# %%
def newstation():
    name=st.text_input('Name:')
    id=st.text_input('Id:')
    if st.button('Add New Station'):
        query='insert into stations values(\''+name+'\','+str(id)+');'
        cursor.execute(query)
        mydb.commit()
        st.success('Successfully added staion {} with id {}'.format(name,id))

# %%
def updatestation():
    id1=st.number_input('Station Id io be Updated:')
    name2=st.text_input('Chnaged Station Name:')
    id2=st.number_input('Updated station Id:')
    if st.button('Update Staion'):
        query='update stations set station_name=\''+name2+'\',sid='+str(id1)+' where sid='+str(id2)
        cursor.execute(query)
        mydb.commit()
        st.success('Successfully updated station {} with id {}'.format(name2,id2))

# %%
def addfare():
    id1=st.number_input('Destination Station:')
    id2=st.number_input('Source Station:')
    cost=st.number_input('Fare:')
    if st.button('Update Staion'):
        query='insert into fare values('+str(id1)+','+str(id2)+','+str(cost)+');'
        cursor.execute(query)
        mydb.commit()
        st.success('Successfully added fare {} from station {} to station {}'.format(cost,id2,id1))

# %%
def updatefare():
    id1=st.number_input('Destination Station:')
    id2=st.number_input('Source Station:')
    cost=st.number_input('Updated Fare:')
    if st.button('Update Staion'):
        query='update fare set cost='+str(cost)+' where to_station_id='+str(id1)+' and from_station_id='+str(id2)
        cursor.execute(query)
        mydb.commit()
        st.success('Successfully Updated fare {} from station {} to station {}'.format(cost,id2,id1))

# %%
def newcard():
    cid=st.number_input('Issue Card Number:')
    balance=st.number_input('Initial Balance:')
    if st.button('Add Card'):
        query='insert into card(cid,balance) values('+str(cid)+','+str(balance)+')'
        cursor.execute(query)
        mydb.commit()
        st.success('New Card Added')

# %%
def viewcard():
    cursor.execute('select cid,balance,start_date from card')
    data=cursor.fetchall()
    st.text('[Card Id,Balance,Start_Date]')
    for i in data:
        st.text(i)
    # df=pd.DataFrame(data,columns=['Card Id','Balance','Start_Date'])
    # # df['Balance']=df['Balance']/100000
    # with st.expander("Card Info"):
    #     st.dataframe(df)


# %%
def viewstation():
    cursor.execute('select * from stations')
    data=cursor.fetchall()
    st.text('[Station Nmae,Station Id]')
    for i in data:
        st.text(i)
    # df=pd.DataFrame(data,columns=['Station Nmae','Station Id'])
    # with st.expander("Station Info"):
    #     st.dataframe(df)
    

# %%
def viewfare():
    cursor.execute('select to_station_id,s.station_name,from_station_id,si.station_name,cost from stations s join fare f on f.to_station_id=s.sid join stations si on f.from_station_id=si.sid;')
    data=cursor.fetchall()
    st.text('[DestinationID,Destination,SourceId,Source,Fare]')
    for i in data:
        st.text(i)
    # df=pd.DataFrame(data,columns=['DestinationID','Destination','SourceId','Source','Fare'])
    # # df['Fare']=df['Fare']/1000
    # with st.expander("Fare Info"):
    #     st.dataframe(df)

# %%
def addcard():
    name=st.text_input('Name:')
    card=st.number_input('Card Id:')
    if st.button('Add Card to user'):
        query='select count(*) from card where cid='+str(card)
        cursor.execute(query)
        trig=0
        for x in cursor:
            if(x[0]==0):
                trig=1
                break
        if(trig):
            st.text('Incorrect Card details')
        else:
            query='insert into user_card values(\''+name+'\','+str(card)+')'
            cursor.execute(query)
            mydb.commit()
            st.success('Card successfully attached to the user')

# %%
def removecard():
    name=st.text_input('Name:')
    card=st.number_input('Card Id:')
    if st.button('Remove Card from user'):
        query='delete from user_card where Uname=\''+name+'\' and cid='+str(card)
        cursor.execute(query)
        mydb.commit()
        st.success('Card removed')

# %%
def newuser():
    name=st.text_input('Name:')
    biometric=st.text_input('Biometric Identification')
    if st.button('Add User'):
        query='insert into user values(\''+name+'\',\''+biometric+'\')'
        cursor.execute(query)
        mydb.commit()
        st.success('Welcome to metro. Hope u have a great experience')

# %%
def historyname(name):
    query='select cid,payment_type,amount,s.station_name,si.station_name from transaction join stations s on entry_id=s.sid join stations si on exit_id=si.sid where cid in(select cid from user_card where Uname=\''+str(name)+'\')'
    cursor.execute(query)
    data=cursor.fetchall()
    st.text('[Card Id,Payment,Amount,Source,Destination]')
    for i in data:
        st.text(i)
    # df=pd.DataFrame(data,columns=['Card Id','Payment','Amount','Source','Destination'])
    # # df['Amount']=df['Amount']/1000
    # with st.expander("User History"):
    #     st.dataframe(df)

# %%
def historycard(card):
    query='select Uname,payment_type,amount,s.station_name,si.station_name from transaction join stations s on entry_id=s.sid join stations si on exit_id=si.sid where cid in(select cid from user_card where cid='+str(int(card))+')'
    cursor.execute(query)
    data=cursor.fetchall()
    st.text('[User Name,Payment,Amount,Source,Destination]')
    for i in data:
        st.text(i)
    # df=pd.DataFrame(data,columns=['User Name','Payment','Amount','Source','Destination'])
    # # df['Amount']=df['Amount']/1000
    # with st.expander("Card History"):
    #     st.dataframe(df)

# %%
def history():
    name=st.text_input('Name:')
    card=st.number_input('Card Id:')
    if st.button('Show History'):
    # if(card==''):
        historyname(name)
    # elif(name==0.0):
        historycard(card)
    # else:
        q1='select payment_type,amount,s.station_name,si.station_name from transaction join stations s on entry_id=s.sid join stations si on exit_id=si.sid where cid in(select cid from user_card where cid='+str(card)+' and Uname=\''+str(name)+'\')'
        query='select payment_type,amount,entry_id,exit_id from transaction where cid in(select cid from user_card where cid='+str(card)+' and Uname=\''+str(name)+'\')'
        cursor.execute(q1)
        data=cursor.fetchall()
        st.text('[Payment,Amount,Source,Destination]')
        for i in data:
            st.text(i)
        # df=pd.DataFrame(data,columns=['Payment','Amount','Source','Destination'])
        # # df['Amount']=df['Amount']/1000
        # with st.expander("Combined History"):
        #     st.dataframe(df)
        

# %%
def checkbio(name,bio):
    query='select count(*) from user where Uname=\''+name+'\' and biometric=\''+bio+'\''
    cursor.execute(query)
    for x in cursor:
        if(x[0]==0):
            return False
        else:
            return True
        

# %%
def checkcard(name,card):
    query='select count(*) from user_card where Uname=\''+name+'\' and cid='+str(card)
    cursor.execute(query)
    for x in cursor:
        if(x[0]==0):
            return False
        else:
            return True

# %%
def topup():
    card=int(st.number_input('Card Id:'))
    name=st.text_input('Name:')
    amount=st.number_input('Top Up Amount:')
    station=int(st.number_input('Station Id:'))
    biometric=st.text_input('Enter Identification:')
    ptype=st.text_input('Enter Payment Mode(Cash/Onlone')
    if st.button('TopUP'):
        if(checkbio(name,biometric)):
            if(checkcard(name,card)):
                q1='select tid from transaction order by tid desc limit 1'
                cursor.execute(q1)
                tid=0
                for x in cursor:
                    tid=x[0]+1
                q1='insert into transaction(tid,cid,Uname,payment_type,amount,entry_id) values('+str(tid)+','+str(card)+',\''+name+'\',\''+ptype+'\','+str(amount)+','+str(station)+')'
                cursor.execute(q1)
                q1='update card set balance=balance+'+str(amount)+' where cid='+str(card)
                cursor.execute(q1)
                mydb.commit()
                st.success('Ur card has been recharged')
            else:
                st.text('Check Card Details')
        else:
            st.text('Check Identification')

# %%
def amt(sid1,sid2):
    q1='select cost from fare where to_station_id='+str(sid1)+' and from_station_id='+str(sid2)
    cursor.execute(q1)
    amt=1000
    for x in cursor:
        amt=-1*x[0]
    return amt

# %%
def checkfunds(card,amt):
    q1='select balance from card where cid='+str(card)
    cursor.execute(q1)
    bal=0
    for x in cursor:
        bal=x[0]
    if(bal>=50 and bal-amt>=0):
        return True
    return False

# %%
def travel():
    card=int(st.number_input('Card Id:'))
    name=st.text_input('Name:')
    biometric=st.text_input('Enter Identification:')
    sid1=st.number_input('Destination:')
    sid2=st.number_input('Source')
    if st.button('Travel'):
        if(checkbio(name,biometric)):
            if(checkcard(name,card)):
                cs=amt(sid1,sid2)
                if(checkfunds(card,cs)):
                    q1='select tid from transaction order by tid desc limit 1'
                    cursor.execute(q1)
                    tid=0
                    for x in cursor:
                        tid=x[0]+1
                    q1='insert into transaction(tid,cid,Uname,payment_type,amount,entry_id,exit_id) values('+str(tid)+','+str(card)+',\''+name+'\',\'card\','+str(cs)+','+str(sid1)+','+str(sid2)+')'
                    cursor.execute(q1)
                    q1='update card set balance=balance-'+str(-1*cs)+' where cid='+str(card)
                    cursor.execute(q1)
                    mydb.commit()
                    st.success('Happy Journey')
                else:
                    st.text('Insufficienct balance kindly recharge')
            else:
                st.text('Check card number\n')
        else:
            st.text('Check biometric\n')

# %%
def funds():
    card=st.number_input('Card Id:')
    if st.button('Check Balance'):
        q1='select balance from card where cid='+str(int(card))
        cursor.execute(q1)
        bal=0
        for x in cursor:
            bal=x[0]
            break
        st.text(str(bal))

def card():
    bio=st.text_input("Enter Biometric:")
    if st.button('Find Cards'):
        q1='select Uname,count(*) from user natural join user_card where biometric=\''+bio+'\''
        cursor.execute(q1)
        st.text('[User Name, Total Cards]')
        for x in cursor:
            st.text(x)
        q1='select CID from user natural join user_card where biometric=\''+bio+'\''
        cursor.execute(q1)
        data=cursor.fetchall()
        st.text('[User Name,Card ID]')
        for i in data:
            st.text(i)
        # df=pd.DataFrame(data,columns=['User Name','Card ID'])
        # with st.expander("Fare Info"):
        #     st.dataframe(df)
def query():
    menu=['card','fare','stations','transacation','user','user_card']
    choice=st.selectbox('Tables',menu)
    if choice=='card':
        txt='Columns \n cid, balance, start_date, end_date'
        st.text(txt)
    elif choice=='fare':
        txt='Columns \n to_station_id, from_station_id, cost'
        st.text(txt)
    elif choice=='stations':
        txt='Columns \n sid, station_name'
        st.text(txt)
    elif choice=='transacation':
        txt='Columns \n tid, cid, Uname, payment_type, amount, entry_id, entry_time, exit_id, exit_time'
        st.text(txt)
    elif choice=='user':
        txt='Columns \n Uname, biometric'
        st.text(txt)
    else:
        txt='Columns \n Uname, CID'
        st.text(txt)
    q=st.text_input('Enter Sql Query:')
    if st.button('Run Query'):
        cursor.execute(q)
        try:
            data=cursor.fetchall()
            for i in data:
                st.text(i)
            # df=pd.DataFrame(data)
            # with st.expander("Query Result"):
            #     st.dataframe(df)
        except:
            st.text('Wrong Query')
        mydb.commit()

def users_on_a_day():
    dat=st.date_input('Enter Date:')
    if st.button("Find Passengers"):
        q='select distinct date(entry_time),passen(\''+str(dat)+'\') from transaction where date(entry_time)=\''+str(dat)+'\''
        cursor.execute(q)
        data=cursor.fetchall()
        for i in data:
            st.text(i)
# def users_on_card():
#     cur=mydb.connect()
    # card=st.text_input('Enter Card Number:')
#     cur.execute('select * from card')
#     # if st.button('Users'):
#         # q1='call card_users(\''+card+'\')'
#         # cur.execute(q1)
#         # data=cur.fetchall()
#         # for i in data:
#         #     st.text(i)
#         # cur.close()
