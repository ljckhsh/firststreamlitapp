import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
def load_data():
    file_path = 'PC_urinary_marker.csv'
    return pd.read_csv(file_path)

data = load_data()

# Streamlit app setup
st.title("Pancreatic Cancer의 Urinary Biomarker 분석")
st.markdown(
    "This app provides an overview and analysis of the urinary marker dataset.")

# Display dataset overview
if st.checkbox("Show dataset overview"):
    st.write(data.head())
    st.write("Shape of the dataset:", data.shape)
    st.write("Column information:")
    st.write(data.info())

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
    data[selected_column].hist(bins=20, ax=ax, color='skyblue', edgecolor='black')
    ax.set_title(f"Distribution of {selected_column}")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

# Correlation heatmap
if st.checkbox("Show correlation heatmap"):
    st.subheader("Correlation Matrix")
    corr_matrix = data.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    cax = ax.matshow(corr_matrix, cmap='coolwarm')
    plt.colorbar(cax)
    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_yticks(range(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, rotation=90)
    ax.set_yticklabels(corr_matrix.columns)
    st.pyplot(fig)

# Age distribution by diagnosis
if st.checkbox("Show age distribution by diagnosis"):
    st.subheader("Age Distribution by Diagnosis")
    fig, ax = plt.subplots()
    for diagnosis, group in data.groupby("diagnosis"):
        group["age"].plot(kind='kde', ax=ax, label=f"Diagnosis {diagnosis}")
    ax.set_title("Age Distribution by Diagnosis")
    ax.set_xlabel("Age")
    ax.legend()
    st.pyplot(fig)
    

st.markdown("---")
st.markdown("Developed for quick insights into urinary marker data.")

# CA19-9 levels by diagnosis
if st.checkbox("Show CA19-9 levels by diagnosis"):
    st.subheader("CA19-9 Levels by Diagnosis")
    diagnosis_map = {1: "Healthy population", 2: "Benign Diseases", 3: "Pancreatic Cancer"}
    data["diagnosis_label"] = data["diagnosis"].map(diagnosis_map)
    fig, ax = plt.subplots()
    data.boxplot(column="plasma_CA19_9", by="diagnosis_label", ax=ax, grid=False, showfliers=False,
                 boxprops=dict(color="blue"), medianprops=dict(color="red"))
    ax.set_title("CA19-9 Levels by Diagnosis")
    ax.set_xlabel("Diagnosis")
    ax.set_ylabel("CA19-9 Levels")
    plt.suptitle("")  # Remove default subtitle
    st.pyplot(fig)

st.markdown("---")
st.markdown("Developed for quick insights into urinary marker data.")
