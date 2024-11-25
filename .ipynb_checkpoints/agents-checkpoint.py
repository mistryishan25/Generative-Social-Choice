# create agents for each author in the list and 



# agent for each user 
def create_agent_from_participants(context, reply, task):
    """
        prompt : ACTION or ROLE that you want your agent to perform. 
    """
    prompt = f" You are a commentor on the post that has the following context : {context}; 
    and your reply to this post was {reply}.  Do the required {task} from this person's perspective based on his reaction to the post.
    
    For example, if the context was : Veganism is great and it is inhumane for others to eat animal products. ; 
    your reply to this post was : It is more about having a convinient protien rich diet for people who cannot afford expensive vegan foods.
    The task is to arrange the statments S1, S2, S3 in the order of decreasing order of agreement. 
    
    S1 : I understand that there are plant based meats but they do not taste the same. Also it is a little more expensive and not readily available.
    S2 : I hate how you vegans try to shove it in our face let people do what they want to. To each their own! 
    S3 : Vegans are not getting balanced diets because they are protien deficient meals
    
    The answer would be a list : [S1,S3,S2] and some reasoning for the order like : the person gets the problem but can't help it. Also, this person seems more health conscious. "




# generate slate



# justified representation 