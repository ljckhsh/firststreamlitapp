import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
def load_data():
    file_path = 'PC_urinary_marker.csv'
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("The dataset file was not found. Please ensure 'PC_urinary_marker.csv' is in the correct location.")
        return pd.DataFrame()

data = load_data()

# Check if data is loaded successfully
if data.empty:
    st.stop()

# Streamlit app setup
st.title("PC Urinary Marker Analysis")
st.markdown(
    "This app provides an overview and analysis of the urinary marker dataset.")

# Display dataset overview
if st.checkbox("Show dataset overview"):
    st.write(data.head())
    st.write("Shape of the dataset:", data.shape)
    st.write("Column information:")
    buffer = []
    data.info(buf=buffer.append)
    st.text("\n".join(buffer))

# Summary statistics
if st.checkbox("Show summary statistics"):
    st.write(data.describe())

# Missing values
if st.checkbox("Show missing values summary"):
    missing_summary = data.isnull().sum()
    st.write(missing_summary)

# Visualize data distribution
st.header("Data Distribution")
selected_column = st.selectbox("Select a column to visualize", data.select_dtypes(include=['float64', 'int64']).columns)

if selected_column:
    fig, ax = plt.subplots()
    data[selected_column].dropna().hist(bins=20, ax=ax, color='skyblue', edgecolor='black')
    ax.set_title(f"Distribution of {selected_column}")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

# Age distribution by diagnosis
if st.checkbox("Show age distribution by diagnosis"):
    st.subheader("Age Distribution by Diagnosis")
    diagnosis_map = {1: "Healthy", 2: "Benign Disease", 3: "Pancreatic Cancer"}
    if "diagnosis" in data.columns:
        data["diagnosis_label"] = data["diagnosis"].map(diagnosis_map)
        if "age" in data.columns:
            fig, ax = plt.subplots()
            data.boxplot(column="age", by="diagnosis_label", ax=ax, grid=False, showfliers=False,
                         boxprops=dict(color="blue"), medianprops=dict(color="red"))
            ax.set_title("Age Distribution by Diagnosis")
            ax.set_xlabel("Diagnosis")
            ax.set_ylabel("Age")
            plt.suptitle("")  # Remove default subtitle
            st.pyplot(fig)
        else:
            st.error("The 'age' column is missing in the dataset.")
    else:
        st.error("The 'diagnosis' column is missing in the dataset.")

# CA19-9 levels by diagnosis
if st.checkbox("Show CA19-9 levels by diagnosis"):
    st.subheader("CA19-9 Levels by Diagnosis")
    if "diagnosis" in data.columns and "plasma_CA19_9" in data.columns:
        diagnosis_map = {1: "Healthy", 2: "Benign Disease", 3: "Pancreatic Cancer"}
        data["diagnosis_label"] = data["diagnosis"].map(diagnosis_map)
        fig, ax = plt.subplots()
        data.boxplot(column="plasma_CA19_9", by="diagnosis_label", ax=ax, grid=False, showfliers=False,
                     boxprops=dict(color="blue"), medianprops=dict(color="red"))
        ax.set_title("CA19-9 Levels by Diagnosis")
        ax.set_xlabel("Diagnosis")
        ax.set_ylabel("CA19-9 Levels")
        plt.suptitle("")  # Remove default subtitle
        st.pyplot(fig)
    else:
        st.error("The required columns ('diagnosis', 'plasma_CA19_9') are missing in the dataset.")

# LYVE1 levels by pancreatic cancer stage
if st.checkbox("Show LYVE1 levels by pancreatic cancer stage"):
    st.subheader("LYVE1 Levels by Pancreatic Cancer Stage")
    if "diagnosis" in data.columns and "stage" in data.columns and "LYVE1" in data.columns:
        cancer_stages = data[data["diagnosis"] == 3]  # Filter for pancreatic cancer patients
        fig, ax = plt.subplots()
        cancer_stages.boxplot(column="LYVE1", by="stage", ax=ax, grid=False, showfliers=False,
                               boxprops=dict(color="blue"), medianprops=dict(color="red"))
        ax.set_title("LYVE1 Levels by Stage")
        ax.set_xlabel("Pancreatic Cancer Stage")
        ax.set_ylabel("LYVE1 Levels")
        plt.suptitle("")  # Remove default subtitle
        st.pyplot(fig)
    else:
        st.error("The required columns ('diagnosis', 'stage', 'LYVE1') are missing in the dataset.")

st.markdown("---")
st.markdown("Developed for quick insights into urinary marker data.")
