import requests
import json
import os
import time

def fetch_all_pokemon_forms():
    # The 'limit=1' call is just to find out how many total entries exist
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    
    try:
        initial_response = requests.get(f"{base_url}?limit=1")
        total_count = initial_response.json()['count']
        print(f"Total entries found (including forms): {total_count}")
    except Exception as e:
        print(f"Could not determine total count: {e}")
        return

    pokemon_data = {}
    cwd = r"C:\Me\Python Projects\All Pokemon Sprites"
    file_path = os.path.join(cwd, "all_pokemon_forms.json")

    # We fetch the list of all URLs first to avoid ID gaps
    all_urls_resp = requests.get(f"{base_url}?limit={total_count}")
    results = all_urls_resp.json()['results']

    for entry in results:
        name = entry['name']
        url = entry['url']
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Building the dictionary
            info = {name:data}
            if name == "bulbasaur":
                print(info["bulbasaur"]["sprites"])
                with open(os.path.join(cwd, "bulbasaur-test.json"), "w", encoding="utf-8") as f:
                    json.dump(info, f, indent=4)
            
            pokemon_data.update(info)
            print(f"Fetched: {name} (ID: {data['id']})")
            
            # Politeness delay
            time.sleep(0.05) 

        except Exception as e:
            print(f"Error fetching {name}: {e}")
            continue

    # Save to JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(pokemon_data, f, indent=4)

    print(f"\nSuccess! Total forms saved: {len(pokemon_data)}")

if __name__ == "__main__":
    fetch_all_pokemon_forms()