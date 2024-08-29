import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


# Loading image for the app // load png into your project folder
st.image("title for app.png")

# Title for the app
st.title('Exploring the effects of demographics and social attributes on math scores among portuguese high schoolers')

# Load the data // load the data into your project too so we have same name
df = pd.read_csv('student_math_clean.csv')

# ############# 1st graph --> Distribution selection #############

import pandas as pd
import streamlit as st
import plotly.express as px

st.subheader('Final Grade Distribution based on a social or demographic variable:')

# Load the data
df = pd.read_csv('student_math_clean.csv')

# Define the lists of social and demographic attributes
social_attributes = [
    'parent_status', 'mother_education', 'father_education', 'mother_job',
    'father_job', 'school_choice_reason', 'guardian', 'school_support',
    'family_support', 'extra_paid_classes', 'activities', 'nursery_school',
    'higher_ed', 'internet_access', 'romantic_relationship', 'family_relationship',
    'free_time', 'social', 'weekday_alcohol', 'weekend_alcohol', 'health'
]

demographic_attributes = [
    'school', 'sex', 'age', 'address_type', 'family_size',
    'travel_time', 'study_time', 'class_failures', 'absences'
]

# Define bins and labels for final grade categories
bins = [0, 5, 10, 15, 20]
labels = ['Poor (0-5)', 'Average (6-10)', 'Good (11-15)', 'Excellent (16-20)']

# Create a new column with categorical labels for final grade
df['final_grade_category'] = pd.cut(df['final_grade'], bins=bins, labels=labels, include_lowest=True)

# Step 1: Select between Social and Demographic attributes
attribute_group = st.radio(
    "Select an attribute group (social or demographic)",
    ('Social', 'Demographic')
)

# Step 2: Allow user to select multiple symptoms based on the chosen group
if attribute_group == 'Social':
    available_attributes = social_attributes
else:
    available_attributes = demographic_attributes

selected_symptom = st.selectbox('Select Symptom', available_attributes)

# Filter the data based on selected symptoms
filtered_data = df[['final_grade_category', selected_symptom]]

# Group by selected symptoms and final grade category, then count occurrences
grouped_data = filtered_data.groupby([selected_symptom, 'final_grade_category']).size().reset_index(name='count')

# Create a grouped bar plot
fig = px.bar(grouped_data, x=selected_symptom, y='count', color='final_grade_category',
             title=f'Distribution of Final Grade Categories by {selected_symptom}', barmode='group')


# Update layout for better visualization
fig.update_layout(xaxis_title=selected_symptom, yaxis_title="Count")

# Display the plot
st.plotly_chart(fig)

# ############# 2nd graph --> Heatmap #############

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load the data
df = pd.read_csv('student_math_clean.csv')

# Define the lists of social and demographic attributes
social_attributes = [
    'parent_status', 'mother_education', 'father_education', 'mother_job',
    'father_job', 'school_choice_reason', 'guardian', 'school_support',
    'family_support', 'extra_paid_classes', 'activities', 'nursery_school',
    'higher_ed', 'internet_access', 'romantic_relationship', 'family_relationship',
    'free_time', 'social', 'weekday_alcohol', 'weekend_alcohol', 'health'
]

demographic_attributes = [
    'school', 'sex', 'age', 'address_type', 'family_size',
    'travel_time', 'study_time', 'class_failures', 'absences'
]

# Define bins and labels for final grade categories
bins = [0, 5, 10, 15, 20]
labels = ['Poor (0-5)', 'Average (6-10)', 'Good (11-15)', 'Excellent (16-20)']

# Create a new column with categorical labels for final grade
df['final_grade_category'] = pd.cut(df['final_grade'], bins=bins, labels=labels, include_lowest=True)

# Step 1: Overview Heatmap
st.subheader("Correlation Heatmap")

# Overview options
overview_option = st.radio(
    "Select Feature Set",
    ('Whole set of features', 'Only Social', 'Only Demographic')
)

# Determine the set of features to display
if overview_option == 'Whole set of features':
    selected_features = [col for col in df.columns if col not in ['student_id', 'grade_1', 'grade_2']]
elif overview_option == 'Only Social':
    selected_features = [feature for feature in social_attributes if feature in df.columns]
elif overview_option == 'Only Demographic':
    selected_features = [feature for feature in demographic_attributes if feature in df.columns]

# Add final_grade for correlation matrix
if 'final_grade' in df.columns:
    selected_features.append('final_grade')
else:
    st.error("The 'final_grade' column is missing from the dataset.")

# Ensure selected_features only contains numeric columns
numeric_features = df[selected_features].select_dtypes(include=[float, int]).columns.tolist()

if numeric_features:
    # Calculate the correlation matrix
    corr_matrix = df[numeric_features].corr()

    # Plot the heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title(f"Correlation Heatmap - {overview_option}")
    st.pyplot(plt)
else:
    st.error("No numeric features found for correlation calculation.")


# # ###################### interactive graph ----> Works well / Needs a better design
# # Add - Needs to be able to tell whos accountable for the % result. maybe not in Pie Chart?
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv('student_math_clean.csv')

