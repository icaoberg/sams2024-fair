import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


## DO NOT MODIFY THIS BLOCK
# Function to determine the type
def determine_type(dataset_type: str) -> str:
    if "[" in dataset_type and "]" in dataset_type:
        return "Derived"
    else:
        return "Primary"


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
        if "data" in json_data:  # Check if the JSON contains the key 'data'
            df = pd.DataFrame(
                json_data["data"]
            )  # Create a DataFrame using the data under 'data' key
            df = df[df["status"] == "Published"]
            df["dataset_status"] = df["dataset_type"].apply(determine_type)
            print("Data successfully loaded.")  # Print a message indicating success
        else:
            raise KeyError(
                "'data' key not found in the JSON response"
            )  # Raise an error if 'data' key is missing

        return df  # Return the DataFrame with the data
    except (ValueError, KeyError) as e:  # Catch errors related to value or missing keys
        print(f"Error loading data: {e}")  # Print the error message
        return pd.DataFrame()  # Return an empty DataFrame if there is an error
    except requests.RequestException as e:  # Catch errors related to the request itself
        print(f"Request failed: {e}")  # Print the error message
        return pd.DataFrame()  # Return an empty DataFrame if the request fails


# Unpublished dataframe
@st.cache_data
def get_unpublished_data() -> pd.DataFrame:
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
        if "data" in json_data:  # Check if the JSON contains the key 'data'
            df = pd.DataFrame(
                json_data["data"]
            )  # Create a DataFrame using the data under 'data' key
            df = df[df["status"] != "Published"]
            df["dataset_status"] = df["dataset_type"].apply(determine_type)
            print("Data successfully loaded.")  # Print a message indicating success
        else:
            raise KeyError(
                "'data' key not found in the JSON response"
            )  # Raise an error if 'data' key is missing

        return df  # Return the DataFrame with the data
    except (ValueError, KeyError) as e:  # Catch errors related to value or missing keys
        print(f"Error loading data: {e}")  # Print the error message
        return pd.DataFrame()  # Return an empty DataFrame if there is an error
    except requests.RequestException as e:  # Catch errors related to the request itself
        print(f"Request failed: {e}")  # Print the error message
        return pd.DataFrame()  # Return an empty DataFrame if the request fails


df = get_data()
df2 = get_unpublished_data()
## DO NOT MODIFY THIS BLOCK

# Convert the dictionary into a DataFrame


## DO NOT MODIFY THIS BLOCK

logo_url = "https://hubmapconsortium.org/wp-content/uploads/2019/01/HuBMAP-Retina-Logo-Color-300x110.png"
st.image(logo_url)
# Display the logo with column width fitting

title = "# FAIR Assessment of HuBMAP data"
st.write(title)

authors = "Bailey, T.; Chen, J.; Esmaeeli, A.; Hernandez, Y.; Ho, M.; Lampejo, M.; Ma, J.; Martinez, G.; Rubio Martinez, V.; Forchap, E.; Mathurin, S.; Omar, Y.; Segil, J.; McLeod, A.; Cao-Berg, I."
st.write(authors)

today = pd.Timestamp.today().strftime("%m-%d-%Y")
st.write(today)

abstract = """
The Human BioMolecular Atlas Program (HuBMAP) aims to create a comprehensive 3D-map representation of the human body and improve data access while developing methods for tissue interrogation applicable to other studies. In its first phase, HuBMAP achieved significant milestones, including the development of critical resources, standardized protocols, innovative imaging and sequencing techniques, and a reliable data integration platform. These efforts have led to the creation of high-resolution molecular and cellular maps that are essential resources for biomedical research. Researchers are expanding the map from 2D to 3D environments, incorporating niche factors such as age and ethnicity. The core value of HuBMAP is to provide freely accessible data via its online portal. Future directions include investigating changes in individual cells and neighborhoods during healthy aging and diseases that will help develop better drugs, predict disease outcomes, and understand disease progression in clinical settings. The program adheres to the FAIR guiding principles for scientific data management and stewardship, ensuring findability, accessibility, interoperability, and reusability of data. We researched these properties of HuBMAP, along with whether it has rich metadata, identifiable titles, standardized communication protocols, and open access to metadata even if the data itself is no longer available.
"""
# Anchor point
st.title("Abstract")
st.sidebar.markdown("[Abstract](#abstract)", unsafe_allow_html=True)
st.write(abstract)

