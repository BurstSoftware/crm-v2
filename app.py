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

            # Updated expected columns
            expected_columns = [
                'invoiced', 'quoted', 'status', 'products', 'product_line',
                'contacted', 'contact_name', 'business_name', 'phone_number',
                'email_address', 'business_address', 'city', 'state',
                'zip_code', 'social_media_links'
            ]

            # Validate columns
            if all(col in df.columns for col in expected_columns):
                # Convert invoiced and quoted to float, handling errors
                df['invoiced'] = pd.to_numeric(df['invoiced'], errors='coerce')
                df['quoted'] = pd.to_numeric(df['quoted'], errors='coerce')

                # Identify rows with NaN in invoiced or quoted
                invalid_rows = df[df['invoiced'].isna() | df['quoted'].isna()]
                if not invalid_rows.empty:
                    st.warning("Some 'invoiced' or 'quoted' values could not be converted to numbers and were set to NaN.")
                    st.subheader("Rows with Invalid Data")
                    st.dataframe(invalid_rows[['business_name', 'invoiced', 'quoted', 'status', 'products']])
                    st.write("Please correct 'invoiced' and 'quoted' to numeric values (e.g., 5000.00 or 0) in your CSV and re-upload.")

                # Store the DataFrame in session state
                st.session_state['client_data'] = df
                st.success("Data uploaded successfully! Navigate to the Client Details page to view individual client information.")

                # Display preview
                st.subheader("Preview of Uploaded Data")
                st.dataframe(df[['business_name', 'invoiced', 'quoted', 'status', 'products']].head())
            else:
                st.error(f"CSV must contain the following columns: {', '.join(expected_columns)}")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Please upload a CSV file to proceed.")

if __name__ == "__main__":
    main()
