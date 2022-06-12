import streamlit as st
import plotly.express as px
import pandas as pd
from skills import dict_category

df = pd.read_csv('./processed_data.csv')

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


st.set_page_config(layout="wide", page_icon="📈", page_title="DS skills app")

# Data visualisation part

st.title("Skills required for Junior Data Scientist jobs 📈")


st.sidebar.text('')
st.sidebar.markdown("**You can filter the data by choosing any company activity and/or company size you're interested in:** 👇")

st.sidebar.text('')
st.sidebar.text('')
all_activities = df['activity'].unique()
activities = st.sidebar.multiselect("Select the company activities you want to include.", all_activities)

st.sidebar.text('')
st.sidebar.text('')

all_sizes = df['size'].unique()
sizes = st.sidebar.multiselect("Select the company sizes you want to include.", all_sizes)


if len(activities) == 0 and len(sizes) == 0:
	df_filtered = df
elif len(sizes) == 0 and len(activities) != 0:
	df_filtered = df[df['activity'].isin(activities)]
elif len(activities) == 0 and len(sizes) != 0:
	df_filtered = df[df['size'].isin(sizes)]
else:
	df_filtered = pd.merge(df[df['activity'].isin(activities)], df[df['size'].isin(sizes)], how='inner')

D = {}
for x in dict_category:
  D[x] = sum(df_filtered[x])
data_to_plot = pd.DataFrame.from_dict({'Skills': [x for x in D], 'Total': [D[x] for x in D]})

fig = px.bar(data_to_plot.sort_values(by='Total', ascending=False), 
                x='Skills', 
                y='Total',
                width=1000, 
                height=570,
                color_discrete_sequence=['#FF4B4B']
                )

fig.update_layout(
    font=dict(
        size=14)
    )

st.plotly_chart(fig)
space(2)
st.subheader('Note:')
st.markdown('Each skill category includes multiple key words indicating or refering to the same category. For example:') 
st.markdown('- Deep Learning category includes Neural Networks, Tensorflow, PyTorch ...')
st.markdown('- Business Intelligence category includes tools like PowerBI, Tableau ...')