about_us = """
# About Us
"""
st.write(about_us)
import plotly.graph_objects as go

state_abbreviations = {
    "Massachusetts": "MA",
    "New York": "NY",
    "Missouri": "MO",
    "Kentucky": "KY",
    "New Jersey": "NJ",
    "Alabama": "AL",
    "California": "CA",
    "Georgia": "GA",
    "Texas": "TX",
    "Illinois": "IL",
    "Pennsylvania": "PA",
}

state_population = {
    "MA": 1,
    "NY": 1,
    "MO": 1,
    "KY": 1,
    "NJ": 1,
    "AL": 1,
    "CA": 3,
    "GA": 1,
    "TX": 2,
    "IL": 1,
    "PA": 1,
}

state_codes = list(state_abbreviations.values())
state_names = list(state_abbreviations.keys())

hovertext = [
    f"{state_names[i]}<br>Population: {state_population[code]:,}"
    for i, code in enumerate(state_codes)
]

data = go.Choropleth(
    locations=state_codes,
    z=[state_population[code] for code in state_codes],
    locationmode="USA-states",
    colorscale="Reds",
    hoverinfo="location+text",
    hovertext=hovertext,
    marker_line_color="black",
    colorbar=dict(title="Population", tickvals=[1, 2, 3], ticktext=["1", "2", "3"]),
)

layout = go.Layout(
    geo=dict(
        scope="usa",
        projection=dict(type="albers usa"),
        showlakes=False,
        showland=True,
        landcolor="rgb(217, 217, 217)",
    )
)

fig = go.Figure(data=[data], layout=layout)
st.plotly_chart(fig)

intro = """
The Human BioMolecular Atlas Program (HuBMAP) is an initiative that aims to create a comprehensive multi-scale spatial atlas of the healthy human body. HuBMAP aims to help biomedical researchers visualize how the cells in the human body influence our health and can also help others understand the way in which the human body functions. HuBMAP can only finalize its atlas with the help of data providers, data curators and other contributors. 

Data providers are crucial to HuBMAP, these providers are responsible for producing biological data from various tissues of donors. These tissues are utilized by different types of cutting-edge technologies such as, single cell transcriptomics, bulk tissue arrays, etc. These providers generate high-quality datasets that help form a structure for HuBMAP.

Additionally, HIVE — the HuBMAP Integration, Visualization, and Engagement team holds the responsibility of curating, integrating, and standardizing the vast amount of datasets. HIVE ensures that the datasets meet quality standards before they become publicly available. HIVE also helps develop analytical tools for scientific researchers to understand and utilize the datasets.

With all the data provided and curated, contributors then develop innovative tools that enhance data analysis and help transform the data into the atlas. Contributions come from 42 different sites, 14 states, and 4 countries. With these contributions, HuBMAP is able to advance its technological and scientific capabilities.

Through the seamless integration of work from data providers, contributors, and HIVE, HuBMAP strives to create a high-tech transformational atlas that fosters inventions of new discoveries in the field of biomedical research.
"""
st.title("Introduction")
st.sidebar.markdown("[Introduction](#introduction)", unsafe_allow_html=True)
st.write(intro)


introImg_url = "https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41586-019-1629-x/MediaObjects/41586_2019_1629_Fig1_HTML.png?as=webp"
st.image(introImg_url, use_column_width=True)

introImgCaption = """
The TMCs will collect tissue samples and generate spatially resolved, single-cell data. Groups involved in TTD and RTI initiatives will develop emerging and more developed technologies, respectively; in later years, these will be implemented at scale. Data from all groups will be rendered useable for the biomedical community by the HuBMAP integration, visualization and engagement (HIVE) teams. The groups will collaborate closely to iteratively refine the atlas as it is gradually realized. (HuBMAP Consortium)
"""
st.write(introImgCaption)

