"""
Aim : How effective the extraction of preferences from the 

Steps : 
0. Generate a slate of comments that are Justied Representation versions of the comments. 
1. For each user in the dataset, we use the post description and their comment as input to the LLM agent. 
2. One the agent is ready, it is asked to order the preferences from the slate.
3. Then we apply the voting rule to see which of the voting rules works and predicts the verdict.  


"""


def create_agent(LLM, context, prompt)
