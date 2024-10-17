class Applicant:
    """
    Applicant class is used to create an object of an applicant.

    Class attributes:
        all_applicants (list): A list of all applicants, initialized as an empty list.
                               Used to store all the applicants. Once an applicant is accepted,
                               the applicant is removed from the list.
        lst_accepted (list): A list of all accepted applicants, initialized as an empty list.
                             Once an applicant is accepted, the applicant is added to the list.

    Instance attributes:
        first_name (str): The first name of the applicant.
        last_name (str): The last name of the applicant.
        scores (list): Scores for particular exams in order - physics, chemistry, math, computer science.
        departments (list): A list of departments the applicant is applying to.
        departments_scores (dict): A dictionary mapping departments to the applicant's scores.
        accepted_department (str): The department to which the applicant has been accepted.
    """
    all_applicants = []
    lst_accepted = []


    def __init__(self, first_name, last_name, scores, departments):
        self.finals_scores = None
        self.current_important_mean = None
        self.accepted_department = None

        self.first_name = first_name
        self.last_name = last_name
        self.departments = departments
        self.create_dict(scores)
        Applicant.all_applicants.append(self)


    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.current_important_mean}'


    def create_dict(self, scores):
        dictionary = {}
        exam = ['Physics', 'Chemistry', 'Math', 'Computer science', 'Additional exam']
        for i in range(5):
            dictionary[exam[i]]= scores[i]

        self.finals_scores = dictionary


class Department:
    """
    Department class is used to create an object representing a university department.

    Class attributes:
        all_departments (list): A list of all department instances, initialized as an empty list.

    Instance attributes:
        department_name (str): The name of the department.
        currently_accepting (int): The number of applicants the department is currently accepting.
        applicants (list): A list of applicants applying to the department in the current round.
        accepted_applicants (list): A list of applicants accepted by the department.

    Methods:
        __init__(department_name, number_of_accepting): Initializes the department with a name and the number of applicants it can accept.
        __str__(): Returns a string representation of the department and its accepted applicants.
        get_applicants(selection_round): Populates the list of applicants for the department based on the selection round.
        update_applicant_info(applicant): Updates the applicant's information upon acceptance.
        choose_applicants(): Selects and accepts applicants based on their scores and the department's capacity.
"""
    all_departments = []


    def __init__(self, department_name, number_of_accepting, type_of_exams):
        self.applicants = None
        self.accepted_applicants = []
        self.department_name = department_name
        self.bare_min_exams = type_of_exams
        self.currently_accepting = number_of_accepting

        Department.all_departments.append(self)


    def __str__(self):
        sep = '\n'
        return f'{sep.join(map(str, self.accepted_applicants))}\n'


    def calculate_mean_score(self, applicant):
        scores = []
        for exam in self.bare_min_exams:
            scores.append(applicant.finals_scores[exam])

        mean = round(sum(scores) / len(self.bare_min_exams), 2)

        if applicant.finals_scores['Additional exam'] > mean:
            return applicant.finals_scores['Additional exam']

        return mean


    def get_applicants(self, selection_round):
        self.applicants = []
        for applicant in Applicant.all_applicants:
            if list(applicant.departments)[selection_round] == self.department_name:
                self.applicants.append(applicant)
                applicant.current_important_mean = self.calculate_mean_score(applicant)


    def update_applicant_info(self, applicant):
        Applicant.lst_accepted.append(applicant)
        Applicant.all_applicants.remove(applicant)
        self.accepted_applicants.append(applicant)
        applicant.accepted_department = self.department_name


    def choose_applicants(self):
        func1 = lambda x: (-x.current_important_mean, x.first_name, x.last_name)
        self.applicants.sort(key=func1)

        for applicant in self.applicants:
            if not self.currently_accepting:
                break

            self.update_applicant_info(applicant)
            self.currently_accepting -= 1

        self.accepted_applicants.sort(key=func1)


def load_data():
    with open('applicants.txt', 'r') as file:
        for line in file:
            lst = line.strip().split(' ', 7)
            Applicant(lst[0], lst[1], [float(val) for val in lst[2:7]], lst[-1].split(' '))



def main():
    number_of_accepting = int(input())
    load_data()

    Department(department_name='Biotech', number_of_accepting=number_of_accepting, type_of_exams=['Chemistry', 'Physics'])
    Department(department_name='Chemistry', number_of_accepting=number_of_accepting, type_of_exams=['Chemistry'])
    Department(department_name='Engineering', number_of_accepting=number_of_accepting, type_of_exams=['Math', 'Computer science'])
    Department(department_name='Mathematics', number_of_accepting=number_of_accepting, type_of_exams=['Math'])
    Department(department_name='Physics', number_of_accepting=number_of_accepting, type_of_exams=['Math', 'Physics'])

    for i in range(3):
        for department in Department.all_departments:
            department.get_applicants(i)
            department.choose_applicants()

    for department in Department.all_departments:
        with open(f'{department.department_name.lower()}.txt', 'w') as file:
            file.write(str(department))

if __name__ == '__main__':
    main()
