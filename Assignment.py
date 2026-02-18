from datetime import datetime, date
class Assignment():
    def __init__(self, assignment_name, due_date, subject = ''):
        self.name = assignment_name
        try: 
            self.due_date = datetime.strptime(due_date, "%m/%d/%y").date()
        except ValueError:
            self.due_date = date.today().replace(year = date.today().year + 1)
        if subject != '':
            self.subject = subject

    # Formates them
    def __str__(self):
        f_a = f'{self.name} \n\t Due: {self.due_date}'
        try:
            f_a += f'\n\t Subject: {self.subject}'
        except AttributeError:
            pass
        return f_a 

