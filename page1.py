import streamlit as st
from PIL import Image
import psycopg2
import os

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
st.write('You entered:', text1)

text2 = st.text_area('Text 2', '''''')
st.write('You entered:', text2)


#-----------------------------------------


imglocation = st.file_uploader("Upload a file", type=(["apng","avif","gif","jpg","jpeg","jfif","pjpeg","pjp","png","svg","webp"]))
if imglocation is not None:
     #show image
     imgloca = Image.open(imglocation.name)
     st.image(imgloca, caption='Your Uploaded Image')

     #store in database
     imgloc=str(imglocation.name)
     imgtype=imglocation.type
    
    
else:
     path_in = None


#--------------------------------------


audio_path = st.file_uploader("Upload a file", type=(["audio","ogg","M4A","FLAC","MP3","MP4","WAV","WMA","AAC"]))
if audio_path is not None:
     #show to the screen
     audio_file = open(audio_path.name, 'rb')
     audio_bytes = audio_file.read()
     st.audio(audio_bytes, format='audio/ogg/M4A/FLAC/MP3/MP4/WAV/WMA/AAC')

     #save to databse
     alocation=str(audio_path.name)
     atype=audio_path.type
     
else:
     path_in = None




#----------------------

if st.button('Add'):
     try:

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


          
          def save_uploaded_image(uploadedfile):
               with open(os.path.join("img",uploadedfile.name),"wb") as f:
                    f.write(uploadedfile.getbuffer())
               return st.success("Saved file :{} in img folder".format(uploadedfile.name))

          def save_uploaded_audio(uploadedfile):
               with open(os.path.join("audio",uploadedfile.name),"wb") as f:
                    f.write(uploadedfile.getbuffer())
               return st.success("Saved file :{} in audio folder".format(uploadedfile.name))

          #store image in local drice
          if imglocation is not None:
               #store in local drive
               save_uploaded_image(imglocation)
          else:
               path_in = None

          #store audio in local drice
          if audio_path is not None:
               #save to local drive
               save_uploaded_audio(audio_path)
          else:
               path_in = None




     
     except (Exception, psycopg2.DatabaseError) as error:
               st.write(error)
     finally:
          if conn is not None:
               conn.close()



else:
    st.write('Click to Add')

