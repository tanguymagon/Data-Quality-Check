import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import os
import tempfile
import io

st.set_page_config(layout="wide", page_title="Data Quality Check App", page_icon="📊")

# Apply custom CSS to adjust the layout and ensure tables/dataframes are responsive
st.markdown(
    """
    <style>
    /* Make dataframes take the full width */
    .dataframe {
        width: 100% !important;
    }
    
    /* Increase general font size */
    body {
        font-size: 16px;
    }

    /* Make the main container wider */
    .main {
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Profile report HTML scaling */
    .report-content {
        overflow-x: scroll;
    }
    </style>
    """, 
    unsafe_allow_html=True
)
# Streamlit app
def main():
    st.title("Data Quality Check App")
    
    # Upload an Excel file
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    
    if uploaded_file:
        # different sheets from the file
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names
        
        st.write("### Select a sheet")
        selected_sheet = st.selectbox("Sheets", sheet_names)
        
        # Load + preview the selected sheet
        if selected_sheet:
            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet, header=None)
            st.write("### Sheet Preview (first 20 rows):")
            st.dataframe(df.head(20))
            
            # Select header row
            st.write("### Select the header row")
            header_row = st.number_input("Select the header row (0-indexed)", min_value=0, max_value=len(df)-1, value=0)
            
            # Apply the header selection
            if st.button("Apply Header"):
                df_with_header = pd.read_excel(uploaded_file, sheet_name=selected_sheet, header=header_row)
                st.write("### Data Preview with Selected Header:")
                st.dataframe(df_with_header.head(10))
                
                # Generate the report
                st.write("### Generating the Profile Report...")
                profile = ProfileReport(df_with_header, explorative=True)
                
                # Display the report
                st_profile_report(profile)
                
                # Generate the HTML report
                st.write("### View or Download the Profile Report as HTML")
                profile_html = profile.to_html()

                # Convert the HTML to a byte object
                report_file = io.BytesIO(profile_html.encode('utf-8'))

                # Download button to download the HTML file
                st.download_button(
                    label="Download Profile Report as HTML",
                    data=report_file,
                    file_name="profile_report.html",
                    mime="text/html"
                )

if __name__ == "__main__":
    main()
