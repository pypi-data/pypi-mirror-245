from abc import ABC
from datetime import datetime
from simpleworkspace.types.time import TimeSpan
from datetime import datetime, timedelta

class ITask(ABC):
    '''
    Tasks needs to implement this interface to be loaded into task scheduler

    properties and methods for Derived classes:
        * task_interval
        * task_ignore
        * task_description
        * On_StartUp
        * On_Schedule 
    '''
    task_interval:TimeSpan = None
    '''Runs On_Schedule event per specified interval, example: TimeSpan(minute=2), would run the task once ever 2 minutes'''
    task_ignore = False
    '''Can ignore a task from being picked up'''
    task_description = None

    _cache_lastRunDate: datetime = None
    _task_id: str
    _HasEvent_StartUp: bool
    _HasEvent_Schedule: bool
    '''An unique identifier for this task, is used to store persistant task states and for lookups'''
    

    def On_StartUp(self) -> str|None:
        '''runs once per start of taskscheduler'''

    def On_Schedule(self) -> str|None:
        '''runs once per specified interval'''

    def NextSchedule(self, previousRunDate: datetime|None) -> bool:
        if(previousRunDate is None):
            return True
        nextRunDate = previousRunDate + timedelta(seconds=self.task_interval.InSeconds())
        if(datetime.now() > nextRunDate):
            return True
        return False
    
    def __new__(cls, *args, **kwargs):
        '''Gives possibility to ensure logic always run even if __init__ is left out. __init__ runs after this method has ran to completion'''
        instance = super().__new__(cls)
        instance._task_id = cls.__module__ + "." + cls.__name__

        instance._HasEvent_StartUp = True
        if(instance.On_StartUp.__func__ is ITask.On_StartUp): #startup function is not implemented
            instance._HasEvent_StartUp = False
        
        instance._HasEvent_Schedule = True
        if(instance.task_interval is None) and (instance.NextSchedule.__func__ is ITask.NextSchedule): # no scheduler used, therefore would never be triggered
            instance._HasEvent_Schedule = False
        if(instance.On_Schedule.__func__ is ITask.On_Schedule): #schedule function is not implemented, therefore no actions to perform
            instance._HasEvent_Schedule = False
            
        return instance
    

class CommandTask(ITask):
    '''Premade task for running a simple command'''
    def __init__(self, interval:TimeSpan, command:str|list[str]) -> None:
        from hashlib import md5
        import shlex

        super().__init__()

        self.task_interval = interval
        if isinstance(command, str):
            command = shlex.split(command)
        self.command = command
        commandStringRepresentation = ' '.join(command)
        self.task_description = commandStringRepresentation
        self._task_id = md5(commandStringRepresentation.encode()).hexdigest()[:16]

    
    def On_Schedule(self):
        import subprocess
        result = subprocess.run(self.command, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        message = ""
        if(result.returncode != 0): #something went bad
            stderr = result.stderr if result.stderr is not None else ""
            message += f"STDERR[{result.returncode}]: {stderr};"
        
        if(result.stdout):
            message += f"STDOUT: {result.stdout.rstrip()};"

        return message
