import prompt


def welcome():
    text_help = ("<command> exit "
                 "- выйти из программы\n<command> help - справочная информация")
    print("\nПервая попытка запустить проект!\n\n***\n" + text_help)
    while True:
        command = prompt.string("Введите команду: ")
        match command:
            case "help":
                print("\n\n" + text_help)
            case "exit":
                return