# Method = """

method = """

# Overview
The Human Biomolecular Atlas Program(HuBMAP) funded by the National Institute of Health(NIH), provides spatial molecular data which serves as a way to completely map out the human body to promote intuitive and revolutionary research. However, in order for the research to be comprehensive and understandable by professionals and the public alike, it needs to be Findable, Accessible, Interoperable, and Reusable. The FAIR guidelines provide a path for the HuBMAP data to lessen unavoidable bias, and corrupt data. The purpose of the project by the Carnegie Mellon Summer Academy for Math and Science team, serves as a means to analyze some of the HuBMAP data, and report back on the level to which the data adheres to the first two FAIR principles(Findable and Accessible). 
"""

st.sidebar.markdown("[Overview](#overview)", unsafe_allow_html=True)
st.write(method)

st.header("Published Data")
st.sidebar.markdown("[Published Data](#published-data)", unsafe_allow_html=True)

text = "### At a Glance"
st.write(text)


# At a glance sentences
# wordcloud
fig, ax = plt.subplots()
wordcloud = WordCloud(
    width=800, height=400, background_color="white"
).generate_from_frequencies(df["group_name"].value_counts())

fig, ax = plt.subplots(figsize=(10, 5))  # Set the figure size
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")  # Hide the axis

st.pyplot(fig)
# wordcloud
number_of_datasets = len(df)
access_level_protected = df["data_access_level"].value_counts()["protected"]
access_level_public = df["data_access_level"].value_counts()["public"]
dataset_status_derived = df["dataset_status"].value_counts()["Derived"]
dataset_status_primary = df["dataset_status"].value_counts()["Primary"]

dataset_types = df["dataset_type"].unique()
number_of_dataset_types = len(dataset_types)
organs = df["organ"].unique()
number_of_organs = len(organs)

donors = df["donor_hubmap_id"].unique()
number_of_donors = len(donors)

groups = df["group_name"].unique()
number_of_groups = len(groups)

answer = f"""
* The number of datasets are **{number_of_datasets}**.
    * The number of  datasets that are protected is **{access_level_protected}**.
    * The number of datasets that are public is **{access_level_public}**.
* The number of dataset types are **{number_of_dataset_types}**.
    * The number of datasets with a derived status is **{dataset_status_derived}**.
    * The number of datasets with a primary status is **{dataset_status_primary}**.
* The number of organ types are **{number_of_organs}**.
* The number of donors for the datasets are **{number_of_donors}**.
* The number of groups for the datasets are **{number_of_groups}**."""

st.write(answer)

# At a a glance sentences (closed)

text = "## Observability"
st.write(text)

text = "### Datasets"
st.write(text)

columns = [
    "organ",
    "dataset_type",
    "group_name",
    "created_timestamp",
    "data_access_level",
]
df_display = df[columns]
df_display["created_timestamp"] = df_display["created_timestamp"].apply(
    lambda time: pd.to_datetime(time, unit="ms").strftime("%m-%d-%Y")
)
df_display["data_access_level"] = df_display["data_access_level"].str.capitalize()
df_display.rename(
    columns={
        "organ": "Organ",
        "dataset_type": "Dataset Type",
        "created_timestamp": "Date Added",
        "group_name": "Group Name",
        "data_access_level": "Data Access Level",
    },
    inplace=True,
)
st.write(df_display)

# Title for Graphs
st.header("Graphs")
st.sidebar.markdown("[Graphs](#graphs)", unsafe_allow_html=True)

# Creating columns for graphs

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

# Count how many times each unique value appears in the 'data_access_level' column
access_level_counts = df["has_data"].value_counts()


# Start making a donut chart

