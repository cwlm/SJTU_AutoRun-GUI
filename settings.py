import yaml
import os
import shutil
from utils.streamlit_wrapper import *
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="设置",
    page_icon="⚙️",
)
st.write("# 修改设置 ⚙️")
st.info("用户设置全部在data/下，不想用GUI可以直接改文件", icon="ℹ️")
st.info("修改设置后，为保证稳定建议重启GUI再执行挂机等功能", icon="ℹ️")
st.warning("所有修改实时保存，不能撤回！测试版bug颇多，保险起见建议经常备份data/文件夹！", icon="🚨")
st.warning("如果GUI崩溃，请关闭GUI并手动修改文件来尝试恢复，并反馈bug", icon="🚨")


# 进行初始化，以及读取配置文件
@st.cache_resource
def load_data():
    # 拷贝模板到data目录
    for root, dirs, files in os.walk("data_template"):
        for name in files:
            src_file = os.path.join(root, name)
            dst_file = src_file.replace("data_template", "data")

            # 无覆盖拷贝
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            if not os.path.exists(dst_file):
                shutil.copy(src_file, dst_file)

    # 加载用户当前设置
    with open("data/user_settings.yaml", "r", encoding="utf-8") as f:
        config_ = yaml.load(f, Loader=yaml.FullLoader)

    all_plans_ = {}
    for root, dirs, files in os.walk("data/plans"):
        for name in files:
            with open(os.path.join(root, name), "r", encoding="utf-8") as f:
                key_name = name.split(".")[0]
                all_plans_[key_name] = yaml.load(f, Loader=yaml.FullLoader)

    return config_, all_plans_


# 保存配置文件
def save_data(config_, all_plans_):
    with open("data/user_settings.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config_, f, allow_unicode=True)

    # 不存在的plan删掉（改名或删除）
    for root, dirs, files in os.walk("data/plans"):
        for name in files:
            key_name = name.split(".")[0]
            if key_name not in all_plans_.keys():
                file_path = os.path.join(root, name)
                os.remove(file_path)

    # 存在的plan保存（覆盖或新增）
    for key in all_plans_.keys():
        with open(f"data/plans/{key}.yaml", "w", encoding="utf-8") as f:
            yaml.dump(all_plans_[key], f, allow_unicode=True)


config, all_plans = load_data()

# 修改设置
with st.expander("模拟器设置", False):
    c = config["emulator"]
    text_input("模拟器路径", c, "emulator_dir")
    text_input("模拟器id（多开器请填写，默认为0）", c, "emulator_index")

# with st.expander("自定义舰船名称", False):
#     st.text("暂未实现GUI，请在data/ship_names.yaml中修改")

with st.expander("跑步计划库", False):
    with st.container():
        plan_name = st.selectbox("选择方案",
                                 [key for key in all_plans.keys()])
        plan = all_plans[f"{plan_name}"]
        tabs = st.tabs(["配速", "模式", "距离"])
        with tabs[0]:
            slider("配速(min/km)", plan, "speed", min_value=1.0, max_value=10.0)
        with tabs[1]:
            selectbox("模式", ["single_trip", "back_and_forth", "circular"], plan, "mode")
        with tabs[2]:
            text_input("距离", plan, "distance")

save_data(config, all_plans)
