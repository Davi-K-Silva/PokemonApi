from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load the CSV data into a pandas DataFrame
df = pd.read_csv('pokemon.csv')

# Fill NaN values with an empty string
df = df.fillna('')

# Now convert rows to dictionaries
def pokemon_to_dict(row):
    return row.to_dict()  # This will now work without errors

# # Function to convert row to dictionary
# def pokemon_to_dict(row):
#     print()
#     return {
#         'name': row['name'],
#         'japanese_name': row['japanese_name'],
#         'pokedex_number': row['pokedex_number'],
#         'percentage_male': row['percentage_male'],
#         'type1': row['type1'],
#         'type2': row['type2'],
#         'classification': row['classification'],
#         'height_m': row['height_m'],
#         'weight_kg': row['weight_kg'],
#         'capture_rate': row['capture_rate'],
#         'base_egg_steps': row['base_egg_steps'],
#         'abilities': row['abilities'],
#         'experience_growth': row['experience_growth'],
#         'base_happiness': row['base_happiness'],
#         'hp': row['hp'],
#         'attack': row['attack'],
#         'defense': row['defense'],
#         'sp_attack': row['sp_attack'],
#         'sp_defense': row['sp_defense'],
#         'speed': row['speed'],
#         'generation': row['generation'],
#         'is_legendary': row['is_legendary']
#     }

# READ - Get all Pokémon
@app.route('/pokemon', methods=['GET'])
def get_pokemon():
    pokemon_list = df.apply(pokemon_to_dict, axis=1).tolist()
    return jsonify(pokemon_list)

# READ - Get Pokémon by name
@app.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon_by_name(name):
    pokemon = df[df['name'].str.lower() == name.lower()]
    if pokemon.empty:
        return jsonify({'message': 'Pokémon not found'}), 404
    return jsonify(pokemon_to_dict(pokemon.iloc[0]))

# CREATE - Add new Pokémon
@app.route('/pokemon', methods=['POST'])
def add_pokemon():
    new_pokemon = request.get_json()
    new_df = pd.DataFrame([new_pokemon])
    global df
    df = pd.concat([df, new_df], ignore_index=True)
    return jsonify({'message': 'Pokémon added'}), 201

# UPDATE - Update existing Pokémon
@app.route('/pokemon/<string:name>', methods=['PUT'])
def update_pokemon(name):
    update_data = request.get_json()
    index = df[df['name'].str.lower() == name.lower()].index
    if len(index) == 0:
        return jsonify({'message': 'Pokémon not found'}), 404
    df.loc[index, update_data.keys()] = update_data.values()
    return jsonify({'message': 'Pokémon updated'})

# DELETE - Delete Pokémon
@app.route('/pokemon/<string:name>', methods=['DELETE'])
def delete_pokemon(name):
    global df
    index = df[df['name'].str.lower() == name.lower()].index
    if len(index) == 0:
        return jsonify({'message': 'Pokémon not found'}), 404
    df = df.drop(index)
    return jsonify({'message': 'Pokémon deleted'})

if __name__ == '__main__':
    app.run(debug=True)
