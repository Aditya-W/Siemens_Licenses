import re
from collections import defaultdict

licenses = defaultdict(list)
unique_users = defaultdict(set)

def process_timeslot(timeslot):
    # RegEx for scraping
    license_pattern = re.compile(
        r'Users of (\w+):.*Total of (\d+) licenses? issued;.*Total of (\d+) licenses? in use'
    )

    # Extracting time stamp
    if not timeslot:
        return
    timestamp = timeslot[0]

    # Extracting license lines and user lines
    license_lines = []
    user_lines = []
    for line in timeslot[1:]:
        if line.startswith('Users of'):
            license_lines.append(line)
        else:
            if line.strip():
                user_lines.append(line)

    # Process license lines to get order and total_used
    licenses_in_order = []
    for line in license_lines:
        match = license_pattern.search(line)
        if match:
            software = match.group(1)
            total_issued = int(match.group(2))
            total_used = int(match.group(3))
            licenses_in_order.append((software, total_used))
            # Updating license usage ratio
            licenses[software].append(total_used / total_issued)

    # Assign users to each license based on total_used
    current_index = 0
    for software, total_used in licenses_in_order:
        # Get the next 'total_used' users
        end_index = current_index + total_used
        assigned_users = user_lines[current_index:end_index]
        current_index = end_index

        for user_line in assigned_users:
            # Extract the username (first token before space)
            username = user_line.split()[0]
            unique_users[software].add(username)

def read_file(filename):
    with open(filename, 'r') as file:
        timeslot = []
        for line in file:
            line = line.strip()
            if line == '============================================================':
                if timeslot:
                    process_timeslot(timeslot)
                    timeslot = []
            else:
                timeslot.append(line)
        # Process the last timeslot if not empty
        if timeslot:
            process_timeslot(timeslot)

def avg_usage(license_dict):
    avg_usage = defaultdict(float)
    for key, values in license_dict.items():
        if not values:
            avg_usage[key] = 0.0
            continue

        # Sort the values to trim extremes
        sorted_values = sorted(values)
        n = len(sorted_values)

        # Calculate average of the trim from both ends (15%)
        k = int(0.15 * n)

        # Trim the data (exclude first k and last k elements)
        trimmed_values = sorted_values[k : n - k]

        # Calculate average fo the trimmed data (handle edge cases)
        if not trimmed_values:
            # Fallback: if all data is trimmed, use original data
            avg = sum(sorted_values) / n
        else:
            avg = sum(trimmed_values) / len(trimmed_values)

        avg_usage[key] = avg

    return avg_usage

if __name__ == "__main__":
    file_path = './Overview__LicenseUtilization.txt'
    read_file(file_path)

    # Calculate average usage
    average_usage = avg_usage(licenses)
    print("Average License Usage:")
    for software, avg in average_usage.items():
        print(f"{software}: {avg:.2%}")

    # Calculate unique users
    print("\nUnique Users per License:")
    for software, users in unique_users.items():
        print(f"{software}: {len(users)} unique users")


# trim by 15%
# user entered timeslot
# effective utilization by each user - who are the heaviest users of license. license utilization by the time by each user on each license
# to be done later
# denial log - licenses need to be issued/ de-issued based on the number of denials unique users face
# line graph for effective utilization
# utilization by type, total, user filteration 
                
