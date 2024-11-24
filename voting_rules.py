import numpy as np
# Pairwise majority matrix :

# we call this function element wise on every cell
def pairwise_scoring(candidate, opponent, P):
  other_candidates = set(np.unique(P)) - set(candidate)
  wins = 0
  # over all ballots see how many times the candidate wins
  for ballot in P.T:

    ballot = list(ballot)
    candidate_index = ballot.index(candidate)
    opponent_index = ballot.index(opponent)
    # print(f"ballot - {ballot} \n candidate_index - {candidate_index}, \n opponent_index - {opponent_index}")
    if candidate_index > opponent_index:
      wins += 1
    # print(f"wins = {wins}")
  return wins



def create_pairwise_majority_matrix(P):

  candidate_index_pmr = {candidate : index for index, candidate in enumerate(np.unique(P))}
    # P is a matrix of preferences of shape (num_candidates, num_voters)

  num_candidates = P.shape[0]
  pmr = np.zeros((num_candidates,num_candidates))

  for ballot in P.T:
    for candidate in ballot:
      for opponent in ballot:
        # print(f"ballot - {ballot} \n candidate - {candidate}, \n opponent - {opponent}")
        try :
          if candidate != opponent and candidate!= "" and opponent!="":
            pmr[candidate_index_pmr[opponent], candidate_index_pmr[candidate]] = pairwise_scoring(candidate, opponent, P)
          else :
            pmr[candidate_index_pmr[opponent], candidate_index_pmr[candidate]] = 0
        except :
          print(f"Error at candidate - {candidate}, \t opponent - {opponent}")
  return pmr


def pos_scoring_rule(P,w):
  # As per the notation,
  # P - Ballots or preferences,
  # A - Candidates,
  # w - Weight vector

  score= {candidate : 0 for candidate in np.unique(P)}

  for ballot in P.T:
    for index, candidate in enumerate(ballot):
      # print(f"ballot - {ballot} \n index - {index}, \n candidate - {candidate}")
      score[candidate] += w[index]
      # print(f"score - {score}")
  return score

def plurarity_winner(P):
  
  num_candidates = P.shape[0]
  num_voters = P.shape[1]
  
  w = np.zero(num_voters) 
  w[0] = 1 

  score = pos_scoring_rule(P,w)
  winner = max(score.items(), key=lambda k: k[1])
  return winner

# recursive implementation of STV

def stv_scoring_rule(P):

    # P is a matrix of preferences of shape (num_candidates, num_voters)
    num_candidates = P.shape[0]
    num_voters = P.shape[1]

    # defined a key within the function to store the index of each candidate
    candidate_index_stv = {candidate: index for index, candidate in enumerate(np.unique(P))}

    # using the plurarity vector as the weight vector
    weight_plurarity = np.zeros(num_candidates)
    weight_plurarity[0] = 1

    # calculate plurality score for each candidate
    plurarity = pos_scoring_rule(P, weight_plurarity)
    plurarity_winner, max_votes = max(plurarity.items(), key=lambda k: k[1])

    # using the previous results for a majority check
    if max_votes > num_candidates / 2:
        print(f"majority found - {plurarity_winner}")
        return plurarity_winner
    else:
        print("majority not found")

        # create pairwise majority matrix - pmr
        pmr_stv = create_pairwise_majority_matrix(P)

        # calculate candidate losses from the pmr
        candidate_losses = {candidate: np.sum(pmr_stv[:, candidate_index_stv[candidate]], axis=0)
                            for candidate, index in candidate_index_stv.items()}

        # eliminate the candidate with the most losses
        elimination, max_loses = max(candidate_losses.items(), key=lambda k: k[1])
        # print(f"elimination - {elimination}")

        # remove the eliminated candidate from every voter's preference while preserving order
        P = np.array([[candidate for candidate in P[:, i] if candidate != elimination] for i in range(num_voters)]).T

        print(f"Updated P after eliminating {elimination}: \n{P}")

        # recursively call STV with the updated preferences
        winner = stv_scoring_rule(P)

    return winner

