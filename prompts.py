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


# did not work, the statements selected seemed ranadom and were just giving the same order if run again.

AGENT_PROMPT_TEMPLATE = PromptTemplate.from_template( """
You are a commentor on a post with description from the author is as follows : 
----
{description} 
----
You have put the following opinion as a comment on the post : 
----
{comment}
----

----
{slate}
----

Given, the description and your comment as stance, think like this person and try to order the statements from the slate in an order that goes from MOST LIKED to LEAST LIKED.
The output would just be a list with ranks of the statements, for example if there are 3 statements :[3,2,1] where 3>2>1, meaning they prefer/agree the most with 3, and then 2 and 1 is the least liked.
ONLY respond with the list of ordering.You need to RANK all of the statements. Reorder the ranks if needed, in most cases the order might not the same and be something random.
DO NOT SKIP on any of the statements. 


""")


# this worked a little but on inspection it did not work the way I intended it to. 
# For example, I took a YTA comment and observed the statements did match the expected ordering but then it was in the middle.
# For example, [1,2,3,4,5,6,7]
AGENT_PROMPT_TEMPLATE = PromptTemplate.from_template( """
You are a commentor on a post. The post is from r/AITA the with the following description: 
----
{description} 
----
Imagine you are a redditor and you have put the following comment on the post as a reflection of what you think : 
----
{comment}
----

These are the summarized statements/opinions across all the other comments(including yours).
----
{slate}
----

Given, the description and the comment as your stance, think like this person and try to order ALL the statements from the slate in an order that goes from MOST LIKED to LEAST LIKED.
The output would just be a list with ranks of the statements in that order, for example if there are 10 statements :[4,5,6,10,3,2,1,7,9,8], meaning they prefer/agree the most with 4 and 8 is the least liked.
 Reorder the ranks if needed, in most cases the order might not the same and be something random.
 
RULES TO STRICTILY FOLLOW : 
1. DO NOT SKIP any statements.You NEED TO RANK all of the statements.
2. ONLY respond with the list of ordering.
3. FOLLOW the format where the output is just a list
4. Each RANK should be in the output exactly once.


""")