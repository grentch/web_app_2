import streamlit as st
import psycopg2


filter1 = st.multiselect(
     'Col A',
     ['option1', 'option2','option3'],
)

filter2 = st.multiselect(
     'Col B',
     ['option1', 'option2','option3'],
     )


#-----------------------

#table
itrt=0
try: 
    #create connection with database
    conn = psycopg2.connect(database ="streamlit_project", user = "postgres",
                                password = "1234",port = "5432")

    #create cursor of connection
    cur = conn.cursor()

    #get values for filter 
    qf3 = """select img_type from mydata ;"""
    cur.execute(qf3,(filter1,filter2,))
    f_3 = cur.fetchall()
    f3=list(set(f_3))

    
    filter3 = st.multiselect(
        'Image Type',
        f3,
        )


    #get values for filter 
    query = """select * from mydata where (col_a=ANY(%s) or col_b=ANY(%s)) and img_type= ANY(%s) order by last_updated desc;"""
    cur.execute(query,(filter1,filter2,filter3))
    data = cur.fetchall()
    
    

    #show data to the screen
    if data:
        all=[]
        for i in data: 
            l=[]
            for j in i:
                l.append(j)
            all.append(l)

        

       
            
        
        while(itrt < len(data)):
            
            st.write("----------------------------------------------------------------------------------")
            #st.write(all[itrt])
            for r in range(1):
                    table = "<html>"
                    table += "<table>\n"
                    table +="<tr>\n"
                    for i in all[itrt]:
                        table += "<td>{0}</td>\n".format(i)
                    table += "</tr>\n"
            table += "</table>"
            table += "</html>"
            st.write(table, unsafe_allow_html=True )



            #update last updated time in record   
            btn="Update"+"-->"+str(itrt+1)
            if st.button(btn):
                #update last_modified
                query2 = """update mydata set col_a=%s where id=%s;"""
                p,q=str(all[itrt][2]),str(all[itrt][0])

                cur.execute(query2,(p,q))
                #commit the changes
                conn.commit()
                st.write(" updated "+str(itrt+1))
            else:
                st.write('Click to Update')
            itrt=itrt+1
        
    else:
        st.write("No data found to show ")


except(Exception, psycopg2.DatabaseError) as error:
    st.write(error)
finally:
    if conn is not None:
        conn.close()



