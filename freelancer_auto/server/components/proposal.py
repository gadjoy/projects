def generate_proposal(title, description):

    prompt = f"""

    INPUT:

    Role: You are a client-focused project proposal expert with strong understanding of the client's vision.

    Context: The client's requirements are analyzed for a software project. You have a solid understanding of their needs and have prepared the following:

    Project Title: {title}
    Project Description: {description}

    Project Summary: Begin with a 2-3 sentence overview of the potential project, emphasizing its key benefits derived from the client's requirements.
    Project Understanding: Write 2-3 paragraphs highlighting how your solution addresses their needs:
    Emphasize that you carefully analyzed their needs and developed a clear project description, providing a solid foundation.
    Stress your commitment and focus by proactively outlining the project's scope and objectives
    Solution Fit: Briefly explain how your solution's design meets their requirements (provide a top-level explanation). This establishes a focus on quality and alignment with their goals.
    Client-Centric Value: Explain how your project outline provides clarity to ensure the project evolves in accordance with their vision.
    Invitation to Collaboration:
    Underscore your commitment to their feedback and invite the client to further refine project goals as a collaborative effort.
    Call to Action: Suggest next steps, such as discussing a formal development plan.


    Additional Considerations:

    Tone: Proactive, demonstrating your understanding of the client's needs.
    Client Ownership: Clearly acknowledge the collaborative nature of the project and their role in its direction.
    Concise: The proposal should be easily readable in one sitting.
    Outcome: The client should be clearly told that we would like to do the whole software development process for a proof of concept with SRS, Architecture, Workflows, Message sequence charts, UI wireframes as part of showing our skills rather than just saying we can do it.
    Keep it within 1400 characters with spaces
    """


    from dotenv import load_dotenv, find_dotenv
    import os, requests

    # Load environment variables from .env file
    _ = load_dotenv(find_dotenv())

    # Set the API key
    api_key = os.environ['GOOGLE_API_KEY']

    # Set the API endpoint
    endpoint = "https://generativelanguage.googleapis.com/v1beta"

    # Prepare the request body
    request_body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Make the request to Generative Language API
    response = requests.post(
        f"{endpoint}/models/gemini-pro:generateContent?key={api_key}",
        json=request_body,
    )

    # Check if 'questions' key exists in the response JSON
    if response.status_code == 200:
        # response_json = response.json()
        # print(response.json())
        proposal = response.json()['candidates'][0]['content']['parts'][0]['text']
        return proposal