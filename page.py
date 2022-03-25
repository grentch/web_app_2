import streamlit as st
from PIL import Image
import psycopg2
import os
import glob
import soundfile as sf



menu = st.sidebar.radio(
     'Menu:', ['page1','page2','page3','page4'],index=0)


if menu == "page1":
    try:
        
        conn = None
        result1=None
        result2=None
        atype=""
        alocation=""
        imgloc=""
        imgtype=""
        cola=""
        colb=""
        text1=""
        text2=""
        try: 
            #create connection with database
            conn = psycopg2.connect(database ="streamlit_project", user = "postgres",
                                        password = "1234",port = "5432")
            
            #create cursor of connection
            cur = conn.cursor()

            #check if table already exists
            cur.execute("select exists(select relname from pg_class where relname = 'mydata' and relkind='r');")
            check_exists=cur.fetchone()[0]
            if(check_exists):
                #table already exists
                pass
            else:
                #create table command
                create_table = """CREATE TABLE mydata (
                    ID SERIAL PRIMARY KEY,
                    TITLE VARCHAR(255) default NULL, COL_A VARCHAR(255) NOT NULL , COL_b VARCHAR(255) NOT NULL,
                    TEXT1 VARCHAR(2000) NOT NULL,TEXT2 VARCHAR(2000) NOT NULL,
                    IMG_LOCATION VARCHAR(255) NOT NULL, IMG_TYPE VARCHAR(255) NOT NULL,
                    AUDIO_LOCATION VARCHAR(255) NOT NULL, AUDIO_TYPE VARCHAR(255) NOT NULL
                    ,CREATED_AT TIMESTAMP  DEFAULT current_timestamp
                    , LAST_UPDATED TIMESTAMP  DEFAULT current_timestamp 
                )"""
                #execute command
                cur.execute(create_table)

                #create trigger function to set last_updated time column to last updated time
                f="""CREATE OR REPLACE FUNCTION trigger_set_timestamp()
                RETURNS TRIGGER AS $$
                BEGIN
                NEW.LAST_UPDATED = current_timestamp;
                RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;"""

                cur.execute(f)

                #create a trigger to execute the function
                tf="""CREATE TRIGGER set_timestamp
                BEFORE UPDATE ON public.mydata
                FOR EACH ROW
                EXECUTE PROCEDURE trigger_set_timestamp();"""

                cur.execute(tf)

                # #insert test data into table 
                # insert_query=""" insert into mydata(col_a,col_b,text1,text2,img_location,img_type,audio_location,audio_type) values(%s,%s,%s,%s,%s,%s,%s,%s);"""
                # record_to_insert=('cola','colb','text1','text2','imgloc,imgtype,alocation,atype)
                # #execute query
                # cur.execute(insert_query,record_to_insert)


                #commit the changes
                conn.commit()
                


            #get values for column a 
            query1 = """select col_a from mydata;"""
            cur.execute(query1)
            result1 = cur.fetchall()

            #get values for column b
            query2 = """select col_b from mydata;"""
            cur.execute(query2)
            result2 = cur.fetchall()
            


        except (Exception, psycopg2.DatabaseError) as error:
                st.write(error)
        finally:
            if conn is not None:
                conn.close()


        #--------------------------------



        cola = st.selectbox(
            'Col A',
            ('option1', 'option2','option3',))

        st.write('You selected:', cola)

        colb = st.selectbox(
            'Col B',
            ('option1', 'option2','option3',))

        st.write('You selected:', colb)

        #----------------------------------------------------

        text1 = st.text_area('Text 1', '''''')
        

        text2 = st.text_area('Text 2', '''''')
       

        #-----------------------------------------


       




        def img_file_selector(folder_path='.', target="Image"):
            filenames = [f for f in os.listdir(folder_path) if
                        not f[0] == "."]  # get file names from dir excluding hidden files
            selected_filename = st.selectbox(f'Select a {target}', filenames)
            abs_path = os.path.join(folder_path, selected_filename)
            if os.path.isdir(abs_path):
                return img_file_selector(abs_path, target)
            return os.path.join(folder_path, selected_filename)
        imglocation = img_file_selector(folder_path="C:\\Users")
        st.write('You selected path is  `%s`' % imglocation)

        
                
        if imglocation is not None:
            try:
                #show image
                imgloca = Image.open(imglocation)
                st.image(imgloca, caption='Your Uploaded Image')

              
            except Exception: 
                pass
            
            
        else:
            path_in = None

        #--------------------------------------


        # audio_path = st.file_uploader("Upload a file", type=(["audio","ogg","M4A","FLAC","MP3","MP4","WAV","WMA","AAC"]))
        # if audio_path is not None:
        #     #show to the screen
        #     audio_file = open(audio_path.name, 'rb')
        #     audio_bytes = audio_file.read()
        #     st.audio(audio_bytes, format='audio/ogg/M4A/FLAC/MP3/MP4/WAV/WMA/AAC')

        #     #save to databse
        #     alocation=str(audio_path.name)
        #     atype=audio_path.type
            
        # else:
        #     path_in = None


        def audio_file_selector(folder_path='.', target="Audio"):
            filenames = [f for f in os.listdir(folder_path) if
                        not f[0] == "."]  # get file names from dir excluding hidden files
            selected_filename = st.selectbox(f'Select a {target}', filenames)
            abs_path = os.path.join(folder_path, selected_filename)
            if os.path.isdir(abs_path):
                return audio_file_selector(abs_path, target)
            return os.path.join(folder_path, selected_filename)
        alocation = audio_file_selector(folder_path="C:\\Users")
        st.write('You selected path is  `%s`' % alocation)

        if alocation is not None:
            try:
                #show to the screen
                audio_file = open(alocation, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/ogg/M4A/FLAC/MP3/MP4/WAV/WMA/AAC')

              
            except Exception: 
                pass
            
            
        else:
            path_in = None

        #----------------------

        if st.button('Add'):
            try:
                
            
                
                def save_uploaded_image(uploadedfile):
                    uploadedfileopen=str(uploadedfile).rsplit('\\',1)[-1]
                    with open(os.path.join("img",uploadedfileopen),"wb") as f:
                            cl_img=Image.open(uploadedfile)
                            cl_img.save(f)
                          
                    return st.success("Saved file :{} in img folder".format(uploadedfile))


                def save_uploaded_audio(uploadedfile):
                    
                    try:
                        t=re.escape(uploadedfile)
                        st.write(t)
                        data, fs = sf.read(t) 
                        sf.write("audio", data, fs)  
                    except Exception:
                        pass
                            
                    return st.success("Saved file :{} in audio folder".format(uploadedfile))


                


                
                #store image in local drice
                if str(imglocation).rsplit('.',1)[-1] in ["apng","avif","gif","jpg","jpeg","jfif","pjpeg","pjp","png","svg","webp"]:
                    if str(alocation).rsplit('.',1)[-1] in ["audio","ogg","M4A","FLAC","MP3","MP4","WAV","WMA","AAC"]:
                        


                        #store in database
                        imgloc=str(imglocation)
                        imgtype=imgloc.rsplit('.',1)[-1]
                        aloc=str(alocation)
                        atype=aloc.rsplit('.',1)[-1]

                        #create connection with database
                        conn = psycopg2.connect(database ="streamlit_project", user = "postgres",
                                                        password = "1234",port = "5432")
                        

                        #create cursor of connection
                        cur = conn.cursor()     
                        #insert above data into table 
                        insert_query=""" insert into mydata(col_a,col_b,text1,text2,img_location,img_type,audio_location,audio_type) values(%s,%s,%s,%s,%s,%s,%s,%s);"""
                        record_to_insert=(cola,colb,text1,text2,imgloc,imgtype,alocation,atype)
                        #execute query
                        cur.execute(insert_query,record_to_insert)
                        #commit the changes
                        conn.commit()
                        #message of insert successsfully
                        st.write("Successfully inserted to database")
                        #close cursor
                        cur.close()
                        conn.close()





                        #store in local drive
                        save_uploaded_image(imglocation)
                        #save to local drive
                        save_uploaded_audio(alocation)




                    else:
                        st.write("audio must be of following type:\n")
                        st.write("--->audio,ogg,M4A,FLAC,MP3,MP4,WAV,WMA,AAC")

                else:
                    st.write("image must be of following type:\n")
                    st.write("--->apng,avif,gif,jpg,jpeg,jfif,pjpeg,pjp,png,svg,webp")

                




            
            except (Exception, psycopg2.DatabaseError) as error:
                    st.write(error)
            finally:
                if conn is not None:
                    conn.close()



        else:
            st.write('Click to Add')


    except Exception:
        st.write("error in page1")


if menu == "page2":
    try:
        
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

        
    except Exception:
        st.write("error in page2")
    

if menu == "page3":
    try:
        

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
                        st.write(" updated --->"+str(itrt+1))
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




    except Exception:
        st.write("error in page3")
    

if menu == "page4":
    try:
        
        

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
            qf3 = """select audio_type from mydata ;"""
            cur.execute(qf3,(filter1,filter2,))
            f_3 = cur.fetchall()
            f3=list(set(f_3))

            
            filter3 = st.multiselect(
                'Audio Type',
                f3,
                )


            #get values for filter 
            query = """select * from mydata where (col_a=ANY(%s) or col_b=ANY(%s)) and audio_type= ANY(%s) order by last_updated desc;"""
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



    except Exception:
        st.write("error in page4")
    