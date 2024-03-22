import pickle


def update_Leaderboard(player_name: str, score: int) -> None:
    """function to save top 5 runs

    Args:
        player_name (str): name player uses to play game
        score (int): player run score
    """
    # object save in pickle file
    run_data = {
        'player_name': player_name,
        'score': int(score)
    }

    saves = read_leaderboard_binary_file()

    # append a new one run record if less than 5 people
    if len(saves) < 5:
        saves.append(run_data)
    elif len(saves) == 5: # else recalculate top 5 then update game
        saves.append(run_data) # add new record to array of previous top 5
        saves.sort(key=lambda x: x["score"], reverse=True)  # sort array from highest to lowest
        saves = saves[:-1] # take top 5 onluy

    # Save the updated list/top 5 back to the file
    with open('Leaderboard.dat', 'wb') as file:
        pickle.dump(saves, file)


def read_leaderboard_binary_file() -> list:
    try:
        with open('Leaderboard.dat', 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        # Return an empty list if the file doesn't exist or is empty
        return []
