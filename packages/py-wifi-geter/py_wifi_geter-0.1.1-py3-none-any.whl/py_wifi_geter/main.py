import subprocess
import requests


def show_pass(profile=False, passwords=False) -> list or str:
    """
    Get Wi-Fi profiles and their keys.

    Returns:
        list: List of Wi-Fi profiles and their keys.
    """
    wifi_list = []

    see_users = str(subprocess.check_output("netsh wlan show profiles"))
    find_users = see_users[
                 see_users.find("All User Profile     : ") + 23: see_users.find(r"C:\Users\1>netsh wlan show profiles")] \
                     .replace("\\r", "").replace("\\n", "").replace("    All User Profile     : ", " $ ") + " $ "

    count = find_users.count(" $ ")

    list_find_users = find_users.split(" $ ")[0:-1]

    for dont_know in range(1, count + 1):
        try:
            one_user = list_find_users[dont_know - 1]
            "".join(one_user)
            comand = f"netsh wlan show profiles name= \"{one_user}\" key=clear"
            see_pass = str(subprocess.check_output(comand))
            find_pass = see_pass[
                        see_pass.find("Key Content            :") + len("Key Content            :"):see_pass.find(
                            "Cost settings")].replace(r"\r\n", "").replace("            ", "").replace("    ", "")[1::]
            req_it = f"{one_user}:{find_pass}"
            wifi_list.append(req_it.split(":"))
        except Exception as e:
            one_user = list_find_users[dont_know - 1]
            "".join(one_user)
            comand = f"netsh wlan show profiles name= \"{one_user}\" key=clear"
            find_pass = f"Error retrieving password for {one_user}. Exception: {str(e)}"
            wifi_list.append(find_pass)

    if not passwords and not profile:
        return wifi_list
    elif passwords and not profile:
        Passwords = []
        for pr, ps in wifi_list:
            Passwords.append(ps)
        return Passwords
    elif profile and not passwords:
        Profile = []
        for pr, ps in wifi_list:
            Profile.append(pr)
        return Profile
    else:
        return "Please choose one or leave nothing in the parameter if you want both"


def create_file(name: str):
    """
    it creates a file and puts some password and profile in to it

    !! it can't add to your file
    !! it can replace your file with passwords and profiles
    """
    file_fill = ""

    for profile, passwords in show_pass():
        file_fill = file_fill + f"{profile}:{passwords}\n"
    file_fill = file_fill[0:-3]
    with open(name, "w") as f:
        f.write(file_fill)


def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def scan_available_networks():
    """
    Scan and display available Wi-Fi networks in the vicinity.

    Returns:
        list: A list of dictionaries, each containing information about a Wi-Fi network.
    """
    try:
        # Run the command to scan for Wi-Fi networks
        scan_result = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
        scan_result = scan_result.decode("utf-8")

        # Parse the scan results
        networks = []
        current_network = {}

        for line in scan_result.split('\n'):
            line = line.strip()

            if line.startswith("SSID"):
                # New network, add the previous one to the list
                if current_network:
                    networks.append(current_network)
                current_network = {"SSID": line.split(":")[1].strip()}

            elif line.startswith("Signal"):
                current_network["SignalStrength"] = line.split(":")[1].strip()

            elif line.startswith("Authentication"):
                current_network["Authentication"] = line.split(":")[1].strip()

            # Add more conditions to extract other relevant information

        # Add the last network to the list
        if current_network:
            networks.append(current_network)

        return networks

    except Exception as e:
        return {"error": str(e)}
