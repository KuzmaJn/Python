from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    leitner_box = Column(Integer)

    def __repr__(self):
        return f'Flashcard id: {self.id}, Question: {self.question}, Answer: {self.answer}, Box: {self.leitner_box}'

    def show_question(self):
        return self.question

    def show_answer(self):
        return self.answer


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def learning_menu(session, flashcard):
    loop_check = 1
    while loop_check:
        print('press "y" if your answer is correct:')
        print('press "n" if your answer is wrong:')
        choice = input()
        if choice == 'y':
            if flashcard.leitner_box >= 3:
                session.delete(flashcard)
            else:
                flashcard.leitner_box += 1
            loop_check = 0
        elif choice == 'n':
            flashcard.leitner_box = 1
            loop_check = 0
        else:
            print(f'{choice} is not an option')


def update_menu(session, flashcard):
    loop_check = 1
    while loop_check:
        print('press "d" to delete the flashcard:')
        print('press "e" to edit the flashcard:')
        choice = input()

        if choice == 'd':
            session.delete(flashcard)
            loop_check = 0
        elif choice == 'e':
            print(f'current question: {flashcard.question}')
            question = input('please write a new question:\n')
            print(f'current answer: {flashcard.answer}')
            answer = input('please write a new answer:\n')
            if question.strip() != '':
                flashcard.question = question
            if answer.strip() != '':
                flashcard.answer = answer

            loop_check = 0
        else:
            print(f'{choice} is not an option')


def add_flashcard():
    question = input('Question:\n')
    while not question.strip():
        question = input('Question:\n')

    answer = input('Answer:\n')
    while not answer.strip():
        answer = input('Answer:\n')

    with Session() as session:
        card = Flashcard(question=question, answer=answer, leitner_box=1)
        session.add(card)
        session.commit()


def practice_menu():
    with Session() as session:
        flashcards = session.query(Flashcard).all()
        
        if len(flashcards) == 0:
            print('There is no flashcard to practice!')
            return

        for flashcard in flashcards:
            print(f'Question: {flashcard.question}')
            loop_check = 1
            while loop_check:
                print('press "y" to see the answer:')
                print('press "n" to skip:')
                print('press "u" to update:')

                option = input()
                if option == 'y':
                    print(f'Answer: {flashcard.answer}')
                    learning_menu(session, flashcard)
                    loop_check = 0
                elif option == 'n':
                    loop_check = 0
                elif option == 'u':
                    update_menu(session, flashcard)
                    loop_check = 0
                else:
                    print(f'{option} is not an option')

                session.commit()


def creator_menu():
    print('1. Add a new flashcard')
    print('2. Exit')

    choice = input()

    if choice == '1':
        add_flashcard()
        return 1
    elif choice == '2':
        return 0
    else:
        print(f'{choice} is not an option')
        return 1


def main_menu():
    print('1. Add flashcards')
    print('2. Practice flashcards')
    print('3. Exit')

    choice = input()

    if choice == '1':
        while creator_menu():
            pass

        return 1
    elif choice == '2':
        practice_menu()
        return 1
    elif choice == '3':
        print('Bye!')
        return 0
    else:
        print(f'{choice} is not an option')
        return 1


def main():
    while main_menu():
        pass
    return 0

if __name__ == '__main__':
    main()