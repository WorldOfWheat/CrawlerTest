class teacher:
    def __init__(self, 
                name: str, 
            ) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return self.name

class subject_time:
    def __init__(self,
                times: list[dict], # {day: int, section: int}
            ):

        for time in times:
            day = time['day']
            section = time['section']
            # 星期幾初始化
            if (day < 1 or day > 7):
                raise ValueError('day should be in 1-7')
            # 節次初始化
            if (section < 1 or section > 14):
                raise ValueError('section should be in 1-14')
        
        self.times = times

# 科目
class subject:
    def __init__(self,
                print_name: str,
                class_room_id: str,
                teacher: teacher,
                time: subject_time,
            ):
            self.print_name = print_name
            self.class_room_id = class_room_id
            self.teacher = teacher
            self.time = time