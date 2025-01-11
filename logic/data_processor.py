import pandas as pd
import random

class DataProcessor():

    def __init__(self) -> None:
        self.df = None  # Initialize df to None
        self.activity_cols = None  # Initialize activity_cols to None

    @classmethod
    def set_data(cls, data):
        cls.df = data
        cls.activity_cols = [col for col in cls.df.columns if col.startswith('Activity')]

    @classmethod
    def assign_to_activity(cls, activity_cols, max_spaces):
        """
        Assigns users to activities based on their preferences and available spaces,
        prioritizing choices in order (1st, 2nd, 3rd, etc.).

        Args:
            df: The DataFrame containing user preferences and activity columns.
            activity_cols: A list of column names representing the activities.
            max_spaces: A dictionary specifying the maximum spaces for each activity.
        Returns:
            A tuple containing two elements:
                - assignments: A DataFrame with columns 'Attendee ID', 'First Name', 'Last Name', 'Email address' and 'Assigned Activity'.
                - unassigned_users: A DataFrame with columns 'Attendee ID', 'First Name', 'Last Name', and 'Email address' for users who could not be assigned.
        """

        # Convert all columns in activity_cols to numeric, replacing all non-numeric values with 'NaN'
        for col in activity_cols:
            cls.df[col] = pd.to_numeric(cls.df[col], errors='coerce')

        assignments = []
        unassigned_users = []
        remaining_spaces = max_spaces.copy()

        # Create a set of assigned user indices
        assigned_users = set()

        # Iterate through choices in order (1st, 2nd, 3rd, etc.)
        for choice_number in range(1, len(activity_cols) + 1):
            for activity in activity_cols:
                if remaining_spaces[activity] > 0:
                    # Consider only unassigned users for the current choice
                    potential_users = cls.df[
                        (cls.df[activity] == choice_number) & 
                        (cls.df['Attendee ID'].isin(assigned_users) == False) & 
                        (cls.df['No Activity'] != 'TRUE')
                    ].index.tolist()
                    random.shuffle(potential_users)

                    for user_index in potential_users:
                        if remaining_spaces[activity] > 0:
                            assignments.append({
                                'Attendee ID': cls.df.loc[user_index, 'Attendee ID'],
                                'First Name': cls.df.loc[user_index, 'Your name | First name'],
                                'Last Name': cls.df.loc[user_index, 'Your name | Last name'],
                                'Email address': cls.df.loc[user_index, 'Your email address | Email address'],
                                'Assigned Activity': activity
                            })
                            remaining_spaces[activity] -= 1
                            assigned_users.add(cls.df.loc[user_index, 'Attendee ID'])
                        else:
                            break  # Move to the next activity if this one is full

        # Identify unassigned users
        for index, row in cls.df.iterrows():
            if row['Attendee ID'] not in assigned_users:
                unassigned_users.append({
                    'Attendee ID': row['Attendee ID'],
                    'First Name': row['Your name | First name'],
                    'Last Name': row['Your name | Last name'],
                    'Email address': row['Your email address | Email address']
                })

        # Re-evaluate unassigned users
        for user in unassigned_users.copy():
            # Get the user's preferences from the DataFrame
            user_preferences = cls.df.loc[
                cls.df['Attendee ID'] == user['Attendee ID'], activity_cols
            ].values.flatten()

                # Filter out NaN (blank) preferences to get the actual preferred activities
            preferred_activities = [
                activity for preference, activity in zip(user_preferences, activity_cols) 
                if not pd.isna(preference)
            ]
            # Sort the activity columns based on the user's preferences
            sorted_activities = [
                activity for _, activity in sorted(zip(user_preferences, preferred_activities))
            ]
            # Check if the user wants to do an activity
            if cls.df.loc[cls.df['Attendee ID'] == user['Attendee ID'], 'No Activity'].values[0] != 'TRUE': 
                for activity in sorted_activities:
                    user_choice = cls.df.loc[cls.df['Attendee ID'] == user['Attendee ID'], activity].values[0]
                    if not pd.isna(user_choice) and remaining_spaces[activity] > 0:
                        assignments.append({
                            'Attendee ID': user['Attendee ID'],
                            'First Name': user['First Name'],
                            'Last Name': user['Last Name'],
                            'Email address': user['Email address'],
                            'Assigned Activity': activity
                        })
                        remaining_spaces[activity] -= 1
                        unassigned_users.remove(user)
                        break

        # Create DataFrames from the lists
        assignments_df = pd.DataFrame(assignments)
        unassigned_users_df = pd.DataFrame(unassigned_users)

        return assignments_df, unassigned_users_df