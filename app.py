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
                # Convert invoiced and quoted to float, handling errors
                try:
                    df['invoiced'] = pd.to_numeric(df['invoiced'], errors='coerce')
                    df['quoted'] = pd.to_numeric(df['quoted'], errors='coerce')

                    # Identify rows with NaN in invoiced or quoted
                    invalid_rows = df[df['invoiced'].isna() | df['quoted'].isna()]
                    if not invalid_rows.empty:
                        st.warning("Some 'invoiced' or 'quoted' values could not be converted to numbers and were set to NaN.")
                        st.subheader("Rows with Invalid Data")
                        # Display relevant columns for debugging
                        st.dataframe(invalid_rows[['business_name', 'invoiced', 'quoted', 'status', 'products']])
                        st.write("The above rows have non-numeric values in 'invoiced' or 'quoted'. Please correct these to numeric values (e.g., 5000.00 or 0) in your CSV and re-upload.")

                        # Create a cleaned DataFrame by dropping NaN rows
                        cleaned_df = df.dropna(subset=['invoiced', 'quoted'])
                        if not cleaned_df.empty:
                            # Offer download of cleaned CSV
                            csv = cleaned_df.to_csv(index=False)
                            st.download_button(
                                label="Download Cleaned CSV (NaN rows removed)",
                                data=csv,
                                file_name="cleaned_clients.csv",
                                mime="text/csv"
                            )
                            st.session_state['client_data'] = cleaned_df
                            st.success("Valid rows stored. Navigate to other pages to visualize the data.")
                        else:
                            st.error("No valid rows remain after removing NaN values. Storing original data to allow inspection.")
                            st.write("You can still navigate to other pages to view non-numeric fields like 'status' and 'products'. Please fix the CSV for full functionality.")
                            st.session_state['client_data'] = df  # Store original DataFrame
                    else:
                        st.success("All 'invoiced' and 'quoted' values are valid numbers.")
                        st.session_state['client_data'] = df

                    # Display the first few rows
                    st.subheader("Preview of Uploaded Data")
                    st.dataframe(df[['business_name', 'invoiced', 'quoted', 'status', 'products']].head())
                except Exception as e:
                    st.error(f"Error converting numeric columns: {e}")
                    return
            else:
                st.error(f"CSV must contain the following columns: {', '.join(expected_columns)}")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Please upload a CSV file to proceed.")

if __name__ == "__main__":
    main()
