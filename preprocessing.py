import pandas as pd
import re
def preprocess(data):
    dates = []
    messages = []

    lines = data.split('\n')

    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            match = re.match(r'^(.+?)\s-\s(.+)$', line)

            if match:
                dates.append(match.group(1))
                messages.append(match.group(2))
    df = pd.DataFrame({'date': dates, 'user-messages': messages})
    df['date'] = df['date'].str.replace('\u202f', ' ')  # Replace Unicode space with regular space

    # Filter out rows that don't match the date pattern
    date_pattern = r'^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} [AP]M$'
    df = df[df['date'].str.match(date_pattern, na=False)]

    # Now convert to datetime
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour

    users = []
    messages = []
    for message in df['user-messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user-messages'], inplace=True)
    return df


