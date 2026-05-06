# PhonePe Transaction Insights

## Description
End-to-end data science project on the PhonePe Pulse dataset. This project involves extracting data from the PhonePe Pulse GitHub repository, transforming it, and loading it into a MySQL database. It features comprehensive Exploratory Data Analysis (EDA), Machine Learning models for predictive analytics, and an interactive Streamlit dashboard for data visualization.

## Technologies Used
*   Python (Pandas, Numpy)
*   MySQL (mysql-connector-python, sqlalchemy)
*   Data Visualization: Matplotlib, Seaborn, Plotly Express
*   Machine Learning: Scikit-Learn, XGBoost, Joblib, SHAP
*   Web Application: Streamlit, streamlit-option-menu
*   Version Control: GitPython, PyGithub

## Dataset
Data is extracted from the official [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse).

## Setup Instructions

### 1. Install Requirements
Install all necessary Python packages:
```bash
pip install -r requirements.txt
```

### 2. Configure Database Credentials
Open `config.py` and update the database credentials with your MySQL username and password:
```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "phonepe_pulse"
```

### 3. Extract and Load Data
Run the data extraction pipeline. This will clone the PhonePe Pulse repository, parse the JSON files, create the MySQL database schema, and load all the data.
```bash
python data_extraction.py
```

### 4. Run Notebooks (Optional)
To view the EDA and ML steps, you can run the provided Jupyter notebooks:
*   `EDA_Notebook.ipynb`
*   `ML_Notebook.ipynb`

### 5. Launch the Dashboard
Run the Streamlit application to explore the interactive dashboard:
```bash
streamlit run app.py
```

## Dashboard Screenshots

*Placeholder for Home Page Screenshot*
![Home](https://via.placeholder.com/800x400.png?text=Home+Page)

*Placeholder for Transaction Analysis Screenshot*
![Transaction Analysis](https://via.placeholder.com/800x400.png?text=Transaction+Analysis)
