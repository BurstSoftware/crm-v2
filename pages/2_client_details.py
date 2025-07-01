# pages/2_client_details.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Client Details", layout="wide")

def main():
    st.title("Client Details")

    # Check if data exists in session state
    if 'client_data' not in st.session_state:
        st.error("No data uploaded. Please go to the main page and upload a CSV file.")
        return

    df = st.session_state['client_data']

    # Select a client by business name or index
    st.subheader("Select a Client")
    client_names = df['business_name'].tolist()
    selected_client = st.selectbox("Choose a client", options=client_names)

    if selected_client:
        # Get the selected client's data
        client_data = df[df['business_name'] == selected_client].iloc[0]

        st.subheader(f"Details for {client_data['business_name']}")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Basic Information**")
            st.write(f"**Contact Name**: {client_data['contact_name']}")
            st.write(f"**Business Name**: {client_data['business_name']}")
            st.write(f"**Phone Number**: {client_data['phone_number']}")
            st.write(f"**Email Address**: {client_data['email_address']}")
            st.write(f"**Business Address**: {client_data['business_address']}")
            st.write(f"**Social Media Links**: {client_data['social_media_links']}")

        with col2:
            st.write("**Business Details**")
            st.write(f"**Invoiced**: ${client_data['invoiced']:.2f}")
            st.write(f"**Quoted**: ${client_data['quoted']:.2f}")
            st.write(f"**Status**: {client_data['status']}")
            st.write(f"**Products**: {client_data['products']}")
            st.write(f"**Product Line**: {client_data['product_line']}")
            st.write(f"**Contacted**: {'Yes' if client_data['contacted'] else 'No'}")
            st.write(f"**Marketed**: {'Yes' if client_data['marketed'] else 'No'}")
            st.write(f"**Emailed**: {'Yes' if client_data['emailed'] else 'No'}")

if __name__ == "__main__":
    main()
