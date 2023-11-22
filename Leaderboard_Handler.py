import pickle


def update_Leaderboard(player_name: str, score: int)->None:
    
    run_data = {
        'player_name': player_name,
        'score': int(score)
    }

    
    saves = read_leaderboard_binary_file()

    # Update existing save or append a new one
    if len(saves)<5:
        saves.append(run_data)
    elif len(saves)==5:
        saves.append(run_data)
        saves.sort(key=lambda x:x["score"],reverse=True)
        saves = saves [:-1]

    # Save the updated list back to the file
    with open('Leaderboard.dat', 'wb') as file:
        pickle.dump(saves, file)


def read_leaderboard_binary_file() -> list[{str,int}]:
    try:
        with open('Leaderboard.dat', 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        # Return an empty list if the file doesn't exist or is empty
        return []