plt.clf()
fig, ax = plt.subplots(
    figsize=(5, 5)
)  # Create a blank space (figure) where the chart will be drawn
colors = ["#cadF9E"]
# Plot a pie chart that will later become a donut chart
wedges, texts, autotexts = ax.pie(
    access_level_counts,  # This is the data we're using — the counts of each access level
    autopct="%1.1f%%",  # This makes sure that each piece of the pie shows its percentage like "25.0%"
    startangle=90,  # This starts the first piece of the pie at the top of the circle
    wedgeprops=dict(
        width=0.3
    ),  # This makes the pie chart have a hole in the middle, turning it into a donut chart
    colors=colors,
)

# Draw a white circle in the middle to make it look like a donut instead of a pie
centre_circle = plt.Circle(
    (0, 0),  # This places the circle in the middle of the chart
    0.70,  # This sets the size of the white circle, making sure it's small enough to see the data around it but big enough to make a 'hole'
    fc="white",  # 'fc' stands for fill color, which we're setting to white here
)
fig.gca().add_artist(centre_circle)  # This adds the white circle to our chart

ax.legend(
    wedges,
    access_level_counts.index,
    title="Contributors",
    loc="center right",
    bbox_to_anchor=(1.2, 0.5),
)


# Make sure the chart is a perfect circle
ax.axis(
    "equal"
)  # This command makes sure the height and width are the same, keeping our donut round

# Add a title to the chart
plt.title("Percentages of Dataset with Data")


# Display the plot in Streamlit
plt.tight_layout()
with col1:
    st.pyplot(fig)

text = "### Datasets"
st.write(text)

text = "### Data access level"
st.write(text)

# Count how many times each boolean appears in the data
data_counts = df["has_donor_metadata"].value_counts()

# Plot pie chart using Streamlit
fig, ax = plt.subplots(figsize=(3, 3))
wedges, texts, autotexts = ax.pie(
    data_counts, autopct="%1.1f%%", startangle=90, colors=["#cadF9E"]
)
centre_circle = plt.Circle((0, 0), 0.70, fc="white")
fig.gca().add_artist(centre_circle)

ax.legend(wedges, data_counts.index, title="Has Metadata", loc="center")
ax.axis("equal")
plt.title("Percentage of Datasets with Donor Metadata")

# Display the plot in Streamlit
plt.tight_layout()
with col2:
    st.pyplot(fig)


# Count the occurrences of each data access level in the dataframe
access_level_counts = df["group_name"].value_counts()


# Increase figure size for better readability

plt.clf()
plt.figure(figsize=(10, 6))  # Adjust width and height as necessary

# Counting the number of datasets with contributors
data_counts = df["has_contributors"].value_counts()
colors = ["#3d5a6c", "#a4c4d7"]
colors = ["#5b6255", "#cadF9E"]

fig, ax = plt.subplots(figsize=(3, 3))
wedges, texts, autotexts = ax.pie(
    data_counts, autopct="%1.1f%%", startangle=90, colors=colors, shadow=True
)

autotexts[0].set_color("white")
autotexts[1].set_color("black")

ax.legend(
    wedges,
    data_counts.index,
    title="Contributors",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)


ax.axis("equal")
ax.set_title('Distribution of "has contributors"')

# Display the plot in Streamlit
plt.tight_layout()
with col3:
    st.pyplot(fig)

# Counting the number of datasets with contacts
data_counts = df["has_contacts"].value_counts()

plt.clf()


colors = ["#5b6255", "#cadF9E"]
colors = ["#3d5a6c", "#a4c4d7"]


fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    data_counts, autopct="%1.1f%%", startangle=90, colors=colors, shadow=True
)

autotexts[0].set_color("white")
autotexts[1].set_color("black")

