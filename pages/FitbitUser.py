import os.path
import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
from fitbit_uitls.fitbit_funcs import get_last_min_heart_data, get_live_heart_rate
from streamlit_js_eval import get_geolocation


def main():

    st.title("Fitbit User App")
    DATE = datetime.today().strftime('%Y-%m-%d')

    usr_data = None
    if 'user_data' in st.session_state and st.session_state['user_data'] != "INVALID":
        usr_data = st.session_state['user_data']
    else:
        st.switch_page("home.py")

    tab1, tab2, tab3, tab4 = st.tabs([f"{usr_data['name']}'s Home", "Contact Medical Professional", "Fitbit Logger", "Logout"])

    with tab1:
        loc = get_geolocation()
        st.markdown(":blue[Location Data]")
        st.dataframe(loc.get("coords"))
        st.divider()
        lat = loc.get("coords").get("latitude")
        lon = loc.get("coords").get("longitude")
        loc_df = pd.DataFrame([{"lat": lat, "lon": lon}])
        loc_df.to_csv("user_location.csv")
        st.markdown(f"Latitude - {lat} Longitude -{lon}")
        st.map(loc_df)
        # Open Google Maps in a new window with the current location
        google_maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        st.write(google_maps_url)
        st.divider()

    with tab2:
        st.header("Video Conference")
        st.markdown("Join Video Conference [Telko Live](https://telko.live/5bc36d47b87dad6c)")

    with tab3:
        st.image("https://cdn.iconscout.com/icon/free/png-256/free-fitbit-282220.png", width=200)
        st.subheader("Add your Fitbit API Refresh Toke and Start Data Logging ")
        with (open("./config.json") as f):
            data = json.load(f)
            access_token = data.get("access_token")

        fitbit_key = st.text_input(label="Fitbit Access Token", value=access_token)
        btn = st.button("Start Logging Heart Data")

        if btn:
            if os.path.exists("alarm.json"):
                with open("alarm.json", 'r') as f:
                    alarm_data = json.load(f)

            st.session_state['fitbit_key'] = fitbit_key

            df = get_live_heart_rate(access_token=fitbit_key, date=DATE)

            if os.path.exists("hrate.csv"):
                pdf = pd.read_csv("hrate.csv", index_col=0)
                df = pd.concat([pdf, df])

            df = df.sort_values(by="time")

            df["min_alarm"] = alarm_data.get("min")
            df["max_alarm"] = alarm_data.get("max")
            df.to_csv("hrate.csv")

            curr_hrate = df.value.tolist()[-1]

            if (curr_hrate >= alarm_data.get("min")) & (curr_hrate <= alarm_data.get("max")):
                st.markdown("### Patient is :green[safe]")
            else:
                st.markdown("### Patient is in :red[danger]")

            st.markdown("### Live Heart Rate")
            col1, col2 = st.columns([3, 1])

            col1.subheader("Graphical")
            col1.line_chart(df, x="time", y=["value", "min_alarm", "max_alarm"])

            col2.subheader("Data")
            col2.write(df)
            st.divider()

    with tab4:
        if st.button("Logout"):
            st.session_state['user_data'] = "INVALID"
            st.switch_page("home.py")

if __name__ == '__main__':
    main()
