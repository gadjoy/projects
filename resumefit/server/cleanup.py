import json, re

def extract_message_content(message):
    # Extract the content from the ChatCompletionMessage object
    message_content = message.content

    # Convert the message content to a JSON formatted string for readability
    formatted_message = json.dumps(message_content, indent=4)

    # Print the formatted message
    return formatted_message

def clean_string(input_string):
    # Remove leading and trailing quotes if present
    if input_string.startswith('"') and input_string.endswith('"'):
        input_string = input_string.strip('"')

    # Replace \\n with actual newlines
    cleaned_string = input_string.replace('\\n', '\n')
    
    # Replace unicode escape sequences like \\u2022 with actual characters
    cleaned_string = re.sub(r'\\u([0-9A-Fa-f]{4})', lambda x: chr(int(x.group(1), 16)), cleaned_string)
    
    return cleaned_string