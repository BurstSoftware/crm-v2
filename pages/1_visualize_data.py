# pages/1_visualize_data.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Visualize Client Data", layout="wide")

def main():
    st.title("Client Data Visualizations")
    
    # Check if data exists in session state
    if 'client_data' not in st.session_state:
        st.error("No data uploaded. Please go to the main page and upload a CSV file.")
        return

    df = st.session_state['client_data']
    
    st.subheader("Dataset Overview")
    st.dataframe(df.head())

    # Create columns for visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Status Distribution
        st.subheader("Status Distribution")
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        fig_status = px.pie(status_counts, names='status', values='count', title="Client Status Distribution")
        st.plotly_chart(fig_status, use_container_width=True)

        # Contacted/Marketed/Emailed Breakdown
        st.subheader("Contact Activity")
        activity = pd.DataFrame({
            'Activity': ['Contacted', 'Marketed', 'Emailed'],
            'Count': [
                df['contacted'].sum() if pd.api.types.is_numeric_dtype(df['contacted']) else df['contacted'].str.lower().eq('yes').sum(),
                df['marketed'].sum() if pd.api.types.is_numeric_dtype(df['marketed']) else df['marketed'].str.lower().eq('yes').sum(),
                df['emailed'].sum() if pd.api.types.is_numeric_dtype(df['emailed']) else df['emailed'].str.lower().eq('yes').sum()
            ]
        })
        fig_activity = px.bar(activity, x='Activity', y='Count', title="Contact Activity Counts")
        st.plotly_chart(fig_activity, use_container_width=True)

    with col2:
        # Invoiced vs Quoted
        st.subheader("Invoiced vs Quoted Amounts")
        fig_amounts = go.Figure()
        fig_amounts.add_trace(go.Histogram(x=df['invoiced'], name='Invoiced', opacity=0.5))
        fig_amounts.add_trace(go.Histogram(x=df['quoted'], name='Quoted', opacity=0.5))
        fig_amounts.update_layout(barmode='overlay', title="Invoiced vs Quoted Distribution")
        st.plotly_chart(fig_amounts, use_container_width=True)

        # Product Line Distribution
        st.subheader("Product Line Distribution")
        product_line_counts = df['product_line'].value_counts().reset_index()
        product_line_counts.columns = ['product_line', 'count']
        fig_product = px.bar(product_line_counts, x='product_line', y='count', title="Product Line Distribution")
        st.plotly_chart(fig_product, use_container_width=True)

if __name__ == "__main__":
    main()
