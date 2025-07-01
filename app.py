# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Client Data Dashboard", layout="wide")

def main():
    st.title("Client Data Import")
    st.write("Upload a CSV file containing client data.")

    # File uploader for CSV
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)

            # Expected columns
            expected_columns = [
                'invoiced', 'quoted', 'status', 'products', 'product_line', 
                'contacted', 'marketed', 'emailed', 'contact_name', 
                'business_name', 'phone_number', 'email_address', 
                'business_address', 'social_media_links'
            ]

            # Validate columns
            if all(col in df.columns for col in expected_columns):
                # Store the dataframe in session state
                st.session_state['client_data'] = df
                st.success("File uploaded successfully! Navigate to other pages to visualize the data.")
                
                # Display the first few rows
                st.subheader("Preview of Uploaded Data")
                st.dataframe(df.head())
            else:
                st.error(f"CSV must contain the following columns: {', '.join(expected_columns)}")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Please upload a CSV file to proceed.")

if __name__ == "__main__":
    main()
