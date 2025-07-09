import pandas as pd
import streamlit as st
from collections import defaultdict

# Load schedule
df = pd.read_excel("rotations.xlsx")

# Column layout: Time, Red, Green, Yellow, ...
group_names = df.columns[1:]
all_locations = [
    "AR", "SNACK", "ART", "GYM",
    "PLAYGROUND", "GAMEROOM", "STEM", "LIBRARY"
]

# Build location schedule with "next location" info
location_schedule = defaultdict(list)

for i in range(len(df)):
    row = df.iloc[i]
    time = row["Time"]
    next_row = df.iloc[i + 1] if i + 1 < len(df) else None

    used_locations = set()

    for group in group_names:
        current_loc = str(row[group]).strip().upper()
        if not current_loc or current_loc == "NAN":
            continue
        
        used_locations.add(current_loc)

        # Determine "next" location for this group
        if next_row is not None:
            next_loc = str(next_row[group]).strip().upper()
        else:
            next_loc = "End"

        # Append entry: (time, group, next location)
        location_schedule[current_loc].append((time, group, next_loc))

    # Fill "Free" if no group used the location
    for location in all_locations:
        if location not in used_locations:
            location_schedule[location].append((time, "Free", "-"))

# === Streamlit Interface ===
st.title("📍 Staff Location Schedule Viewer")
selected_location = st.selectbox("Select a location", all_locations)

schedule_df = pd.DataFrame(
    location_schedule[selected_location],
    columns=["Time", "Group", "Next Location"]
)

st.table(schedule_df)