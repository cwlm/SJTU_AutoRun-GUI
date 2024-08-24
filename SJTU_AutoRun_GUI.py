import streamlit as st

pg = st.navigation([st.Page("mygo.py", title="Its MyGO!!!!!"),
                    st.Page("settings.py")])
pg.run()
