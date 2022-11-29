import streamlit as st
st.title("Hello world")
from time import sleep

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def get_complementary(color):
    color = color[1:]
    color = int(color, 16)
    comp_color = 0xFFFFFF ^ color
    comp_color = "#%06X" % comp_color
    return comp_color

def change_bg_color(color):
    replace_line('.streamlit/config.toml', 3,f'backgroundColor="{color}"\n')

def change_fg_color(color):
    comp_color = get_complementary(color)
    replace_line('.streamlit/config.toml', 1,f'textColor="{comp_color}"\n')
    replace_line('.streamlit/config.toml', 2,f'primaryColor="{comp_color}"\n')

if st.button('Click', key="a"):
    st.write('Clicked')
else:
    st.write('Not clicked')

color = st.color_picker("Select a background color")

if st.button('Change colors', key="change"):
    change_bg_color(color)
    change_fg_color(color)
    sleep(2)
    st.experimental_rerun()