# Define bins and labels for final grade categories
bins = [0, 5, 10, 15, 20]
labels = ['Poor (0-5)', 'Average (6-10)', 'Good (11-15)', 'Excellent (16-20)']

# Create a new column with categorical labels for final grade
df['final_grade_category'] = pd.cut(df['final_grade'], bins=bins, labels=labels, include_lowest=True)


# Interactive plot: Distribution of final grade categories based on selected symptoms
st.subheader('Distribution of Final Grade Categories Based on multiple Selected Symptoms')

# Allow user to select multiple symptoms
selected_symptoms = st.multiselect('Select Symptoms', df.columns[:-3], default=['age'])

# Filter the data based on selected symptoms
filtered_data = df[['final_grade_category'] + selected_symptoms]

# Group by final grade category and count occurrences
grouped_data = filtered_data.groupby(selected_symptoms + ['final_grade_category']).size().reset_index(name='count')

# Calculate percentages for the pie chart
grouped_data['percentage'] = grouped_data.groupby(selected_symptoms)['count'].transform(lambda x: x / x.sum() * 100)

# Create a pie chart
fig = px.pie(grouped_data, values='percentage', names='final_grade_category',
             title='Distribution of Final Grade Categories')

# Display the plot
st.plotly_chart(fig)


# ########################### 2nd graph ----> BoxPlot of final grade distribution by an attribute
# Good for categorical features. Can make it side by side with the non discrete features
# st.subheader('Final Grade Distribution by Categorical Variables')
#
# # Allow the user to select a categorical variable
# selected_categorical = st.selectbox('Select Categorical Variable',
#                                     ['sex', 'school', 'address_type', 'family_size', 'parent_status',
#                                      'mother_education', 'father_education'])
#
# # Create a box plot
# fig = px.box(df, x=selected_categorical, y='final_grade',
#              title=f'Final Grade Distribution by {selected_categorical}',
#              labels={selected_categorical: selected_categorical.capitalize(), 'final_grade': 'Final Grade'})
#
# # Display the plot
# st.plotly_chart(fig)


# ################################### 4th graph ----> Should be for non-discrete features only (like age). gender is no good
# error on graph presentation doesnt show real ranges
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load your dataset
df = pd.read_csv('student_math_clean.csv')

# Calculate overall average grades
overall_avg_grade = df['final_grade'].mean()

# Streamlit App Title and Description
st.title('Interactive Trend Analysis of Final Grades')
st.write("Explore how final grades vary with different attributes.")

# Add here -----> need data conversion for features like family size (turn into numerical),
# can turn travel time into random between ranges also study time
# Define available attributes (only those that are meaningful for visualization)
available_attributes = ['age', 'class_failures', 'family_relationship',
                        'free_time', 'social', 'weekday_alcohol', 'weekend_alcohol', 'health', 'absences']

# Sidebar for user selection (changed to st.selectbox for single select)
selected_attribute = st.selectbox('Choose Attribute', available_attributes, index=0)


# If no attribute selected, default to the first attribute
if not selected_attribute:
    selected_attribute = available_attributes[0]

# Group by selected attribute and calculate average final grade
grouped_data = df.groupby(selected_attribute)['final_grade'].mean().reset_index()

# Create a figure with Plotly graph objects
fig = go.Figure()

# Add trace for the selected attribute
fig.add_trace(go.Scatter(x=grouped_data[selected_attribute], y=grouped_data['final_grade'],
                         mode='lines+markers', name=f'{selected_attribute}'))

# Add overall average line
fig.add_hline(y=overall_avg_grade, line_dash="dash", line_color="red",
              annotation_text=f'Overall Average: {overall_avg_grade:.2f}')

# Update figure layout
fig.update_layout(title='Average Final Grades Comparison',
                  xaxis_title='Attribute Value',
                  yaxis_title='Average Final Grade')

# Display Plotly figure
st.plotly_chart(fig)


# # ################## 7th graph -------------> Good idea - like 4th graph but more interactive comparission
# # Idea - can normalize final scores: if many learn 2-5 but not many >10 it should be put into perspective
# import streamlit as st
# import pandas as pd
# import plotly.express as px
#
# # Load your dataset
# df = pd.read_csv('student_math_clean.csv')
#
# # Streamlit App Title and Description
# st.title('Comparison of Final Grades by Attribute')
#
# # Remove 'student_id' from the list of available attributes
# available_attributes = [col for col in df.columns[:-3] if col != 'student_id']
#
# # Bar for user selection
# selected_attribute = st.selectbox('Choose Attribute', available_attributes)
#
# # If no attribute selected, default to 'gender'
# if not selected_attribute:
#     selected_attribute = 'gender'
#
# # Group by selected attribute and calculate average final grade for each class
# grouped_data = df.groupby([selected_attribute, 'final_grade']).size().reset_index(name='count')
#
# # Plotly figure for comparison
# fig = px.line(grouped_data, x='final_grade', y='count', color=selected_attribute,
#               title=f'Comparison of Final Grades by {selected_attribute}',
#               labels={'final_grade': 'Final Grade', 'count': 'Count', selected_attribute: selected_attribute})
#
# # Update figure layout
# fig.update_layout(xaxis_title='Final Grade', yaxis_title='Count')
#
# # Display Plotly figure
# st.plotly_chart(fig)
