from tpltable.utils import *
class TableIO:  # Used for typing
    ...
class TableIO:
    """
    本质上是一个巨大的sheet容器，每个sheet都是一个openpyxl.Worksheet对象
    """
    _aSOURCEKEY = '_tpltable_sheetsource'
    _id = 0
    def __init__(self, name:str = None):
        if name is None:
            self.name = f"t{TableIO._id}"
            TableIO._id += 1
        self._source_sheets = {}  # {source: [sheet1, sheet2, ...]}

        # readonly(Write only in append method)
        self._sheets = []

    @property
    def sheets(self):
        return self._sheets

    @staticmethod
    def _mark_source(source: str, *sheets, force=False):
        for _sheet in sheets:
            _aSOURCE = getattr(_sheet, TableIO._aSOURCEKEY, None)
            if force or _aSOURCE is None:
                setattr(_sheet, TableIO._aSOURCEKEY, source)


    def append(self, target: Union[TableIO, Worksheet, Workbook, str]):
        """
        将target中的所有sheet追加到self中
        :param target:
        :return:
        """
        _new_sheets = {}
        if isinstance(target, TableIO):
            _list = target.sheets
            self._mark_source(target.name, *_list, force=True)
            _new_sheets[target.name] = _list
        elif isinstance(target, Workbook):
            _list = target.worksheets
            self._mark_source(get_book_name(target), *_list)
            _new_sheets[get_book_name(target)] = _list
        elif isinstance(target, Worksheet):
            _list = [target]
            self._mark_source(get_book_name(target.parent), *_list)
            _new_sheets[get_book_name(target.parent)] = _list
        elif isinstance(target, str):
            target = load_workbook(target)
            _list = target.worksheets
            self._mark_source(get_book_name(target), *_list)
            _new_sheets[get_book_name(target)] = _list
        else:
            raise TypeError(f"Unsupported type: {type(target)}")

        # check new sheets
        for _sheet in _list:
            if not isinstance(_sheet, Worksheet):
                raise TypeError(f"Unsupported type: {type(_sheet)}")
            # if getattr(_sheet, TableIO._aSOURCEKEY, None) is not None:
            #     raise ValueError(f"Sheet {_sheet} has been appended to another TableIO object.")

        self._source_sheets.update(_new_sheets)

        self._sheets.clear()
        for _sheets in self._source_sheets.values():
            self._sheets.extend(_sheets)

    def extend(self, targets):
        """
        将targets中的所有sheet追加到self中
        :param targets: array of <TableIO, Workbook, Worksheet, str>
        :return:
        """
        for _target in targets:
            self.append(_target)

    def __len__(self):
        return len(self.sheets)

    def __getitem__(self, item):
        return self.sheets[item]

    def __iter__(self):
        return iter(self.sheets)

    def __repr__(self):
        return f"<TableIO: {self.name}>"

    def __str__(self):
        _txt = ""
        for k, v in self._source_sheets.items():
            _txt += f"{k}: {len(v)}, "
        if _txt:
            _txt = _txt[:-2]
        return f"TableIO: {self.name} <count: {len(self.sheets)}" + (f", source: [{_txt}]>" if _txt else ">")



if __name__ == '__main__':
    t = TableIO()
    print(t)
    t.extend(['tpl.xlsx', 'res.xlsx', 'data.xlsx'])
    print(t)

