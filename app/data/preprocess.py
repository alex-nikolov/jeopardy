import pandas as pd
import re

df = pd.read_csv('jeopardy_questions.csv')
new_columns = {c:c.strip() for c in list(df.columns)}
df = df.rename(columns=new_columns)

def remove_a_tags_keep_text(s):
    return re.sub(r'<a[^>]*>(.*?)</a>', r'\1', s)

def preprocess_value(v):
    if isinstance(v, str):
        return int(v[1:].replace(',', ''))
    return v

df['Question'] = df['Question'].apply(remove_a_tags_keep_text)
df['Value'] = df['Value'].apply(preprocess_value)
df['Value'] = df['Value'].fillna(0)

df = df.to_csv('jeopardy_sanitized.csv', index=False)

