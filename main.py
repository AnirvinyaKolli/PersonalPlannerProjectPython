RECORD_PATH = 'assignment_records.txt'

def main():
    display_assignments(RECORD_PATH)
    
    inp = 'n'
    while inp != 'n':
        write_assignment_to_file(
            get_input(),
            RECORD_PATH
        )
        inp = input("Add more? (y/n)")

def display_assignments(path):
    try:
        with open(path, 'r') as file:
            for a in file: 
                print(
                    format_record(a)
                )
    except FileNotFoundError: 
        open(path, 'w')

def format_record(input):
    records = input.split('|')
    f = ''
    for r in records:
        f += r + '\n'
    return f 

def get_input():
    assignment_name = input('Name of assignment')
    due_date = input("Enter date of due")
    subject = input("Enter subject (x if N/A)")
    subject = subject if subject == 'x' else ''
    return f'{assignment_name}|{due_date}|{subject}'

def write_assignment_to_file(input, path):
    try: 
        with open(path, 'a') as file:
            file.write(input +'\n')
    except FileNotFoundError:
        return Exception

if __name__ == '__main__':
    main()