ax.legend(
    wedges,
    data_counts.index,
    title="Contacts",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

ax.axis("equal")
ax.set_title('Distribution of "has contacts"')

# Display the plot in Streamlit
plt.tight_layout()
with col4:
    st.pyplot(fig)


# Counting the number of datasets with contributors
data_counts = df["data_access_level"].value_counts()
colors = ["#5b6255", "#cadF9E"]

fig, ax = plt.subplots(figsize=(3, 3))
wedges, texts, autotexts = ax.pie(
    data_counts, autopct="%1.1f%%", startangle=90, colors=colors, shadow=True
)

autotexts[0].set_color("white")
autotexts[1].set_color("black")

ax.legend(
    wedges,
    [s.capitalize() for s in data_counts.index],
    title="Access Level",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

ax.axis("equal")
ax.set_title("Data Access Level Distribution")

# Display the plot in Streamlit
plt.tight_layout()
with col5:
    st.pyplot(fig)

# Count the occurrences of each data access level in the dataframe
access_level_counts = df["group_name"].value_counts()


# Increase figure size for better readability

plt.clf()
plt.figure(figsize=(10, 6))  # Adjust width and height as necessary

# Start making a bar chart to visualize the data
# This will create a bar chart where each bar represents a different data access level
access_level_counts.plot(
    kind="bar", color="skyblue", width=0.8
)  # 'width' adjusts the width of the bars

# Add a title to the top of the chart
plt.title("Research group name", fontsize=16)  # Increase font size for the title

# Label the x-axis (horizontal axis)
plt.xlabel(
    "University", fontsize=14, labelpad=15
)  # Increase font size for the x-axis label and add padding

# Label the y-axis (vertical axis)
plt.ylabel("Count", fontsize=14)  # Increase font size for the y-axis label

# Rotate the labels on the x-axis to 45 degrees for better readability
plt.xticks(
    rotation=45, fontsize=12, ha="right"
)  # Increase font size and rotate x-axis labels, align them to the right

# Add grid lines to the plot
plt.grid(axis="y", linestyle="--")  # Add horizontal grid lines with dashed style

# Adjust the layout to make sure everything fits without clipping
plt.tight_layout()


# Display the chart
with col6:
    st.pyplot(fig)


# Count the occurrences of each data access level in the dataframe

plt.clf()
access_counts = df["data_access_level"].value_counts()
plt.figure(figsize=(10, 6))

# Generate a list of colors - one for each bar
colors = ["skyblue", "coral", "lightgreen"]

# Start making a bar chart to visualize the data
access_counts.plot(kind="bar", color=colors)

# Add a title to the top of the chart

plt.title("Data Access Level Distribution")

# Label the x-axis (horizontal axis)
plt.xlabel("Data Access Level")

# Label the y-axis (vertical axis)
plt.ylabel("Count")

# Rotate the labels on the x-axis to 45 degrees
plt.xticks(rotation=45)

# Adjust the layout to make sure everything fits without clipping
plt.tight_layout()

# Display the chart
with col7:
    st.pyplot(fig)
text = "To enlarge graph, click on desired"


# unpublished data
st.header("Unpublished Data")
st.sidebar.markdown("[Unpublished Data](#unpublished-data)", unsafe_allow_html=True)

st.subheader("At A Glance")


def at_a_glance():
    number_of_datasets = len(df2)
    access_level_protected = df2["data_access_level"].value_counts()["protected"]
    dataset_status_derived = df2["dataset_status"].value_counts()["Derived"]
    dataset_status_primary = df2["dataset_status"].value_counts()["Primary"]

    dataset_types = df2["dataset_type"].unique()
    number_of_dataset_types = len(dataset_types)
    organs = df2["organ"].unique()
    number_of_organs = len(organs)

    donors = df2["donor_hubmap_id"].unique()
    number_of_donors = len(donors)

    groups = df2["group_name"].unique()
    number_of_groups = len(groups)

    answer = f"""
    * The number of unpublished datasets are **{number_of_datasets}**.
        * The number of unpublished datasets that are protected is **{access_level_protected}**.
    * The number of unpublished dataset types are **{number_of_dataset_types}**.
        * The number of unpublished datasets with a derived status is **{dataset_status_derived}**.
        * The number of unpublished datasets with a primary status is **{dataset_status_primary}**.
    * The number of unpublished organ types are **{number_of_organs}**.
    * The number of donors for unpublished datasets are **{number_of_donors}**.
    * The number of groups with unpublished datasets are **{number_of_groups}**."""
    st.write(answer)


columns = [
    "organ",
    "dataset_type",
    "status",
    "created_timestamp",
    "data_access_level",
]
df_display = df2[columns]
df_display["created_timestamp"] = df_display["created_timestamp"].apply(
    lambda time: pd.to_datetime(time, unit="ms").strftime("%m-%d-%Y")
)
df_display["data_access_level"] = df_display["data_access_level"].str.capitalize()
df_display.rename(
    columns={
        "organ": "Organ",
        "dataset_type": "Dataset Type",
        "created_timestamp": "Date Added",
        "status": "Status",
        "data_access_level": "Data Access Level",
    },
    inplace=True,
)
st.write(df_display)


def unpublished_has_contributors():
    # st.subheader("Unpublished Dataset Plots")
    data_counts = df2["has_contributors"].value_counts()
    colors = ["#3d5a6c", "#a4c4d7"]
    colors = ["#cadF9E", "#5b6255"]

    fig, ax = plt.subplots(figsize=(3, 3))
    wedges, texts, autotexts = ax.pie(
        data_counts, autopct="%1.1f%%", startangle=90, colors=colors, shadow=True
    )

    autotexts[0].set_color("black")
    autotexts[1].set_color("white")

    ax.legend(
        wedges,
        data_counts.index,
        title="Contributors",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )
    ax.axis("equal")
    ax.set_title('Distribution of "has contributors" in Unpublished Data')
    st.pyplot(fig)


def unpublished_has_contacts():
    data_counts = df2["has_contacts"].value_counts()
    colors = ["#5b6255", "#cadF9E"]
    colors = ["#a4c4d7", "#3d5a6c"]

    fig, ax = plt.subplots(figsize=(3, 3))
    wedges, texts, autotexts = ax.pie(
        data_counts, autopct="%1.1f%%", startangle=90, colors=colors, shadow=True
    )

    autotexts[0].set_color("black")
    autotexts[1].set_color("white")

    ax.legend(
        wedges,
        data_counts.index,
        title="Contributors",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    ax.axis("equal")
    ax.set_title('Distribution of "has contacts" in Unpublished Data')
    st.pyplot(fig)


def unpublished_data_access_level():
    data_counts = df2["data_access_level"].value_counts()
    colors = ["#5b6255", "#cadF9E"]

    fig, ax = plt.subplots(figsize=(3, 3))
    wedges, texts, autotexts = ax.pie(
        data_counts, autopct="%1.1f%%", startangle=90, colors=colors, shadow=True
    )

    autotexts[0].set_color("white")
    autotexts[1].set_color("black")

    ax.legend(
        wedges,
        [s.capitalize() for s in data_counts.index],
        title="Access Level",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    ax.axis("equal")
    ax.set_title("Data Acess Level Distribution in Unpublished Data")
    # Display the plot in Streamlit
    st.pyplot(fig)


# Creation of side bar (again...)
def main():
    # Sidebar with dropdown menu
    option = st.sidebar.selectbox(
        "Select an option:",
        ["At a Glance", "Contributors Plot", "Contacts Plot", "Data Access Level Plot"],
    )

    # Display content based on selected option
    if option == "At a Glance":
        at_a_glance()
    elif option == "Contributors Plot":
        unpublished_has_contributors()
    elif option == "Contacts Plot":
        unpublished_has_contacts()
    elif option == "Data Access Level Plot":
        unpublished_data_access_level()


if __name__ == "__main__":
    main()


# Introduction paragraph for VR
vrIntro = """
Recent advancements in virtual reality (VR) development have sparked interest in applying VR to biomedical research and practice. VR allows for dynamic exploration and enables viewers to enter visualizations from various viewpoints (Camp et al., 1998). It also facilitates the creation of detailed visualizations of intricate molecular structures and biomolecular systems (Chavent et al., 2011; Gill and West, 2014; Trellet et al., 2018; Wiebrands et al., 2018).
When viewed in VR, the spatiality of organs and tissue blocks mapped to the Human Reference Atlas (HRA) can be explored in their true size, providing a perspective that surpasses traditional 2D user interfaces. Added 2D and 3D visualizations can then offer data-rich context. The HRA Organ Gallery, a VR application, allows users to explore 3D organ models of the HRA in their true scale, location, and spatial relation to each other. Currently, the HRA Organ Gallery features 55 3D reference organs, 1,203 mapped tissue blocks from 292 demographically diverse donors and 15 providers, linking to over 6,000 datasets. It also includes prototype visualizations of cell type distributions and 3D protein structures.
"""
st.title("HuBMAP In VR", anchor="hubmap-in-vr")
st.sidebar.markdown("[HuBMAP In VR](#hubmap-in-vr)", unsafe_allow_html=True)
st.write(vrIntro)

# How to use VR

vrNavigate = """
## Navigating VR
"""
st.write(vrNavigate)

logoVr_url = "https://www.frontiersin.org/files/Articles/1162723/fbinf-03-1162723-HTML/image_m/fbinf-03-1162723-g002.jpg"
st.image(logoVr_url)
figure_caption = """
Functionality of the HRA Organ Gallery (A) Default organ layout (B) A user extrudes all 10 body systems containing 55 organs. (C) A user inspects a kidney and tissue blocks. (D) A user moves through the scene using teleportation, plus other views of the fully extruded gallery view. (E) A user employs the filter menu to show or hide organs. (Bueckle et al., 2023)
"""
st.write(figure_caption)

vrCaption = """
The VR device, while innovative and interesting, 
has several notable drawbacks. Users often experience nausea and dizziness 
after prolonged usage, particularly beyond 30 minutes. Comfort is a 
significant issue, as the device needs to be tightly fitted to the face for 
optimal functionality, which poses problems for individuals who wear glasses. 
Achieving the clearest image can be challenging, requiring time to adjust the lenses, 
which are never completely clear. The home screen, which displays the user's actual surroundings, 
is of poor quality, appearing in black and white and often glitchy. In contrast, the quality within
 games, such as light saber experiences, is excellent, with smooth performance. However, certain applications, 
 like the Organ HR application, have cumbersome navigation, requiring precise pointer movements to view cell types, 
 which disappear when the pointer is moved away. The text on screens can be blurry and difficult to read, and the zoom 
 functionality is hindered by its programming. Additionally, the instruction manual lacks clarity, making setup and use more challenging. 
 Overall, while the VR offers some high-quality experiences, it is marred by comfort issues, visual clarity problems, and suboptimal user instructions.
"""
st.write(vrCaption)

text = "### Dataset types"
st.write(text)

acknowledgements = """
We thank Andreas Bueckle for their assistance in data acquisition and management.  

Research reported in this publication was supported by the National Institute of Health's (NIH) Common Fund under award numbers X, Y, and Z. Additionally, it’s important to include a disclaimer: The content is solely the responsibility of the authors and does not necessarily represent the official views of the NIH.
"""
st.title("Acknowledgements")
st.sidebar.markdown("[Acknowledgements](#acknowledgements)", unsafe_allow_html=True)
st.write(acknowledgements)

conclusion = """
Regarding our first objective, an assessment of the FAIRness of HuBMAP Data, we found that data visualization techniques allowed us to present a live time analysis of HuBMAP data. HuBMAP data includes many features that help ensure the FAIR guideline;. most datasets include rich metadata, identifiable titles, standardized communication protocols. Thus, we conclude that HubMAP data adheres to the first 2 FAIR guidelines of findable and accessible.

When considering our second objective, assessing the FAIRness of the HuBMAP VR application, we came to a different conclusion. HRA Organ VR still needs some work to meet the principles of FAIR, as not all the data is easily accessible and findable. However, the application is still in development and is expected to improve on many of its current shortcomings. Thus, this result is somewhat expected as the current version is not the final product.
"""
st.title("Conclusion")
st.sidebar.markdown("[Conclusion](#conclusion)", unsafe_allow_html=True)

st.write(conclusion)

references = """
* Browne K, Cross LE, Herr, II BW, Record EG, Quardokus EM, Bueckle A, Börner K. 2020. HuBMAP CCF 3D Reference Object Library.
* Bueckle, A., Qing, C., Luley, S., Kumar, Y., Pandey, N., & Borner, K. (2023, April 10). The HRA Organ Gallery affords immersive superpowers for building and exploring the Human Reference Atlas with virtual reality. Frontiers, 3. https://www.frontiersin.org/journals/bioinformatics/articles/10.3389/fbinf.2023.1162723/full
* Camp, J. J., Cameron, B. M., Blezek, D., and Robb, R. A. (1998). Virtual reality in medicine and biology.” Future Generation Computer Systems. Telemedical Inf. Soc. 14 (1), 91–108. https://www.sciencedirect.com/science/article/abs/pii/S0167739X98000235 
* Chavent, M., Antoine, V., Tek, A., Levy, B., Robert, S., Bruno, R., et al. (2011). GPU-accelerated atom and dynamic bond visualization using hyperballs: A unified algorithm for balls, sticks, and hyperboloids. J. Comput. Chem. 32 (13), 2924–2935. https://doi.org/10.1002/jcc.21861  
* García, L. J., Batut, B., Burke, M. L., Kuzak, M., Psomopoulos, F. E., Arcila, R., Attwood, T. K., Beard, N., Carvalho-Silva, D., Dimopoulos, A. C., Del Angel, V. D., Dumontier, M., Gurwitz, K. T., Krause, R., McQuilton, P., Pera, L. L., Morgan, S. L., Rauste, P., Via, A., . . . Palagi, P. M. (2020). Ten simple rules for making training materials FAIR. PLOS Computational Biology/PLoS Computational Biology, 16(5), e1007854. https://doi.org/10.1371/journal.pcbi.1007854
* Gill, B. J., and West, J. L. (2014). Modeling the tumor extracellular matrix: Tissue engineering tools repurposed towards new frontiers in cancer biology. J. Biomechanics, Funct. Tissue Eng. 47 (9), 1969–1978. https://pubmed.ncbi.nlm.nih.gov/24300038/ 
* HuBMAP Consortium. The human body at cellular resolution: the NIH Human Biomolecular Atlas Program. Nature 574, 187–192 (2019). https://doi.org/10.1038/s41586-019-1629-x
* Jain, S., Pei, L., Spraggins, J.M. et al. Advances and prospects for the Human BioMolecular Atlas Program (HuBMAP). Nat Cell Biol 25, 1089–1100 (2023). https://doi.org/10.1038/s41556-023-01194-w
* Snyder, M.P., Lin, S., Posgai, A. et al. The human body at cellular resolution: the NIH Human Biomolecular Atlas Program. Nature 574, 187–192 (2019). https://doi.org/10.1038/s41586-019-1629-x.
* Trellet, M. L., Férey, N., Flotyński, J., Baaden, M., and Bourdot, P. (2018). Semantics for an integrative and immersive pipeline combining visualization and analysis of molecular data. J. Integr. Bioinforma. 15 (2), 20180004. https://doi.org/10.1515/jib-2018-0004 
* Wiebrands, M., Malajczuk, C. J., Woods, A. J., Rohl, A. L., and Mancera, R. L. (2018). Molecular dynamics visualization (MDV): Stereoscopic 3D display of biomolecular structure and interactions using the Unity game engine. J. Integr. Bioinforma. 15 (2), 20180010. https://doi.org/10.1515/jib-2018-0010 
* Wilkinson, M. D., Sansone, S. A., Schultes, E., Doorn, P., Bonino da Silva Santos, L. O., & Dumontier, M. (2018). A design framework and exemplar metrics for FAIRness. Scientific data, 5, 180118. https://doi.org/10.1038/sdata.2018.118
"""
st.title("References")
st.sidebar.markdown("[References](#references)", unsafe_allow_html=True)
st.write(references)
