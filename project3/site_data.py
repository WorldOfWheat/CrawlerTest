import sql_handle

class page:
    def __init__(self, 
                page_number: int, 
                content: str,
            ) -> None:
        self.page_number = page_number
        self.content = content
        self.sql_handler = sql_handle.sql_handler()
    
    def save_to_sql(self) -> None:
        self.sql_handler.add_page(self)

class entrance:
    def __init__(self,
    			page_number: int,
                url: str,
            ) -> None:
        self.page_number = page_number
        self.url = url
    
    def __str__(self) -> str:
        return f'page_number: {self.page_number}, url: {self.url}'