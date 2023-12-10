import re

# First function: Extract available translatable captions 
def extract_translatable_languages_and_count(df, column_name='caption'):
    languages = set()
    translatable_captions_count = 0

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Access the dictionary in the specified column
        caption_data = row[column_name]

        # Check if 'captionTracks' is in the dictionary
        if 'captionTracks' in caption_data:
            for item in caption_data['captionTracks']:
                # Check if the caption is translatable
                if item.get('isTranslatable'):
                    # Add the language to the set and increment the counter
                    languages.add(item.get('name'))
                    translatable_captions_count += 1

    return list(languages), translatable_captions_count


#Second function: Extract video and audio quality 
def extract_quality_and_audio(df, column_name='formats'):
    quality_and_audio = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Access the list of dictionaries in the specified column
        format_data = row[column_name]

        # Iterate over each dictionary in the list
        for item in format_data:
            quality = item.get('qualityLabel', 'N/A')  # Default to 'N/A' if not found
            audio_quality = item.get('audioQuality', 'N/A')  # Default to 'N/A' if not found
            quality_and_audio.append((quality, audio_quality))

    return quality_and_audio


#Third function: Extract relevant links from description

def extract_links(df, column_name='description'):
    links = []

    # URL Regular Expression Pattern
    url_pattern = r'https?://[^\s]+'

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Access the description
        description = row[column_name]

        # Find all URLs using the regular expression
        found_links = re.findall(url_pattern, description)
        links.extend(found_links)

    return links
