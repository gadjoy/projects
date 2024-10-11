prompt = """"
                ### Task Description:
                **You are a resume writing expert specializing in tailoring resumes to specific job descriptions. Your task is to refine the resume to enhance clarity, coherence, grammar, and style while aligning it with the given job description. You must not invent or fabricate any new details.**

                ### Steps:

                - Analyze the base resume and job description for key skills, qualifications, and experiences.
                - Adjust and refine the resume to match the job description by highlighting relevant experiences, skills, and achievements.
                - Use action verbs and tailor the language to the job's responsibilities and requirements, ensuring maximum relevance to the job description.
                - Ensure there are no grammatical errors or inconsistencies and that the resume flows logically.
                - Maintain the user's original meaning and intent while customizing it to the job description. Do not add any fictional or unprovided information.

                ### Output Instructions:

                - Customized resume that is highly relevant to the provided job description.
                - A list of recommendations for further improvement, such as specific sections that could be expanded with real examples or how to better showcase achievements.
                - Include NO additional commentary or explanation in the response.
         """

base_resume = """

VIVEKANAND B
Engineer • Innovator • Entrepreneur
vivekanandb@hotmail.com | +91-97381-26623
github.com/vivekanandba | www.linkedin.com/in/vivekanand-balakrishnan-68448777
SUMMARY
Experienced Software and Mechanical Engineer with over 10 years of expertise in aerospace, medical robotics, and AI-powered applications. Proven ability to develop cloud-based solutions, automate processes using AI, and lead cross-functional teams to success. Founded a successful gadget repair business, showcasing entrepreneurial spirit and business acumen. Proficient in Python, JavaScript, GCP, and healthcare standards like ISO 13485. Passionate about leveraging AI to create innovative solutions that make a meaningful impact on the world.
SKILLS
•	Programming Languages & Frameworks: Python, JavaScript, Flask, Vue.js, Playwright
•	AI: OpenAI API, Google Vertex API, Github Copilot, Vision API, TTS
•	Data Analysis & Visualization: Pandas, Power BI, Jupyter
•	Cloud & DevOps: Google Cloud Platform[GCP] (VM, Serverless, VPC), Docker, Jenkins
•	Databases: MongoDB, MySQL, SQLite
•	Tools & Project Management: RESTful APIs, Software Architecture, Jira, Agile, ISO 13485, networking protocols, DICOM, HL7
EXPERIENCE
PROGRAMMING
Software Engineer | NovaSignal / NeuraSignal | Bangalore, India
Nov 2020 – Present
Data View Application
•	Key Contributions: Developed a web-based app using Python, Flask, and Streamlit for real-time insights into robotic system deployments. Extracted and analysed large datasets with SQL and Power BI.
•	Impact: Empowered sales, medical education, and management teams to make data-driven decisions, improving operational efficiency and robotic system utilization.
•	Technologies: Python, Flask, Streamlit, SQL, Power BI, Docker, GCP (Cloud Run)
AI-Driven Test Automation
•	Key Contributions: Created automated test scripts for GUI applications using Python, PyTest, and Pywinauto. Leveraged OpenAI tools to automate test script development and GUI interactions.
•	Impact: Reduced development and testing time by 30%, increased test coverage, and introduced AI into test automation processes.
•	Technologies: Python, PyTest, Pywinauto, OpenAI Assistant API, Vision API, Vertex AI
Cloud Progressive Web Applications (Europa, Venus, Galileo, Jupiter, Saturn)
•	Key Contributions: Supported testing for multiple cloud applications using Playwright for UI and PyTest for API testing. Developed internal tools with Python and Flask and contributed to DevOps activities using GCP.
•	Impact: Accelerated development and testing cycles, enhanced scalability and reliability of cloud applications, and reduced time-to-market.
•	Technologies: Python, Flask, Vue.js, Playwright, PyTest, GCP, Docker, Jenkins
Microservices and API Development
•	Key Contributions: Designed and tested RESTful APIs for secure data transmission between hospital EMR systems and cloud services. Implemented HL7 and DICOM standards for healthcare data exchange.
•	Impact: Improved integration with hospital systems, ensured compliance with healthcare regulations, and enhanced data security.
•	Technologies: Python, Flask, RESTful APIs, DICOM, HL7, MLLP, GCP (VPC, Cloud Run)
Automation Tools and Frameworks
•	Key Contributions: Developed automation tools like a DICOM Decoder for verifying medical imaging data and a SOUP Creator Tool for security audits of open-source components.
•	Impact: Increased efficiency by automating repetitive tasks, ensured compliance with industry standards, and improved product reliability.
•	Technologies: Python, PyTest, Jenkins, Docker, GCP
ENTREPRENEURIAL 
Founder & Technician | Gadjoy Repair Services | Bangalore, India
Nov 2016 – Jan 2021
•	Founded and managed a successful laptop and gadget repair service, handling over 1,000 devices and 100+ customers per month, and achieving a 4.7+ customer satisfaction rating across multiple platforms.
•	Developed and implemented custom software systems to monitor customer devices, manage checklists, and streamline ledger and enquiry entries. Leveraged Excel as a functional database, utilizing advanced features to trace device activities, which increased operational efficiency by 80%.
•	Acquired transferable skills in team management, customer service, and business development, alongside technical expertise in software development, database management
MECHANICAL
Sr. Engineer | Tech Mahindra | Jan 2019 – Jan 2021
Senior Lead Engineer | Legend Technologies | Jan 2013 – Jan 2019
Trainee Engineer | Safran Engineering India | Aug 2011 – Dec 2012

•	Led multidisciplinary teams in the design and fabrication of aerospace & locomotive jigs and fixtures for clients like ISRO, Safran, and Pratt & Whitney. 
•	Provided end-to-end support in manufacturing, testing, and service, overseeing the entire product lifecycle
•	Utilized advanced CAD and simulation tools to do mechanical design and analysis of aerospace components and developed custom software scripts to automate design tasks reducing design time & in the process gaining transferable skills like applying analytical and project management.
EDUCATION
•	Bachelor of Engineering (Mechanical Engineering) - Visvesvaraya Technological University (VTU) | First Class with Distinction | 2011
•	Deep Learning Specialization & Machine Learning Specialization (Andrew Ng) & Multiple Short Course on AI, Tooling, Ops
PATENTS & PUBLICATIONS
•	Patents: System and Method of Generating Image of Vascular Flow Network - US20230329668A1
•	White Papers: Published research on aerospace manufacturing and slip ring design. 
VOLUNTEERING
•	Contributed to the development of an IoT-based air quality monitoring system (AirCare) and a COVID relief distribution platform (Stop Hunger) with mapshalli.org, Whitefield, Bangalore.
•	Mentored school children, engineering graduates (for skill development), and junior professionals (for career growth).
•	Assisted in organizing engineering society events within the local community.

"""

