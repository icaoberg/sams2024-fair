import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from pprint import pprint
from datetime import datetime

logo_url = 'https://hubmapconsortium.org/wp-content/uploads/2019/01/HuBMAP-Logo-Color.png'
st.image(logo_url)

title = '# FAIR Assessment of HuBMAP data'
st.write(title)

authors = 'Bailey, T.; Chen, J.; Esmaeeli, A.; Hernandez, Y.; Ho, M.; Lampejo, M.; Ma, J.; Martinez, G.; Rubio Martinez, V.; Forchap, E.; Mathurin, S.; Omar, Y.; Segil, J.; McLeod, A.; Cao-Berg, I.'
st.write(authors)

today = 'August 2, 2024'
st.write(today)

abstract = ''' 
# Abstract 
The Human BioMolecular Atlas Program (HuBMAP) aims to create a comprehensive 3D-map representation of the human body and improve data access while developing methods for tissue interrogation applicable to other studies. In its first phase, HuBMAP achieved significant milestones, including the development of critical resources, standardized protocols, innovative imaging and sequencing techniques, and a reliable data integration platform. These efforts have led to the creation of high-resolution molecular and cellular maps that are essential resources for biomedical research. Researchers are expanding the map from 2D to 3D environments, incorporating niche factors such as age and ethnicity. The core value of HuBMAP is to provide freely accessible data via its online portal. Future directions include investigating changes in individual cells and neighborhoods during healthy aging and diseases that will help develop better drugs, predict disease outcomes, and understand disease progression in clinical settings. The program adheres to the FAIR guiding principles for scientific data management and stewardship, ensuring findability, accessibility, interoperability, and reusability of data. We researched these properties of HuBMAP, along with whether it has rich metadata, identifiable titles, standardized communication protocols, and open access to metadata even if the data itself is no longer available.
'''
st.write(abstract)

intro = '''
# Introduction
This is some text
'''
st.write(intro)

method = '''
## Methods
'''
st.write(method)

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

number_of_datasets = len(df.index)
text = f'There are {number_of_datasets} published datasets'
st.write(text)

number_of_organs = len(df.index)
text = f'There are {number_of_organs} organs datasets'
st.write(text)

columns = [
       'organ', 'dataset_type', 'group_name', 'data_access_level']
df2= df[columns]
df2.rename(columns={"organ": "Organ", "dataset_type": "Dataset Type", "data_access_level": "Data Access Level", "group_name": "Group Name"}, inplace=True)
st.write(df2)


text = '### Datasets'
st.write(text)

text = '### Data access level'
st.write(text)

# Count how many times each boolean appears in the data
data_counts = df['has_donor_metadata'].value_counts()

# Plot pie chart using Streamlit
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(data_counts,
                                  autopct='%1.1f%%',
                                  startangle=90)
centre_circle = plt.Circle(
    (0,0),  
    0.70,  
    fc='white'  
)
fig.gca().add_artist(centre_circle)

ax.axis('equal')
plt.title('Percentage of Datasets with Donor Metadata')
st.pyplot(fig)

text = '### Dataset types'

# Count the occurrences of each data access level in the dataframe
access_level_counts = df['group_name'].value_counts()

# Increase figure size for better readability
plt.figure(figsize=(10, 6))  # Adjust width and height as necessary

# Counting the number of datasets with contributors
data_counts = df['has_contributors'].value_counts()
colors=["#3d5a6c","#a4c4d7"]
colors = ["#5b6255","#cadF9E"]

fig, ax = plt.subplots(figsize=(3,3))
wedges, texts, autotexts = ax.pie(data_counts,autopct='%1.1f%%',startangle=90, colors=colors, shadow= True)

autotexts[0].set_color('white') 
autotexts[1].set_color('black') 

ax.legend(wedges, data_counts.index, title="Contributors", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

ax.axis('equal')  
ax.set_title('Distribution of "has contributors"')
st.pyplot(fig)

# Counting the number of datasets with contacts
data_counts = df['has_contacts'].value_counts()
colors = ["#5b6255","#cadF9E"]
colors=["#3d5a6c","#a4c4d7"]

fig, ax = plt.subplots(figsize=(3,3))
wedges, texts, autotexts = ax.pie(data_counts, autopct='%1.1f%%', startangle=90, colors=colors, shadow= True)

autotexts[0].set_color('white') 
autotexts[1].set_color('black') 

ax.legend(wedges, data_counts.index, title="Contacts", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
ax.axis('equal')  
ax.set_title('Distribution of "has contacts"')
st.pyplot(fig)


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
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()


# Count the occurrences of each data access level in the dataframe
access_counts = df['data_access_level'].value_counts()

# Generate a list of colors - one for each bar
colors = ['skyblue', 'coral', 'lightgreen']  

# Start making a bar chart to visualize the data
access_counts.plot(kind='bar', color=colors) 

# Add a title to the top of the chart
plt.title('Data Access Level Distribution')

# Label the x-axis (horizontal axis)
plt.xlabel('Data Access Level')

# Label the y-axis (vertical axis)
plt.ylabel('Count')

# Rotate the labels on the x-axis to 45 degrees
plt.xticks(rotation=45)

# Adjust the layout to make sure everything fits without clipping
plt.tight_layout()

# Display the chart
plt.show()
st.pyplot()


references = '''
# References
* Bueckle, A., Qing, C., Luley, S., Kumar, Y., Pandey, N., & Borner, K. (2023, April 10). The HRA Organ Gallery affords immersive superpowers for building and exploring the Human Reference Atlas with virtual reality. Frontiers, 3. https://www.frontiersin.org/journals/bioinformatics/articles/10.3389/fbinf.2023.1162723/full"
* García, L. J., Batut, B., Burke, M. L., Kuzak, M., Psomopoulos, F. E., Arcila, R., Attwood, T. K., Beard, N., Carvalho-Silva, D., Dimopoulos, A. C., Del Angel, V. D., Dumontier, M., Gurwitz, K. T., Krause, R., McQuilton, P., Pera, L. L., Morgan, S. L., Rauste, P., Via, A., . . . Palagi, P. M. (2020). Ten simple rules for making training materials FAIR. PLOS Computational Biology/PLoS Computational Biology, 16(5), e1007854. https://doi.org/10.1371/journal.pcbi.1007854
* HuBMAP Consortium. The human body at cellular resolution: the NIH Human Biomolecular Atlas Program. Nature 574, 187–192 (2019). https://doi.org/10.1038/s41586-019-1629-x
* Jain, S., Pei, L., Spraggins, J.M. et al. Advances and prospects for the Human BioMolecular Atlas Program (HuBMAP). Nat Cell Biol 25, 1089–1100 (2023). https://doi.org/10.1038/s41556-023-01194-w
* Wilkinson, M. D., Sansone, S. A., Schultes, E., Doorn, P., Bonino da Silva Santos, L. O., & Dumontier, M. (2018). A design framework and exemplar metrics for FAIRness. Scientific data, 5, 180118. https://doi.org/10.1038/sdata.2018.118
'''
st.write(references)

acknowledgements = '''
# Acknowledgements
'''
st.write(acknowledgements)

Conclusion = '''
# Conclusion
'''
st.write(Conclusion)
