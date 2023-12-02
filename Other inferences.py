#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Distribution of Publication Years for Top 100 Cited Papers (Based on degree)
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data-20k.csv', skiprows=[181], nrows=19900) 

# Sort by the 'citations' column in descending order (Degree)
df_sorted = df.sort_values(by='citations', ascending=False)

# Select the top 100 cited papers
top_100 = df_sorted.head(100)

# Plot the distribution of publication years for the top 100 papers
plt.figure(figsize=(10, 6))
plt.hist(top_100['year'], bins=20, color='red', edgecolor='black')
plt.title('Distribution of Publication Years for Top 100 Cited Papers (Based on degree)')
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.grid(axis='y', alpha=0.75)
plt.show()


# In[1]:


#Top 20 Authors with Most Papers
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('data-20k.csv') 

# Split authors 
authors_df = df['authors'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).reset_index(name='author')

# Count occurrences
top_authors = authors_df['author'].value_counts().head(20)
# Display the top authors as a table
print("Top 20 Authors with Most Papers:")
print(top_authors)