job_description = """
Position: AI Integration and Test Automation Specialist - Microsoft Dynamics 365 Business Central

Experience: 5-8 years

Location: [Specify location]

Job Description:

We are looking for an experienced AI Integration and Test Automation Specialist with 5-8 years of experience in Microsoft Dynamics 365 Business Central. The ideal candidate will have a strong background in artificial intelligence (AI), test automation, and integration with the latest version of Business Central.

Responsibilities:

Develop and implement AI solutions to enhance the functionality and efficiency of Business Central. 
Design and implement test automation frameworks and scripts for Business Central applications. 
Integrate AI-powered applications with Business Central using standard integration techniques. 
Collaborate with cross-functional teams to ensure successful integration and testing of AI solutions. 
Provide technical expertise and guidance on AI integration and test automation best practices. 

Requirements:

Bachelor's degree in Computer Science, Engineering, or related field. 
5-8 years of experience in AI development, test automation, and integration with Microsoft Dynamics 365 Business Central. 
Strong proficiency in AI technologies such as machine learning, natural language processing, and computer vision. 
Experience in designing and implementing test automation frameworks for Business Central. 
Demonstrated ability to integrate AI-powered applications with Business Central using APIs, web services, etc. 
Excellent problem-solving skills and attention to detail. 
Strong communication and interpersonal skills. 

"""