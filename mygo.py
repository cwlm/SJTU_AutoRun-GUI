import streamlit as st
from sjtuautorun.mygo import RunPlan
from sjtuautorun.scripts.main import start_script

# ==================== 页面信息 ====================
st.set_page_config(
    page_title="SJTU_AutoRun",
    page_icon="🏃",
)


# ==================== 正文 ====================
st.write("# 欢迎来到交我润控制台!")
with open("Hello.md", "r", encoding="utf-8") as f:
    readme = f.read()
st.markdown(readme)


if st.button("开始运行"):
    st.balloons()
    # 指定采用本地设置

    timer = start_script("data/user_settings.yaml")
    run_plan = RunPlan(timer)
    run_plan.start_run()
