from sql_handle import sql_handler
import configuration as conf
import page_handle.entrance
import page_handle.story
import threading

url = conf.url
headers = conf.headers

def update_progress(progress: int, total: int):
    print(f'Progress: {progress}/{total}', end='\r')

def wait_threads(threads: list[threading.Thread]):
    for index, thread in enumerate(threads, start=1):
        thread.join()
        update_progress(progress=index, total=len(threads))

def sql_to_file():
    sql = sql_handler()
    sql.to_file('~/SQL/Crawler3/Stories/')

def main():
    # 初始化 SQL 資料庫
    sql_handler.initialize()   

    url = f'{conf.url}/books/329828.html'
    entrance_handler = page_handle.entrance.handler(url)
    entrances = entrance_handler.get_entrances()

    threads = []
    request_semaphore = threading.Semaphore(20)
    sql_lock = threading.Lock()
    for entrance in entrances:
        story_handler = page_handle.story.handler(entrance.page_number, entrance.url)
        thread = threading.Thread(target=story_handler.get_content, args=(request_semaphore, sql_lock))
        thread.start()
        threads.append(thread)
        update_progress(progress=len(threads), total=len(entrances))
    
    wait_threads(threads)

if __name__ == '__main__':
    main()
    sql_to_file()