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


#-----------------------

#table