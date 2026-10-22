test_settings = {
    'theme': 'light'

}


def add_setting(dictionary, key_value):

    key, value = key_value

    key, value = key.lower(), value.lower() # lower() fa diventare tutto minuscolo

    if key in dictionary:

        return f"Setting '{key}' already exists! Cannot add a new setting with this name."

    else:

        dictionary[key] = value

        return f"Setting '{key}' added with value '{value}' successfully!"

def update_setting(dictionary, key_value):

    key, value = key_value

    key, value = key.lower(), value.lower()

    if key in dictionary:

        dictionary[key] = value

        return f"Setting '{key}' updated to '{value}' successfully!"

    else:

        return f"Setting '{key}' does not exist! Cannot update a non-existing setting."

def delete_setting(dictionary, key):

    key = key.lower()

    if key in dictionary:

        dictionary.pop(key) # pop() cancella quel singolo elemento che vuoi cancellare

        return f"Setting '{key}' deleted successfully!"

    else:

        return "Setting not found!"

def view_settings(dictionary):

    if dictionary == {}:

        return "No settings available."

    else:

        result = "Current User Settings:\n"

        for key, value in dictionary.items(): # items() restituisce coppie chiave-valore da un dizionario


            result += f"{key.capitalize()}: {value}\n" #non va mai la virgola tra la key e la value, perchè diventano tuple, usa i ":"... capitalize() fa diventare maiuscole la lettera iniziale

        return result

tuple1 = ('volume', 'high')

tuple2 = ('theme', 'dark')

print(add_setting(test_settings, tuple1))

print(update_setting(test_settings, tuple2))