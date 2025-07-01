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

    # Check for duplicate business names
    duplicate_names = df[df['business_name'].duplicated(keep=False)]
    if not duplicate_names.empty:
        st.warning("Duplicate business names found in the data. Please ensure each business name is unique.")
        st.dataframe(duplicate_names[['business_name', 'contact_name', 'email_address']])

    # Select a client by business name
    st.subheader("Select a Client")
    # Sort business names alphabetically and remove duplicates for the dropdown
    client_names = sorted(df['business_name'].drop_duplicates().tolist())
    selected_client = st.selectbox("Choose a client", options=client_names, key="client_select")

    if selected_client:
        # Get the selected client's data (first occurrence if duplicates exist)
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
            invoiced = client_data['invoiced']
            quoted = client_data['quoted']
            st.write(f"**Invoiced**: ${invoiced:.2f}" if pd.notna(invoiced) else "**Invoiced**: Not available")
            st.write(f"**Quoted**: ${quoted:.2f}" if pd.notna(quoted) else "**Quoted**: Not available")
            st.write(f"**Status**: {client_data['status']}")
            st.write(f"**Products**: {client_data['products']}")
            st.write(f"**Product Line**: {client_data['product_line']}")
            st.write(f"**Contacted**: {'Yes' if client_data['contacted'] in [1, '1', 'Yes', 'yes', True] else 'No'}")
            st.write(f"**Marketed**: {'Yes' if client_data['marketed'] in [1, '1', 'Yes', 'yes', True] else 'No'}")
            st.write(f"**Emailed**: {'Yes' if client_data['emailed'] in [1, '1', 'Yes', 'yes', True] else 'No'}")

if __name__ == "__main__":
    main()
