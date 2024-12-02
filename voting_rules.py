import numpy as np
# Pairwise majority matrix :

# we call this function element wise on every cell
def pairwise_scoring_(candidate, opponent, P):
    """
    Compare how many voters prefer `candidate` over `opponent`.
    
    Args:
        candidate: The candidate to compare.
        opponent: The opponent candidate to compare.
        P (numpy.ndarray): Preference matrix.

    Returns:
        int: The score indicating how many voters prefer `candidate` over `opponent`.
    """
    # Count voters who rank `candidate` higher than `opponent`
    preference_count = 0
    for ballot in P.T:
        candidate_rank = np.where(ballot == candidate)[0][0]  # Rank of candidate
        opponent_rank = np.where(ballot == opponent)[0][0]    # Rank of opponent
        
        if candidate_rank < opponent_rank:  # Candidate ranked higher than opponent
            preference_count += 1
    
    return preference_count



def create_pairwise_majority_matrix(P):
    """
    Create a pairwise majority matrix from a preference matrix.

    Args:
        P (numpy.ndarray): A matrix of preferences of shape (num_candidates, num_voters).

    Returns:
        numpy.ndarray: The pairwise majority matrix.
    """
    # Map candidates to indices for the pairwise matrix
    candidates = np.unique(P)
    candidate_index_pmr = {candidate: index for index, candidate in enumerate(candidates)}

    num_candidates = len(candidates)
    pmr = np.zeros((num_candidates, num_candidates))

    for voter in range(P.shape[1]):  # Iterate over each voter
        ballot = P[:, voter]  # Get the preferences of a single voter
        for i, candidate in enumerate(ballot):
            for j, opponent in enumerate(ballot):
                if i < j:  # Only compare unique pairs
                    if candidate != opponent:
                        pmr[candidate_index_pmr[candidate], candidate_index_pmr[opponent]] += 1

    return pmr


def condorcet_winner(pmr):
  num_candidates = len(pmr)

  for i in range(num_candidates):
      is_winner = True
      for j in range(num_candidates):
          if i != j:
              if pmr[i, j] <= pmr[j, i]:
                # if it get's defeated by a single one then it's not the winner
                  is_winner = False
                  break
      if is_winner:
          return i  # the winner

  return -1  # no winner


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

def borda_winner(preferences):
    m = preferences.shape[0]  # Number of candidates
    borda_vector = [i for i in range(m - 1, -1, -1)]  # Borda scores for ranks
    borda = pos_scoring_rule(preferences, borda_vector)  # Compute scores
    winner = max(borda.items(), key=lambda k: k[1])[0]  # Get the candidate with max score
    return winner 

import numpy as np

def k_approval_winner(preferences, k=3):
    """
    Implements the Approval Voting rule assuming voters approve of their top k candidates.
    
    Args:
        preferences (numpy.ndarray): 
            A 2D array where each column represents a voter's ranking of candidates, 
            and each row represents a candidate.
            Lower values represent higher ranks (e.g., 1st, 2nd, 3rd, etc.).
        k (int): The number of top candidates each voter approves. Default is 3.
    
    Returns:
        tuple: A tuple (winners, score), where:
            - winners: A list of candidates with the most approvals (as strings).
            - score: The number of approvals the winners received (as an integer).
    """
    # Initialize approval counts for each candidate (each row is a candidate)
    approval_counts = np.zeros(preferences.shape[0])  # Number of candidates
    
    # For each voter (column), approve the top k candidates
    for voter in preferences.T:  # Iterate over columns (voters)
        top_k_candidates = np.argsort(voter)[:k]  # Indices of the top k ranked candidates
        approval_counts[top_k_candidates] += 1  # Increment approval count for top k candidates
    
    # Find the maximum approval count
    max_approval_count = approval_counts.max()
    
    # Find all candidates with the maximum approval count
    winners = [str(i + 1) for i in range(len(approval_counts)) if approval_counts[i] == max_approval_count]
    
    return winners



def plurarity_winner(P):
    num_candidates = P.shape[0]
    num_voters = P.shape[1]
    
    w = np.zeros(num_voters) 
    w[0] = 1  # Giving a score of 1 for the top-ranked candidate

    score = pos_scoring_rule(P, w)  # Compute scores based on the scoring rule
    winner = max(score.items(), key=lambda k: k[1])[0]  # Get the candidate with max score
    return winner  # Return only the winner (candidate)


# recursive implementation of STV

def stv_winner(P):

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
        winner = stv_winner(P)

    return winner

def copeland_winner(preferences):
    """
    Implements Copeland's voting method using an external function for pairwise matrix calculations.

    Args:
        preferences (numpy.ndarray): 
            A 2D array where each row represents a voter's ranking of candidates, 
            and each column represents a candidate.
            Lower values represent higher ranks (e.g., 1st, 2nd, 3rd, etc.).
        pairwise_matrix_func (function): A function that calculates the pairwise comparison matrix.

    Returns:
        tuple: A tuple (winner, score), where:
            - winner: The candidate with the highest Copeland score.
            - score: The Copeland score of the winner.
    """
    # Use the existing function to calculate the pairwise matrix (pmr)
    pmr = create_pairwise_majority_matrix(preferences)
    
    # Copeland's score calculation: row_sum - col_sum
    row_sum = np.sum(pmr, axis=1)
    col_sum = np.sum(pmr, axis=0)
    copeland_score = row_sum - col_sum

    # Find the candidate with the highest Copeland score
    max_index = np.argmax(copeland_score)
    winner = np.unique(preferences)[max_index]  # Assuming candidates are 0-indexed and sorted
    score = copeland_score[max_index]
    
    return winner


