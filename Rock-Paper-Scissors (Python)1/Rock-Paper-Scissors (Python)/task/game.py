from random import randint


def greet_user():
    user_name = input("Enter your name: ")
    print("Hello,", user_name)
    return user_name


def get_options():
    opt = input()

    return opt.split(sep=',') if len(opt) > 2 else ["rock", "paper", "scissors"]


def read_file(file, user):
    players_dict = dict()

    #check if file is empty
    #if empty add current user to dictionary

    if not file.read(1):
        players_dict[user] = 0

    #if not empty copy players as keys and score as values
    else:
        file.seek(0)
        for line in file:
            lst = line.strip().split()
            players_dict[lst[0]] = int(lst[1])

    #check if current user in dictionary (already played game)
    #and add user if not
        if user not in players_dict:
            players_dict[user] = 0

    return players_dict


def computer_ch(options):
    com_choice = options[randint(0, len(options) - 1)]
    return com_choice


def evaluate(user, computer, options):
    pos = options.index(user)
    win_opt = options[pos:] + options[:pos]
    win_opt.pop(0)
    half = len(win_opt) // 2

    if user == computer:
        print(f"There is a draw ({computer})")
        return 50
    elif computer in win_opt[half:]:
        print(f"Well done. The computer chose {computer} and failed")
        return 100
    else:
        print(f"Sorry, but the computer chose {computer}")
        return 0


def write_file(file, players):
    file.truncate()
    for player in players:
        print(player, players[player], file=file, flush=True)


def game(file):
    current_user = greet_user()
    options = get_options()                  #options so program can check valid input
    all_players = read_file(file, current_user)
    print("Okay, let's start")

    #game loop starts here
    user_input = input()
    while user_input != "!exit":
        if user_input == '!rating':
            print(all_players[current_user])
        elif user_input not in options:
            print("Invalid input")
        else:
            computer_choice = computer_ch(options)
            all_players[current_user] += evaluate(user_input, computer_choice, options)
        user_input = input()

    else:
        write_file(file, all_players)
        print("Bye!")


def main():
    try:
        file_rating = open("rating.txt", "r+")
    except FileNotFoundError:
        # doesn’t exist
        new_file = open("rating.txt", "w")
        new_file.close()
        file_rating = open("rating.txt", "r+")

    game(file_rating)
    file_rating.close()


if __name__ == '__main__':
    main()
