import streamlit as st
import pandas as pd


# 统一 字典、列表 的修改方式
def value_assign(dic_or_list, key_or_index, st_key):
    def assign():
        dic_or_list[key_or_index] = st.session_state[st_key]

    return assign


def value_assign_df(dic_or_list, key_or_index, st_key):
    def assign():
        try:
            dic_or_list[key_or_index] = st.session_state[st_key].to_array()
        except ValueError:
            pass

    return assign


# ==================== 以下为封装的 streamlit 组件 ====================
def selectbox(label, options, dic, key, tag='', **kwargs):
    st_key = label + str(tag)
    default_value = dic[key]
    callback_fn = value_assign(dic, key, st_key)
    return st.selectbox(label, options, options.index(default_value), key=st_key, on_change=callback_fn, **kwargs)


def multiselect(label, options, dic_or_list, key_or_index, tag='', **kwargs):
    st_key = label + str(tag)
    try:
        default_value = dic_or_list[key_or_index]
    except KeyError:
        default_value = None
    callback_fn = value_assign(dic_or_list, key_or_index, st_key)
    return st.multiselect(label, options, default_value, key=st_key, on_change=callback_fn, **kwargs)


def slider(label, dic_or_list, key_or_index, tag='', min_value=0.0, max_value=100.0, step=0.1, **kwargs):
    st_key = label + str(tag)
    try:
        default_value = dic_or_list[key_or_index]
    except KeyError:
        default_value = (0, 100)
    callback_fn = value_assign(dic_or_list, key_or_index, st_key)
    return st.slider(label, min_value, max_value, default_value, step, key=st_key, on_change=callback_fn, **kwargs)


def checkbox(label, dic_or_list, key_or_index, tag='', **kwargs):
    st_key = label + str(tag)
    try:
        default_value = dic_or_list[key_or_index]
    except KeyError:
        default_value = False
    callback_fn = value_assign(dic_or_list, key_or_index, st_key)
    return st.checkbox(label, default_value, key=st_key, on_change=callback_fn, **kwargs)


def text_input(label, dic_or_list, key_or_index, tag='', **kwargs):
    st_key = label + str(tag)
    try:
        default_value = dic_or_list[key_or_index]
    except KeyError:
        default_value = ""
    callback_fn = value_assign(dic_or_list, key_or_index, st_key)
    return st.text_input(label, default_value, key=st_key, on_change=callback_fn, **kwargs)


def rename_text_input(label, father_dict, father_key, prefix='', tag='', **kwargs):
    def item_rename(father_dict_, father_key_, prefix_, st_key_):
        def rename():
            new_key = prefix_ + st.session_state[st_key_]
            father_dict_[new_key] = father_dict_.pop(prefix_ + father_key_)
            st.session_state[st_key_] = ''

        return rename

    st_key = label + str(tag)
    callback_fn = item_rename(father_dict, father_key, prefix, st_key)
    return st.text_input(label, key=st_key, on_change=callback_fn, **kwargs)


def number_input(label, dic_or_list, key_or_index, tag='', **kwargs):
    st_key = label + str(tag)
    try:
        default_value = dic_or_list[key_or_index]
    except KeyError:
        default_value = None
    callback_fn = value_assign(dic_or_list, key_or_index, st_key)
    return st.number_input(label, value=default_value, key=st_key, on_change=callback_fn, **kwargs)


def add_button(label, father_list, value, tag='', **kwargs):
    def item_add(father_list_, value_):
        def add():
            if father_list_ is list:
                father_list_.append(value_)
            elif father_list_ is dict:
                father_list_.update(value_)

        return add

    st_key = label + str(tag)
    callback_fn = item_add(father_list, value)
    return st.button(label, key=st_key, on_click=callback_fn, **kwargs)


def del_button(label, father_list, index, tag='', **kwargs):
    def item_delete(father_list_, index_):
        def delete():
            father_list_.pop(index_)

        return delete

    st_key = label + str(tag) + str(index)
    callback_fn = item_delete(father_list, index)
    return st.button(label, key=st_key, on_click=callback_fn, **kwargs)


def move_up_button(label, father_list, index, tag='', **kwargs):
    def item_move_up(father_list_, index_):
        def move_up():
            if index_ >= 1:
                father_list_[index_], father_list_[index_ - 1] = father_list_[index_ - 1], father_list_[index_]

        return move_up

    st_key = label + str(tag) + str(index)
    callback_fn = item_move_up(father_list, index)

    return st.button(label, key=st_key, on_click=callback_fn, **kwargs)


def editable_table(label, dict_, key, tag=''):
    st_key = label + str(tag)
    df = pd.DataFrame(dict_[key])
    edited_df = st.data_editor(df, key=label + str(tag), num_rows="dynamic")
    dict_[key] = edited_df.to_numpy().tolist()
