import pandas as pd
import streamlit as st
from collections import defaultdict

# Load your spreadsheet
df = pd.read_excel("rotations.xlsx")

# List of all groups (column names excluding "Time")
group_names = df.columns[1:]

# ✅ Define all locations manually (based on your setup)
all_locations = [
    "AR", "SNACK", "ART", "GYM",
    "PLAYGROUND", "GAMEROOM", "STEM", "LIBRARY"
]

# Create a dictionary to store the output
location_schedule = defaultdict(list)

# Loop through each time slot
for _, row in df.iterrows():
    time = row["Time"]
    used_locations = set()
    
    # First, collect used locations
    for group in group_names:
        location = row[group]
        if pd.notna(location):  # Skip empty cells
            location_schedule[location].append((time, group))
            used_locations.add(location)
    
    # Then, fill in "Free" for any location not used
    for location in all_locations:
        if location not in used_locations:
            location_schedule[location].append((time, "Free"))

# ✅ Output results
for location, entries in location_schedule.items():
    print(f"\n📍 {location} Schedule:")
    for time, group in entries:
        print(f"{time} → {group}")

# Streamlit UI
st.title("📍 Staff Location Schedule Viewer")
selected_location = st.selectbox("Select a location", all_locations)

# Display location's schedule
schedule_df = pd.DataFrame(location_schedule[selected_location], columns=["Time", "Group"])
st.table(schedule_df)