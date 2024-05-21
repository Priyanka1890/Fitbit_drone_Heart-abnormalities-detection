import streamlit as st
import streamlit.components.v1 as components
import pandas as pd





def main():


    st.title("DroneComputer")
    usr_data = None
    if 'user_data' in st.session_state and st.session_state['user_data'] != "INVALID":
        usr_data = st.session_state['user_data']
    else:
        st.switch_page("home.py")

    tab1, tab2, tab3 = st.tabs([f"{usr_data['name']}'s Data", "Drone Simulator", "Logout"])
    
    

    with tab1:

        user_data = ["N. John", "V. Hammar", "D. Luke", "M. Kalus", "P. Dey"]
        alarm_data =["Safe", "Safe", "Safe", "Safe"]
        lat_data = ["NA", "NA", "NA", "NA"]
        lon_data = ["NA", "NA", "NA","NA"]

        df = pd.read_csv("user_location.csv")
        lat = df.lat.tolist()[0]
        lat_data.append(lat)
        lon = df.lon.tolist()[0]
        lon_data.append(lon)
        df = pd.read_csv("hrate.csv")
        hrate = df.value.tolist()[-1]
        min_al = df.min_alarm.tolist()[-1]
        max_al = df.max_alarm.tolist()[-1]




        if (hrate <= max_al) & (hrate >= min_al):
            alarm_data.append("Safe")
        else:
            alarm_data.append("Danger")

        df = pd.DataFrame({
            "idx":[1, 2, 3, 4, 5],
            "user_name":user_data,
            "user_loc_lat":lat_data,
            "user_loc_lon": lon_data,
            "alarm":alarm_data
        })
        st.markdown("### User List ")
        st.dataframe(df)


    with tab2:

        markdown = """
    The drone computer is connected with drone via Mission Planner (https://ardupilot.org/planner/)
    """

        st.markdown(markdown)
        components.html(
        '''
        <iframe
        src="https://vnc.eu1.pitunnel.com/novnc/vnc.html?autoconnect=1&resize=scale&quality=5&compression=7&show_dot=1&path=PGuJOQwq5Fx9lsYPC97PG7qnWLm3oMCD2VJsdHfHeP7qmIMsK94e4Tm2UpfdGBq7RIGp8Nb5NCPc2x7Tr5aexakS9hYPSMzvrlNBanYlWATDC592ZvhYQThKKjPhpEgR/websockify?embed=true"
            height=500 width=750></iframe>
        ''',
        height=900,
        width=900
    )


    with tab3:
        if st.button("Logout"):
            st.session_state['user_data'] = "INVALID"
            st.switch_page("home.py")

        
        
        

        


if __name__ == '__main__':
    main()

