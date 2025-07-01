import streamlit as st
import pandas as pd

st.set_page_config(page_title="Client Notes", layout="wide")

def main():
    st.title("Client Notes")

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
    client_names = sorted(df['business_name'].drop_duplicates().tolist())
    selected_client = st.selectbox("Choose a client by business name", options=client_names, key="notes_client_select")

    if selected_client:
        # Get the selected client's data (first occurrence if duplicates exist)
        client_index = df[df['business_name'] == selected_client].index[0]
        client_data = df.loc[client_index]

        st.subheader(f"Notes for {client_data['business_name']}")

        # Notes fields
        notes_fields = [
            'needs', 'wants', 'requirements', 'features', 'functionality',
            'current problem', 'current process', 'current tools',
            'current constraints', 'current limitations', 'current competitors',
            'competitors products', 'competitors services', 'scope of project work',
            'primary contact'
        ]

        # Create two columns for layout
        col1, col2 = st.columns(2)

        # Dictionary to store updated values
        updated_values = {}

        # Display fields in two columns
        for i, field in enumerate(notes_fields):
            # Convert field name to title case and replace underscores with spaces
            field_display = field.replace('_', ' ').title()
            # Check if field exists in DataFrame, else use empty string
            current_value = client_data[field] if field in client_data.index and pd.notna(client_data[field]) else ""
            # Assign to alternating columns
            with col1 if i % 2 == 0 else col2:
                updated_values[field] = st.text_area(f"{field_display}", value=current_value, height=100, key=f"notes_{field}_{client_index}")

        # Save button
        if st.button("Save Notes", key=f"save_notes_{client_index}"):
            # Ensure all notes fields exist in DataFrame
            for field in notes_fields:
                if field not in df.columns:
                    df[field] = pd.NA  # Add missing column with NA values
            # Update the DataFrame with new values
            for field, value in updated_values.items():
                st.session_state['client_data'].loc[client_index, field] = value
            st.success("Notes saved successfully!")

if __name__ == "__main__":
    main()
