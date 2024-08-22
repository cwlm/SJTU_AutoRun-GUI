import streamlit as st
import os

from sjtuautorun.mygo import RunPlan
from sjtuautorun.scripts.main import start_script

st.set_page_config(
    page_title="日常挂机",
    page_icon="🎣",
)
# st.sidebar.success("选择一项功能")

if st.button("开始运行"):
    st.balloons()
    # 指定采用本地设置

    timer = start_script("data/user_settings.yaml")
    run_plan = RunPlan(timer)
    run_plan.start_run()
