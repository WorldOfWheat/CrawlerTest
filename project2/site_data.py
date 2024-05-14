class teacher:
    def __init__(self, 
                name: str, 
            ) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return self.name

class subject_time:
    def __init__(self):
        self.__day = -1
        self.__sections = []

    def set_day(self, day: int):
        if (self.__day != -1):
            raise ValueError('day should not be set again')
        if (day < 1 or day > 7):
            raise ValueError('day should be in 1-7')
        
        self.__day = day
    
    def get_day(self) -> int:
        return self.__day

    def add_section(self, section: int):
        if (section < 1 or section > 14):
            raise ValueError('section should be in 1-14')
        
        self.__sections.append(section)
    
    def get_sections(self) -> list[int]:
        return self.__sections

# 科目
class subject:
    def __init__(self,
                id: str,
                subject_name: str,
                subject_eng_name: str,
                credit: int,
                teacher: teacher,
                required: bool,
                time: list[subject_time],
                room: str
            ):
            self.id = id
            self.subject_name = subject_name
            self.subject_eng_name = subject_eng_name
            self.credit = credit
            self.teacher = teacher
            self.required = required
            self.time = time
            self.room = room