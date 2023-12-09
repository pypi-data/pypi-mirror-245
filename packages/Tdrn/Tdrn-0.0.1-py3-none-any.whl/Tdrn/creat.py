import datetime

'''
creat an To-do record notbook(creat date)
'''
class Creat():
    def __init__(self):
        self.log:list[str]

    def __str__(self,obj:object) -> str:
        return str(obj)

    def creat_txt(self):
        '''
        Shows the time the archive was created
        '''
        with open('tdrn.txt','w',encoding='utf-8') as file:
            now = datetime.datetime.now()
            delta = now.strftime(f'創建時間:%m/%d %H:%M')
            print(delta)
            file.write(f"於{delta}創建文件\n")
            
    def creat_date(self,year:int,month:int,day:int,hour:int,minute:int,second:int):
        '''
        Custom date
        '''
        with open('tdrn.txt','a',encoding='utf-8') as file:
                delta=datetime.datetime.fromisoformat(f'{year}-{month}-{day} {hour}:{minute}:{second}')
                delta=delta.strftime('%m/%d %H:%M分')
                file.write(f"{delta}"+'\n')

    def creat_time(self,hour:int,minute:int):
        '''
        Custom time
        '''
        with open('tdrn.txt','a',encoding='utf-8') as file:
                delta=datetime.datetime.strptime(f'{hour}:{minute}','%H:%M')
                file.write(f"{delta.hour}:{delta.minute}分"+'\n')