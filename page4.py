import streamlit as st


option1 = st.multiselect(
     'Col A',
     ['Green', 'Yellow', 'Red', 'Blue'],
     )

st.write('You selected:', option1)

option2 = st.multiselect(
     'Col B',
     ['Green', 'Yellow', 'Red', 'Blue'],
     )

st.write('You selected:', option2)


#type of file
option3 = st.multiselect(
     'File',
     ['type1', 'type2', 'type3'],
     )

st.write('You selected:', option3)


#-----------------------------

if st.button('Update'):
    st.write(' updated ')
else:
    st.write('Click to Update')

#---------------------------

if st.button('Next'):
    st.write('  Next page ')
else:
    st.write('Click to next')

