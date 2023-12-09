from Tdrn.creat import Creat


class Tdrn_(Creat):

    def __init__(self):
        ...

    @property
    def Log(self) -> list:
        '''
        get log's content
        '''
        '''
        file_path = "C:/Code/Tdrb/trnd.txt"
        if os.path.isfile(file_path):
            return self.log
        else:
            raise FileNotFoundError("file not found")
        '''
        return self.log
        
    
    @Log.setter
    def Log(self,content:list[str]):
        '''
        set log's content
        '''
        self.log=content
        
    
    @Log.deleter
    def Log(self):
        '''
        Delete to-do list
        '''
        del self.log

    def write(self,log:list[str]):
        with open('tdrn.txt','a',encoding='utf-8') as file:
            for index,content in enumerate(log):
                content_=""
                content_+=f"{index+1}.{content}\n"
                file.write(content_)
        with open('ttrn.txt','a',encoding='utf-8') as file:
                file.write("=========================================")