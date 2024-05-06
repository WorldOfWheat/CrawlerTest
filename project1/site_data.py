class q_and_a:
    def __init__(self, 
                question: str, 
                answer: str
            ) -> None:
        self.question = question
        self.answer = answer

class section:
    def __init__(self, 
                id: str,
                link: str,
                print_name: str = None,
                database_link: str = None
            ) -> None:
        self.id = id
        self.link = link
        self.print_name = print_name
        self.database_link = database_link

class department:
    def __init__(self, 
                name: str, 
                print_name: str = None,
                sections: list[section] = None
            ) -> None:
        self.name = name
        self.print_name = print_name
        if (sections == None):
            self.sections = []
        else:
            self.sections = sections 