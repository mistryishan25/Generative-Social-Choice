USER_TO_AGENT = ""


AGENT_TO_STATEMENT_PROMPT = """\
In a qualitative survey about chatbot personalization, a participant has given the following answers:
----
{desc}
----
Based on the opinions the user has articulated above, write a statement for them with the following, specific format: \
Start the statement with 'The most important rule for chatbot personalization is'. GIVE A SINGLE, CONCRETE RULE. \
Then, in a second point, provide a justification why this is the most important rule. \
Then, give an CONCRETE example of why this rule would be beneficial. Write no more than 50 words.
"""


GEN_SUMMARY = "Your task is to summarize the comments as CONCISELY as possible. No need for formal language or nice phrasing. Determine the number of UNIQUE viewpoints you can find. Beware, not each comment would have a unique viewpoint. DO NOT use your knowledge about the world, stick to what the participants said. Do not put quotes around your response. Give the ouput in a JSON format, with a number(from 1) for EACH UNIQUE viewpoint"

