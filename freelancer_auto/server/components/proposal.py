import os
import requests
import re
from dotenv import load_dotenv
def generate_proposal(project_title: str, project_description: str):
    # set api key and api endpoint
    load_dotenv()
    api_key = os.environ.get('GOOGLE_API_KEY')
    endpoint = "https://generativelanguage.googleapis.com/v1beta2"

    # generate the prompt to get my proposal
    prompt = f"""

    INPUT:

    Role: You are a client-focused project proposal expert with strong understanding of the client's vision.

    Context: The client's requirements are analyzed for a software project. You have a solid understanding of their needs and have prepared the following:

    Project Title: {project_title}
    Project Description: {project_description}

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

    # prepare the request body
    request_body = {
        "prompt": {
            "text": prompt
        }
    }

    # make the request to generative language api
    response = requests.post(f"{endpoint}/models/text-bison-001:generateText?key={api_key}", json=request_body)

    # get the generated proposal from the response
    try:
        proposal = response.json()['candidates'][0]['output']
    except KeyError:
        # Handle the error if the response does not contain the expected data
        print('Error: The API response does not contain the expected data.')
        return None

    
    print(f"Generated proposal: {proposal}")

    # save the generated proposal to a file
    with open("proposal.txt", "w") as f:
        f.write(proposal)
    print("Proposal saved to proposal.txt")

    # return the generated proposal
    return proposal
