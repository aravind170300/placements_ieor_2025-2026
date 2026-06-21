import streamlit as st
import pandas as pd

# 1. Setup the Webpage
st.set_page_config(page_title="Placements - IEOR 2025 - 2026", layout="wide")
st.title("📊 Placements - IEOR 2025-2026")
st.markdown("Use the filters on the left to search and refine the data.")

# 2. Load the Data
@st.cache_data
def load_data():
    # skiprows=2 skips the empty rows at the top of your CSV so the headers align correctly
    df = pd.read_excel("placements_ieor_sheet.xlsx", skiprows=2) 
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ Error loading file: {e}. Please check the filename and location.")
    st.stop()

# 3. Create Dynamic Sidebar Filters
st.sidebar.header("🔍 Filter Options")

# Master text search
search_query = st.sidebar.text_input("Search all text data:")

filtered_df = df.copy()

# Apply the master text search if the user typed something
if search_query:
    # This searches across all columns by converting them to strings temporarily
    mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False))
    filtered_df = filtered_df[mask.any(axis=1)]

# Automatically create dropdown filters for columns that have fewer than 20 unique values (like Categories, Status, etc.)
categorical_cols = [col for col in df.columns if df[col].nunique() < 20 and df[col].dtype == 'object']

for col in categorical_cols:
    options = df[col].dropna().unique().tolist()
    selected = st.sidebar.multiselect(f"Filter by {col}:", options=options, default=options)
    # Apply the dropdown filter
    filtered_df = filtered_df[filtered_df[col].isin(selected)]

# 4. Display the Final Table
st.write(f"**Showing {len(filtered_df)} results:**")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
