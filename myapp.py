import streamlit as st
import pandas as pd
import numpy as np 
import pickle
import datetime
import sklearn
import math                      

st.write("""
# Web application : Data Mining
""")

@st.cache 
def import_data_q3():
    return pd.read_csv('./data_sort_speed.csv', index_col=0)

add_selectbox = st.sidebar.selectbox(
    "Choose",
    ("Question 1", "Question 2", "Question 3", "Question 4")
)

if add_selectbox == 'Question 1':
    st.write("Question 1")
    # Importation du train.csv
    #df = pd.read_csv('data_sort_speed.csv', index_col=0)
    # df = df.astype(str)
    # st.write(df.head())
    # st.metric(label="Speed", value="45 km/h", delta="1.5 more than average")

elif add_selectbox == 'Question 2':
    st.write("Question 2")

elif add_selectbox == 'Question 3':
    st.write("Question 3")

    df = import_data_q3()
    st.write(df.head(2))
    # start_stop_id = st.selectbox('Select start stop', 
    #                              [str(elt)+' ('+df[df['stop_id'] == elt]['descr_fr'].unique()[0]+')' 
    #                               for elt in df['stop_id'].unique()])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write('Position')
        start_stop_id = st.selectbox('Select start stop', 
                                 df['stop_id'].unique()
                                )

        arrival_stop_id = st.selectbox('Select arrival stop', 
                                    [str(elt)+' ('+df[df['stop_id'] == elt]['descr_fr'].unique()[0]+')' for elt in
                                     df[df['trip_id'].isin(df[df['stop_id'] == start_stop_id]['trip_id'])]['stop_id'].unique()]
                                  )
     
        line_id = st.selectbox('Select line',
                            df[(df['trip_id'].isin(df[df['stop_id'] == start_stop_id]['trip_id'])) & 
                               (df['trip_id'].isin(df[df['stop_id'] == arrival_stop_id.split(' (')[0]]['trip_id']))]['Code_Ligne'].unique())

    with col2:
        st.write('Time')
        date = st.date_input("Select date", datetime.date.today())
        year = date.year
        month = date.month
        day_number = date.day
        import calendar
        day_str = calendar.day_name[date.weekday()].lower()

        time = st.selectbox('Select time start', 
                            [f'{h}:{m}:{s}' 
                            if (m>9) and (s>9) 
                            else f'{h}:0{m}:{s}' if (m<=9) and (s>9)
                            else f'{h}:{m}:0{s}' if (m>9) and (s<=9) 
                            else f'{h}:0{m}:0{s}'
                            for h in ['00','01','02','03','04','05','06','07','08','09','10',
                                      '11','12','13','14','15','16','17','18','19','20','21',
                                      '22','23']
                            for m in range(60) 
                            for s in range(60)])
                                      
        type_time = datetime.datetime.strptime(time, '%H:%M:%S')   
        nb_seconds = (type_time.hour * 3600)+(type_time.minute*60)+(type_time.second)

    with col3:
        st.write('Prediction')
        data_for_pred = [1 if elt==day_str else 0 for elt in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']] +[int(year), int(month), int(day_number), nb_seconds, int(arrival_stop_id[:4]), int(start_stop_id[:4])]
        
        #  Order : 'monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday',
        #          'start_date_year', 'start_date_month', 'start_date_day',
        #          'start_nb_of_seconds', 'stop_id_int','previous_stop_id_int'

        # load saved model
        with open('model_q3_pkl' , 'rb') as f:
            model_q3 = pickle.load(f)
        f.close()

        pred = model_q3.predict(np.array(data_for_pred).reshape(1,13))[0]
        hour_pred = pred//3600
        second_pred, minute_pred = math.modf(((pred/3600)-hour_pred)*60)
        st.write('Arrival time :')
        h = int(hour_pred)
        m = int(minute_pred)
        s = int(second_pred*60)
        if (h>9) and (m>9) and (s>9):
            st.write(f'{h}:{m}:{s}') 
        elif (h>9) and (m<=9) and (s>9):
            st.write(f'{h}:0{m}:{s}')
        elif (h>9) and (m>9) and (s<=9):
            st.writ(f'{h}:{m}:0{s}')
        elif (h<=9) and (m>9) and (s>9):
            st.write(f'0{h}:{m}:{s}') 
        elif (h<=9) and (m<=9) and (s>9):
            st.write(f'0{h}:0{m}:{s}')
        elif (h>=9) and (m>9) and (s<=9):
            st.writ(f'0{h}:{m}:0{s}')
        elif (h>9) and (m<=9) and (s<=9):
            st.writ(f'0{h}:0{m}:0{s}')
        else:
            st.write(f'0{h}:0{m}:0{s}')

elif add_selectbox == 'Question 4':
    st.write("Question 4")

    gps_tracks = pd.read_csv('gps_tracks_df.csv', index_col=0)
    
    import plotly.express as px
    fig = px.line(gps_tracks, 
                x=[i for track_id in gps_tracks['TrackId'].unique() for i in range(gps_tracks[gps_tracks['TrackId'] == track_id].shape[0])], 
                y="vitesse", title='Vitesse (km/h)',
                color="TrackId")
    st.plotly_chart(fig)
    
