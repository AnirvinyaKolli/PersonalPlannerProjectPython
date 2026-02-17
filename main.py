"""
Project Name: Personal Planner
Developer: Sai Anirvinya
Date: 2026-02-18
Purpose: This app manages personal time and school work by persisting data to assignment_records.txt.
"""

import os
from Assignment import Assignment 
import requests


API_KEY = "AIzaSyDve4yDbHBo71L2LRtZIvzMbNgpwMizshc"
MODEL = "gemini-2.5-flash"  
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

RECORD_PATH = 'assignment_records.txt'                                      
                                      
def main():    
    cont = 'y'                                  
    while cont == 'y':
        os.system('cls')
        assignments = get_assigments(RECORD_PATH)
        choice = 3
        if assignments:
            try:
                choice = int(input("1 for sort by due date, 2 for sort by difficulty, 3 for adding assigments: "))
            except ValueError:
                choice = 1
            pass
        
        if choice == 1:
            display_assignments(assignments)
            input('Enter to return')
        elif choice == 2:
            display_assignments(assignments, ordering='diff')
            input('Enter to return')
        elif choice == 3: 
            inp = 'y'
            while inp != 'n':
                os.system('cls')
                write_assignment_to_file(
                    get_input(),
                    RECORD_PATH
                )
                inp = input("Add more? (y/n): ")
            assignments = get_assigments(RECORD_PATH)
        cont = input("continue program? (y/n): ")

def get_assigments(path):
    assignments = []
    try:
        with open(path, 'r') as file:
            for line in file:
                fields = line.strip().split('|')
                assignments.append(Assignment(*fields)) 
    except FileNotFoundError: 
        with open(path, 'w'):
            pass
    return assignments

def get_difficulty_sorted(assignments):
    prompt = (
        "Rate each assignment on difficulty from 0 to 10 and "
        "return only each id seperated by a \'|\' sorted by the difficulty most difficult to least"
        "Assignments:\n"
    )
    for i, a in enumerate(assignments):
        prompt += f"{i}: {a.name}, due {a.due_date}"
        try:
            prompt += f', subject:{a.subject}'
        except AttributeError: 
            pass

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    response = requests.post(URL, json=payload)

    if response.status_code == 200:
        data = response.json()        
        raw_text = data['candidates'][0]['content']['parts'][0]['text']

        indices = [int(i) for i in raw_text.strip().split('|')]
        result = [assignments[i] for i in indices]
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

def get_input():
    assignment_name = input('Name of assignment: ')
    due_date = input("Enter date of due (mm/dd/yy): ")
    subject = input("Enter subject (x if N/A): ")
    subject = subject if subject != 'x' else ''
    return f'{assignment_name}|{due_date}|{subject}'

def write_assignment_to_file(input, path):
    try: 
        with open(path, 'a') as file:
            file.write(input +'\n')
    except FileNotFoundError:
        print('Failed')


def display_assignments(assignment_list, ordering = 'due'):
    os.system('cls')
    l = []
    if ordering == 'due':
        l = sorted(assignment_list, key= lambda a: a.due_date)
    elif ordering == 'diff':
        l = get_difficulty_sorted(assignment_list)
    for a in l:
        print(f'{a} \n')

if __name__ == "__main__":
    main()