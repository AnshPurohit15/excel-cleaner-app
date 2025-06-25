#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import io

def clean_excel(file):
    # Read all cells as strings to avoid NaN for blanks
    df = pd.read_excel(file, dtype=str)

    # Strip column names
    df.columns = df.columns.str.strip()

    cleaned_df = df.copy()
    changes = []

    # Clean cell values: remove line breaks, trim whitespaces
    for col in df.columns:
        for i, val in df[col].items():
            original = str(val) if pd.notnull(val) else ''
            cleaned = original.replace('\n', ' ').replace('\r', ' ').strip()
            if original != cleaned:
                changes.append({
                    "Row": i + 2,  # Excel-style index
                    "Column": col,
                    "Original": original,
                    "Cleaned": cleaned
                })
                cleaned_df.at[i, col] = cleaned

    changes_df = pd.DataFrame(changes)
    return cleaned_df, changes_df

def main():
    st.set_page_config(page_title="📊 Surf Excel - Line Break & Whitespace Cleaner", layout="wide")
    st.title("🧹 Excel Cleaner – Remove Line Breaks & Trim Whitespaces")

    uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx"])

    if uploaded_file is not None:
        with st.spinner("Cleaning file..."):
            cleaned_df, changes_df = clean_excel(uploaded_file)

        st.success("✅ File cleaned successfully!")

        st.subheader("🔍 Cleaned Data Preview")
        st.dataframe(cleaned_df.head(50))

        # Show cleaned cells only
        st.subheader("📝 Cells That Were Cleaned")
        if not changes_df.empty:
            st.dataframe(changes_df)
        else:
            st.info("No cleaning was needed — all cells were already clean!")

        # Download cleaned file
        towrite = io.BytesIO()
        cleaned_df.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)

        st.download_button(
            label="📥 Download Cleaned Excel File",
            data=towrite,
            file_name="cleaned_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
