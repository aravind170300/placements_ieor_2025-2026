import streamlit as st
import pandas as pd

# 1. Setup the Webpage
st.set_page_config(page_title="Placements - IEOR 2025 - 2026", layout="wide")
st.title("📊 Placements - IEOR 2025-2026")
st.markdown("Use the filters on the left to search and refine the data.")

# 2. Load the Data
@st.cache_data
def load_data():
    df = pd.read_excel("placements_ieor_sheet.xlsx", skiprows=2)

    # Drop the unnamed first column (empty column A in the sheet)
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

    # Forward-fill merged rows: these columns are left blank in sub-rows of merged cells
    cols_to_fill = ['S.No', 'Company Name', 'Sector', 'Category', 'CTC(p.a)', 'Gross(p.a)']
    df[cols_to_fill] = df[cols_to_fill].ffill()

    # Convert S.No to int for cleaner display
    df['S.No'] = df['S.No'].astype(int)

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

# Apply the master text search
if search_query:
    mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False))
    filtered_df = filtered_df[mask.any(axis=1)]

# Dropdown filters for low-cardinality object columns
categorical_cols = [col for col in df.columns if df[col].nunique() < 20 and df[col].dtype == 'object'
                    and col != 'Job Description']

for col in categorical_cols:
    options = sorted(df[col].dropna().unique().tolist())
    selected = st.sidebar.multiselect(f"Filter by {col}:", options=options, default=options)
    filtered_df = filtered_df[filtered_df[col].isin(selected)]

# 4. Make Job Description clickable links
def make_link(filename):
    if pd.isna(filename) or str(filename).strip() == '':
        return ''
    # Base URL where your PDFs are hosted — update this to your actual URL
    base_url = "https://raw.githubusercontent.com/aravind170300/placements_ieor_2025-2026/main/company/"
    return f'<a href="{base_url}{filename}" target="_blank">📄 View JD</a>'

display_df = filtered_df.copy()
display_df['Job Description'] = display_df['Job Description'].apply(make_link)

# 5. Display the Final Table
st.write(f"**Showing {len(filtered_df)} results:**")
st.write(
    display_df.to_html(escape=False, index=False),
    unsafe_allow_html=True
)
