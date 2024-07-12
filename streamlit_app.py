import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from pprint import pprint
from datetime import datetime

# logo_url = ''
# st.image(logo_url)

title = '# FAIR Assessment of HuBMAP data'
st.write(title)

authors = 'Bailey, T.; Chen, J.; Esmaeeli, A.; Hernandez, Y.; Ho, M.; Lampejo, M.; Ma, J.; Martinez, G.; Rubio Martinez, V.; Forchap, E.; Mathurin, S.; Omar, Y.; Segil, J.; McLeod, A.; Cao-Berg, I.'
st.write(authors)

today = 'Today''s date'
st.write(today)

intro = '''
This is some text
'''
st.write(intro)

## DO NOT MODIFY THIS BLOCK
# Function to determine the type
def determine_type(dataset_type: str) -> str:
    if '[' in dataset_type and ']' in dataset_type:
        return 'Derived'
    else:
        return 'Primary'

@st.cache_data
def get_data() -> pd.DataFrame:
    """
    Fetch data from a predefined URL, extract the 'data' key,
    and return it as a DataFrame.

    Returns:
    pd.DataFrame: The data extracted from the 'data' key loaded into a DataFrame.
    """
    url = "https://ingest.api.hubmapconsortium.org/datasets/data-status"  # The URL to get the data from
    try:
        response = requests.get(url)  # Send a request to the URL to get the data
        response.raise_for_status()  # Check if the request was successful (no errors)
        json_data = response.json()  # Convert the response to JSON format

        # Ensure 'data' key exists in the JSON
        if 'data' in json_data:  # Check if the JSON contains the key 'data'
            df = pd.DataFrame(json_data['data'])  # Create a DataFrame using the data under 'data' key
            df = df[df['status']=='Published']
            df['dataset_status'] = df['dataset_type'].apply(determine_type)
            print("Data successfully loaded.")  # Print a message indicating success
        else:
            raise KeyError("'data' key not found in the JSON response")  # Raise an error if 'data' key is missing

        return df  # Return the DataFrame with the data
    except (ValueError, KeyError) as e:  # Catch errors related to value or missing keys
        print(f"Error loading data: {e}")  # Print the error message
        return pd.DataFrame()  # Return an empty DataFrame if there is an error
    except requests.RequestException as e:  # Catch errors related to the request itself
        print(f"Request failed: {e}")  # Print the error message
        return pd.DataFrame()  # Return an empty DataFrame if the request fails

df = get_data()
## DO NOT MODIFY THIS BLOCK

text = '## Published data'
st.write(text)

text = '### At a Glance'
st.write(text)

number_of_datasets = None
text = f'There are {number_of_datasets} published datasets'
st.write(text)

number_of_organs = None
text = f'There are 55 3D organs, 1203 tissue blocks'
st.write(text)

text = '### Datasets'
st.write(text)

text = '### Data access level'
st.write(text)

# Count the occurrences of each data access level in the dataframe
access_level_counts = df['data_access_level'].value_counts()
access_level_counts.plot(kind='bar', color='skyblue')
plt.title('Data Access Level Distribution')
plt.xlabel('Data Access Level')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

text = '### Group name Dataset'
st.write(text)
import matplotlib.pyplot as plt

# Count the occurrences of each data access level in the dataframe
access_level_counts = df['group_name'].value_counts()

# Increase figure size for better readability
plt.figure(figsize=(10, 6))  # Adjust width and height as necessary

# Start making a bar chart to visualize the data
# This will create a bar chart where each bar represents a different data access level
access_level_counts.plot(kind='bar', color='skyblue', width=0.8)  # 'width' adjusts the width of the bars

# Add a title to the top of the chart
plt.title('Research group name', fontsize=16)  # Increase font size for the title

# Label the x-axis (horizontal axis)
plt.xlabel('University', fontsize=14, labelpad=15)  # Increase font size for the x-axis label and add padding

# Label the y-axis (vertical axis)
plt.ylabel('Count', fontsize=14)  # Increase font size for the y-axis label

# Rotate the labels on the x-axis to 45 degrees for better readability
plt.xticks(rotation=45, fontsize=12, ha='right')  # Increase font size and rotate x-axis labels, align them to the right

# Add grid lines to the plot
plt.grid(axis='y', linestyle='--')  # Add horizontal grid lines with dashed style

# Adjust the layout to make sure everything fits without clipping
plt.tight_layout()

# Display the chart
plt.show()

text = '### Dataset types'
st.write(text)
