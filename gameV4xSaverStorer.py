import pickle


def save_Game(player_name: str, score: int, player_position: list[int], player_velocity: int, 
              platform_positions: list[list[int]], background_1_positions: list[int], background_2_positions: list[int]):
    
    save_data = {
        'player_name': player_name,
        'score': score,
        'player_position': player_position,
        'player_velocity': player_velocity,
        'platform_positions': platform_positions,
        'background_1_positions': background_1_positions,
        'background_2_positions': background_2_positions
    }

    # Load existing saves or create an empty list
    saves = read_saves_binary_file()

    # Check if the player already has a save
    # if yes existing save index saved to variable otherwise the variable remains as None
    # existing_save_index = next((index for index, save in enumerate(saves) if save['player_name'] == player_name), None)
    existing_save_index = None
    for d in range(len(saves)):
        if saves[d]["player_name"] == player_name:
            existing_save_index = d
            break

    # Update existing save or append a new one
    if existing_save_index is not None:
        saves[existing_save_index] = save_data
    else:
        saves.append(save_data)

    # Save the updated list back to the file
    with open('player_saves.dat', 'wb') as file:
        pickle.dump(saves, file)


def read_saves_binary_file() -> list:
    try:
        with open('player_saves.dat', 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        # Return an empty list if the file doesn't exist or is empty
        return []
