#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import io

def clean_excel(file):
    df = pd.read_excel(file, dtype=str)
    df.columns = df.columns.str.strip()

    cleaned_df = df.copy()
    changes_by_column = {}

    for col in df.columns:
        # Get original and cleaned versions of the column
        original_col = df[col].fillna("").astype(str)
        cleaned_col = original_col.str.replace('\n', ' ', regex=False)\
                                  .str.replace('\r', ' ', regex=False)\
                                  .str.strip()

        # Identify changed cells
        mask = original_col != cleaned_col

        if mask.any():
            # Apply cleaned column to the output DataFrame
            cleaned_df[col] = cleaned_col

            # Store changed rows
            changes = pd.DataFrame({
                "Row Number": (mask[mask].index + 2),  # Excel-style index
                "Original": original_col[mask].values,
                "Cleaned": cleaned_col[mask].values
            })

            changes_by_column[col] = changes.reset_index(drop=True)

    return cleaned_df, changes_by_column

def main():
    st.set_page_config(page_title="📊 Surf Excel - Line Break & Whitespace Cleaner", layout="wide")
    st.title("🧹 Excel Cleaner – Remove Line Breaks & Trim Whitespaces")

    uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx"])

    if uploaded_file is not None:
        with st.spinner("Cleaning file..."):
            cleaned_df, changes_by_column = clean_excel(uploaded_file)

        st.success("✅ File cleaned successfully!")

        st.subheader("🔍 Cleaned Data Preview")
        st.dataframe(cleaned_df.head(50))

        st.subheader("📝 Cells That Were Cleaned")
        if changes_by_column:
            for col, df_changes in changes_by_column.items():
                st.markdown(f"### Changes in Column: `{col}`")
                st.dataframe(df_changes)
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
