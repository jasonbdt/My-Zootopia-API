from typing import Any
import json
import sys

from animals_api import *

def load_data(file_path: str) -> Any | str | None:
    """
    Load a text or JSON file.

    Opens the file at ``file_path`` for reading. If the path ends with
    ``.json``, the content is parsed and returned as a Python object;
    otherwise the raw text is returned. Prints an error and returns
    ``None`` if the file is missing.

    Args:
        file_path (str): Path to the input file.

    Returns:
        Any | str | None: Parsed JSON object for ``.json`` files, the
            raw text for non-JSON files, or ``None`` when the file
            cannot be found.
    """
    try:
        with open(file_path, "r") as file_obj:
            if file_path.endswith('.json'):
                return json.load(file_obj)
            else:
                return file_obj.read()
    except FileNotFoundError:
        print(f"File {file_path} doesn't exist! Exiting App...")
        sys.exit(0)


def serialize_animal(animal_obj: dict[str, Any]) -> str | None:
    """
    Serialize an animal record into an HTML list item.

    Extracts the name, locations, diet, lifespan, and skin type from the
    record and renders them as an ``<li>`` card used by the template.
    Optional fields are defaulted to ``'N/A'``. An en dash in
    ``lifespan`` is normalized to a hyphen.

    Args:
        animal_obj (dict[str, Any]): Animal data with ``name``,
            ``locations``, and a ``characteristics`` mapping.

    Returns:
        str | None: The HTML fragment, or ``None`` if required keys
            are missing.
    """
    output = ''
    try:
        name, locations = animal_obj['name'], animal_obj['locations']
        diet, lifespan, skin_type = (
            animal_obj['characteristics'].get('diet', 'N/A'),
            animal_obj['characteristics'].get('lifespan', 'N/A'),
            animal_obj['characteristics'].get('skin_type', 'N/A')
        )
    except KeyError:
        print("Fatal error occurred, unable to serialize animal!")
    else:
        lifespan = lifespan.replace('–', '-')
        locations = ", ".join(locations)

        output += '<li class="cards__item">'
        output += f'<div class="card__title">{name}</div>\n'
        output += '<div class="card__text"><ul>'
        output += f"<li><strong>Diet:</strong> {diet}</li>\n"
        output += f"<li><strong>Location:</strong> {locations}</li>\n"
        output += f"<li><strong>Life span:</strong> {lifespan}</li>\n"
        output += f"<li><strong>Skin type:</strong> {skin_type}</li>\n"

        if 'type' in animal_obj['characteristics']:
            animal_type = animal_obj['characteristics']['type']
            output += f"<li><strong>Type:</strong> {animal_type}</li>\n"
        output += "</ul></div></li>\n"

        return output
    return None


def get_unique_skin_types(animals: list[dict[str, Any]]) -> set[str]:
    """
    Collect unique skin types from the dataset.

    Iterates over the provided records and gathers
    ``characteristics['skin_type']`` when present. Adds the sentinel
    value ``'N/A'`` to represent missing data.

    Args:
        animals (list[dict[str, Any]]): The dataset to scan.

    Returns:
        set[str]: Distinct skin types, including ``'N/A'``.
    """
    unique_skin_types = {
        animal_obj['characteristics'].get('skin_type') for animal_obj
        in animals if 'skin_type' in animal_obj['characteristics']
    }
    unique_skin_types.add('N/A')
    return unique_skin_types


def filter_by_skin_type(
    animal_obj: dict[str, Any],
    chosen_skin_type: str
) -> bool:
    """
    Return True if a record matches the selected skin type.

    A blank selection (``""``) matches all records. The special value
    ``"N/A"`` matches records without a ``skin_type``. Otherwise, a
    case-insensitive equality check is performed.

    Args:
        animal_obj (dict[str, Any]): Animal record to test.
        chosen_skin_type (str): Desired skin type, ``""`` for no filter,
            or ``"N/A"`` to match missing values.

    Returns:
        bool: True if the record passes the filter; otherwise False.
    """
    if chosen_skin_type == "":
        return True
    elif chosen_skin_type == "N/A":
        if 'skin_type' not in animal_obj['characteristics']:
            return True

    if 'skin_type' in animal_obj['characteristics']:
        animal_skin_type = animal_obj['characteristics'].get('skin_type')
        if animal_skin_type.lower() == chosen_skin_type.lower():
            return True

    return False


def get_valid_filter(prompt: str, valid_inputs: list[str]) -> str:
    while True:
        user_choice = input(f"{prompt} ").lower()
        valid_inputs_lower = [input_str.lower() for input_str in valid_inputs]

        if user_choice in valid_inputs_lower or user_choice == "":
            return user_choice
        else:
            print("Invalid selection! Please select an available skin type:")
            print(", ".join(valid_inputs), "\n")


def main() -> None:
    """
    Generate the animals HTML page with optional skin-type filtering.

    Loads the dataset and HTML template, lists available skin types,
    prompts for a filter, serializes matching records, injects the items
    into the template, and writes the result to ``animals.html``.

    Returns:
        None
    """
    animals_data = load_data('animals_data.json')
    html_content = load_data('animals_template.html')

    get_animal("Lion")

    skin_types = sorted(get_unique_skin_types(animals_data))
    print(f"Available skin types: {", ".join(skin_types)}\n")

    user_choice = get_valid_filter(
        "Please choose a skin type (leave blank for no filter):",
        skin_types
    )

    filtered_animals = filter(
        lambda animal_obj: filter_by_skin_type(animal_obj, user_choice),
        animals_data
    )

    output = ""
    for animal_obj in filtered_animals:
        serialized = serialize_animal(animal_obj)
        if serialized:
            output += serialized

    if html_content:
        html_content = html_content.replace('__REPLACE_ANIMALS_INFO__', output)
        with open('animals.html', 'w') as file_obj:
            file_obj.write(html_content)


if __name__ == '__main__':
    main()
