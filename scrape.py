import re
from collections import defaultdict

licenses = defaultdict(list)

# {'nx_integration':[],'teamcenter_admin':[],'teamcenter_author':[],
#             'teamcenter_consumer':[],'visview_base':[],'visview_pro':[],'visview_std':[]}

def extract_licenses(file_content): 
    pattern = re.compile(r'Users of (\w+):.*Total of (\d+) licenses? issued;.*Total of (\d+) licenses? in use') 
    for line in file_content: 
        match = pattern.search(line) 
        # print('checking' , match, line)
        if match: 
            software = match.group(1) 
            total_issued = int(match.group(2)) 
            total_used = int(match.group(3))
            licenses[software].append(total_used/total_issued)
            #print(f"{software}: {total_used} licenses in use out of {total_issued} issued")

def read_file(filename):
    with open(filename, 'r') as file:
        timeslot  = []
        for line in file:
            if line.strip() != '============================================================':
                timeslot.append(line.strip())
            else:
                extract_licenses(timeslot)
                timeslot = []

    return timeslot


def avg_usage(license_dict):
    avg_usage = defaultdict(list)
    for key in license_dict:
        avg = sum(license_dict[key])/len(license_dict[key])
        avg_usage[key].append(avg)
    return avg_usage
        


file = './Overview__LicenseUtilization.txt'

res = read_file(file)
extract_licenses(res)

avg_usage = avg_usage(licenses)

#print(licenses['teamcenter_author'])
print(avg_usage)

# teamcenter_admin not being printed
# unique users
# standard deviation
# time slot
# 