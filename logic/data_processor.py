import pandas as pd
import random

class DataProcessor():

    def __init__(self) -> None:
        self.df = None  # Initialize df to None
        self.preference_cols = None  # Initialize preference_cols to None

    @classmethod
    def set_data(cls, data):
        cls.df = data
        cls.preference_cols = ['My top preference:', 'My second preference:', 'My third preference:']

    @classmethod
    def assign_to_activity(cls, max_spaces):
        """
        Assigns users to activities based on their preferences and available spaces,
        prioritizing choices in order (1st, 2nd, 3rd, etc.).

        Args:
            max_spaces: A dictionary specifying the maximum spaces for each activity.
        Returns:
            A tuple containing two elements:
                - assignments: A DataFrame with columns 'Attendee ID', 'First Name', 'Last Name', 'Email address' and 'Assigned Activity'.
                - unassigned_users: A DataFrame with columns 'Attendee ID', 'First Name', 'Last Name', and 'Email address' for users who could not be assigned.
        """

        assignments = []
        unassigned_users = []
        remaining_spaces = max_spaces.copy()

        # Create a set of assigned user indices
        assigned_users = set()

        # Iterate through choices in order (1st, 2nd, 3rd, etc.)
        for choice_col in cls.preference_cols:
            for activity, spaces in remaining_spaces.items():
                if spaces > 0:
                    # Consider only unassigned users for the current choice
                    potential_users = cls.df[
                        (cls.df[choice_col] == activity) & 
                        (~cls.df['Attendee ID'].isin(assigned_users)) & 
                        (cls.df['Do you want to take part in an activity?'] == 'Yes')
                    ].index.tolist()
                    random.shuffle(potential_users)

                    for user_index in potential_users:
                        if remaining_spaces[activity] > 0:
                            assignments.append({
                                'Attendee ID': cls.df.loc[user_index, 'Attendee ID'],
                                'First Name': cls.df.loc[user_index, 'First, please confirm your name: | First name'],
                                'Last Name': cls.df.loc[user_index, 'First, please confirm your name: | Last name'],
                                'Email address': cls.df.loc[user_index, 'Your work email address: | Email address'],
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
                    'First Name': row['First, please confirm your name: | First name'],
                    'Last Name': row['First, please confirm your name: | Last name'],
                    'Email address': row['Your work email address: | Email address']
                })

        # Re-evaluate unassigned users
        for user in unassigned_users.copy():
            user_preferences = cls.df.loc[
                cls.df['Attendee ID'] == user['Attendee ID'], cls.preference_cols
            ].values.flatten()

            for preference in user_preferences:
                if preference in remaining_spaces and remaining_spaces[preference] > 0:
                    assignments.append({
                        'Attendee ID': user['Attendee ID'],
                        'First Name': user['First Name'],
                        'Last Name': user['Last Name'],
                        'Email address': user['Email address'],
                        'Assigned Activity': preference
                    })
                    remaining_spaces[preference] -= 1
                    unassigned_users.remove(user)
                    break

        # Create DataFrames from the lists
        assignments_df = pd.DataFrame(assignments)
        unassigned_users_df = pd.DataFrame(unassigned_users)

        print(assignments_df)
        print(unassigned_users_df)

        return assignments_df, unassigned_users_df

    @classmethod
    def clear_data(cls):
        cls.df = None
        cls.preference_cols = None