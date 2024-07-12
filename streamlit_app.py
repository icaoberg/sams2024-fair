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
text = f'There are {number_of_organs} organs'
st.write(text)

text = '### Datasets'
st.write(text)

text = '### Data access level'
st.write(text)



# Counting the number of datasets with contributors
data_counts = df['has_contributors'].value_counts()
olors=["#3d5a6c","#a4c4d7"]
colors = ["#5b6255","#cadF9E"]

fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(data_counts,autopct='%1.1f%%',startangle=90, colors=colors)

for text in texts:
    text.set_color('white') 

ax.legend(wedges, data_counts.index, title="Contributors", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

ax.axis('equal')  
ax.set_title('Distribution of "has_contributors"')
st.pyplot(fig)

# Counting the number of datasets with contacts
data_counts = df['has_contacts'].value_counts()
colors = ["#5b6255","#cadF9E"]

colors=["#3d5a6c","#a4c4d7"]
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(data_counts, autopct='%1.1f%%', startangle=90, colors=colors)
ax.legend(wedges, data_counts.index, title="Contacts", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
ax.axis('equal')  
ax.set_title('Distribution of "has_contacts"')
st.pyplot(fig)


text = '### Dataset types'
st.write(text)

text = '### Dataset types'
st.write(text)
