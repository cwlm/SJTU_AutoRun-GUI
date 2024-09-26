import streamlit as st

pg = st.navigation([st.Page("mygo.py", title="Its MyGO!!!!!"),
                    st.Page("settings.py", title="设置⚙️")])
pg.run()
