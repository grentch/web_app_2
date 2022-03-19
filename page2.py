import streamlit as st
import psycopg2


filter1 = st.multiselect(
     'Col A',
     ['option1', 'option2','option3'],
)

st.write('You selected:', filter1)

filter2 = st.multiselect(
     'Col B',
     ['option1', 'option2','option3'],
     )

st.write('You selected:',filter2)




#-----------------------

#table

try: 
     #create connection with database
     conn = psycopg2.connect(database ="streamlit_project", user = "postgres",
                                   password = "1234",port = "5432")
     
     #create cursor of connection
     cur = conn.cursor()

     
     #get values for filter 
     query = """select * from mydata where col_a=ANY(%s) or col_b=ANY(%s);"""
     cur.execute(query,(filter1,filter2,))
     data = cur.fetchall()

     #show data to the screen
     if data:

          st.write("Your filtered data is ")
          all=[]
          for i in data: 
               l=[]
               for j in i:
                    l.append(j)
               all.append(l)

          

          count=True
          for l in all:
               #using list l
               table = "<html>"
               table += "<table>\n"
               while count:
                    # Create the table's column headers
                    header = ["id","title","col_a","col_b","text1","text2","img_location","img_type","audio_location","audio_type","created_at","last_updated"]
                    for r in range(1):
                         table +="<tr>\n"
                         for i in header:
                              table += f"<th>{i}</th>\n"
                         table += "</tr>\n"
                         count=False
               #insert data in rows 
               for r in range(1):
                    table +="<tr>\n"
                    for i in l:
                         table += "<td>{0}</td>\n".format(i)
                    table += "</tr>\n"
               table += "</table>"
               table += "</html>"
               st.write(table, unsafe_allow_html=True )
               
     else:
          st.write("No data found to show ")


except (Exception, psycopg2.DatabaseError) as error:
          st.write(error)
finally:
     if conn is not None:
          conn.close()

