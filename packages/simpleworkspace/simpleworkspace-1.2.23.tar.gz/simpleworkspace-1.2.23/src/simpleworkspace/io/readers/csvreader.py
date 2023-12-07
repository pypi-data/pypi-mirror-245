import csv
from typing import TypeVar as _TypeVar, Generic as _Generic, MutableSequence as _MutableSequence

_T = _TypeVar('_T')

class CSVReader(_Generic[_T]):
    '''
    Simple csv reader and writer wrapper class. The class can also be used to create new csv files.

    Properties for the user:
    * self.Delimiter: The delimiter to be used when loading or exporting a csv file. It is specified in the constructor but can be freely changed.
    * self.Rows     : A 2D list of csv rows in the format Rows[row][col]. It can be manipulated to alter the exported csv file on Save().
    * self.Headers  : A list of column names that must match the column count on the rest of csv rows.
                      When headers is None or an empty list, the exported csv file will not include a header row.
    '''

    def __init__(self, delimiter:str=',') -> None:
        self.Delimiter = delimiter
        '''The delimiter character to use'''
        self.Headers:list[str] = []
        '''list of column names aka headers'''
        self.Rows = []
        return
    

    @property
    def Rows(self) -> _T|'_RowList[_ColumnList[str]]':
        '''contains the a 2D list of data rows, self.Rows[row][col]'''
        return self._rows

    @Rows.setter
    def Rows(self, new_value):
        if not isinstance(new_value, (list, tuple)):
            raise ValueError("RowList must be of type iterable (list/tuple)")
        self._rows = self._RowList(self, new_value)


    class _RowList(_MutableSequence[_T], _Generic[_T]):
        def __init__(self, context: 'CSVReader', items: 'list[CSVReader._ColumnList]' = []):
            self._context = context
            self._list = [self._AsRow(item) for item in items]

        def _AsRow(self, value):
            if not isinstance(value, (list, tuple)):
                raise ValueError("RowList can only contain iterables of type list or tuple")
            return CSVReader._ColumnList(self._context, value)

        def __getitem__(self, index):
            return self._list[index]

        def __setitem__(self, index, value):
            self._list[index] = self._AsRow(value)

        def __delitem__(self, index):
            del self._list[index]

        def insert(self, index, value):
            self._list.insert(index, self._AsRow(value))

        def __len__(self):
            return len(self._list)

        def __repr__(self):
            return self._list.__repr__()
        
        def __eq__(self, other):
            if isinstance(other, CSVReader._RowList):
                return self._list == other._list
            if isinstance(other, list):
                return self._list == other
            return False

        
    class _ColumnList(_MutableSequence[_T], _Generic[_T]):
            def __init__(self, context: 'CSVReader', items:list[str] = []):
                self._context = context
                self._list = list(items)

            def _ResolveIndex(self, index:str|int):
                if isinstance(index, int):
                    return index
                
                # If the key is a string, try to find the index by item name
                if not(self._context.Headers):
                    raise LookupError("No headers attached in csv document")
                try:
                    return self._context.Headers.index(index)
                except ValueError:
                    raise KeyError(f"Invalid Column Name '{index}'")
                
            def __getitem__(self, index:int|str):
                index = self._ResolveIndex(index)
                return self._list[index]

            def __getattr__(self, __name: str):
                index = self._ResolveIndex(__name)
                return self._list[index]

            def __setitem__(self, index, value):
                index = self._ResolveIndex(index)
                self._list[index] = value
            
            def __delitem__(self, index):
                index = self._ResolveIndex(index)
                del self._list[index]

            def insert(self, index, value):
                index = self._ResolveIndex(index)
                self._list.insert(index, value)

            def __len__(self):
                return len(self._list)
            
            def __repr__(self) -> str:
                return self._list.__repr__()
            
            def __eq__(self, other):
                if isinstance(other, CSVReader._ColumnList):
                    return self._list == other._list
                if isinstance(other, list):
                    return self._list == other
                return False


    def GetValuesByColumnName(self, columnName:str):
        '''
        Retrieves list of values under a specific column/header name. 

        :param columnName: The columnName to get values of, is case insensitive.
        :raises LookupError: If headers are not mapped or loaded, exception will be thrown
        :return: list of string values as an LINQ iterator for matched column name, otherwise None.
        '''
        from simpleworkspace.utility.linq import LINQ

        if not (self.Headers):
            raise LookupError("No headers attached in csv document")
        
        columnName = columnName.lower()
        for index, headerName in enumerate(self.Headers):
            if(headerName.lower() == columnName):
                return LINQ(self.Rows).Select(lambda row: row[index])
        return None

    def Load(self, filepath:str, hasHeader=True):
        '''Imports a csv instance from a file'''

        self.Rows = []
        self.Headers = []
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.Delimiter)
            if(hasHeader):
                self.Headers = next(reader)
            self.Rows = [row for row in reader]
        return
    
    def Save(self, filepath:str):
        '''Exports the csv instance out to a filepath'''

        with open(filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=self.Delimiter)
            if(self.Headers):
                csv_writer.writerow(self.Headers)
            csv_writer.writerows(self.Rows)
        pass
    