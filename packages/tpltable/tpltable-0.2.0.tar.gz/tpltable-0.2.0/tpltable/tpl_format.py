from tpltable.utils import *


# error：不能对齐
class NotAlignError(Exception):
    pass


class TplFormat:
    """
    tpltable所使用的模板格式，总体来说为一个dict，其中:
        key为str，形如$XXX,
        value为box4

    """

    def __init__(self):
        self._tpl = {}  # 目标模板  # "$XXX": Box4  # 相对位置
        self._valid = {}  # 验证数据  # 模板中非$开头的数据，用于验证模板是否正确  # Vec4: value  # 相对位置
        self._merge = []  # 合并单元格  # 模板中的合并单元格, 用于验证模板是否正确  # Vec4  # 相对位置
        self._roi = None  # 相对位置

        self.__roi = None  # 绝对位置
        self._sheet = None  # 用于获取其style等信息

    def __len__(self):
        if not self._roi:
            return 0
        return self._roi.h * self._roi.w

    @property
    def tpl(self):
        return copy.copy(self._tpl)

    @property
    def roi(self):
        return copy.copy(self.__roi)

    def parse(self, sheet, roi: Vec4 = None) -> bool:
        """
        从sheet中解析模板
        :param sheet: openpyxl Worksheet object
        :param roi: Vec4 object. 用于指定解析的区域. 默认为None，表示解析整个sheet
        :return: bool. True表示解析成功，False表示解析失败
        """
        _tpl, _val = {}, {}
        if roi is None:
            max_row, max_column = sheet_sizeof(sheet)
            roi = Vec4.from_range4([1, 1, max_column, max_row])
        offset = (roi.x, roi.y)
        for ih in range(roi.h):
            for iw in range(roi.w):
                cell = sheet.cell(row=roi.row + ih + offset[1], column=roi.col + iw + offset[0])
                if cell.value is None:
                    continue
                if not isinstance(cell.value, str):
                    continue
                if cell.value.startswith('$'):
                    _tpl[cell.value] = Box4(ih, iw, 0, 0)
                else:
                    _val[Vec4(ih, iw, 0, 0)] = cell.value

        # 记录位于roi范围内的合并单元格
        _merge = []
        for merge in sheet.merged_cells:
            if merge.min_row < offset[1] or merge.min_col < offset[0]:
                continue
            if merge.max_row > offset[1] + roi.h or merge.max_col > offset[0] + roi.w:
                continue
            _merge.append(
                Vec4(
                    merge.min_row - offset[1] - 1,
                    merge.min_col - offset[0] - 1,
                    merge.max_row - merge.min_row + 1,
                    merge.max_col - merge.min_col + 1
                )
            )

        # replace
        self._tpl = _tpl
        self._valid = _val
        self._merge = _merge
        self._sheet = sheet
        # 平移roi到 0，0
        self.__roi = roi
        self._roi = Vec4(0, 0, roi.h, roi.w)

        return True

    @staticmethod
    def from_sheet(sheet, roi: Vec4 = None):
        """
        从sheet中解析模板
        :param sheet: openpyxl Worksheet object
        :param roi: Vec4 object. 用于指定解析的区域. 默认为None，表示解析整个sheet
        :return: TplFormat object
        """
        _ = TplFormat()
        _.parse(sheet, roi)
        return _

    @staticmethod
    def from_book(book:Union[Workbook, str], roi: Vec4 = None):
        """
        从book中解析模板
        :param book: openpyxl Workbook object or str. 只会使用其active sheet
        :param roi: Vec4 object. 用于指定解析的区域. 默认为None，表示解析整个sheet
        :return: TplFormat object
        """
        if isinstance(book, str):
            book = load_workbook(book)
        return TplFormat.from_sheet(book.active, roi)

    def validate(self, sheet, offset: tuple = (0, 0), internal: tuple = (0, 0), tolerence: float = 0.01) -> np.ndarray:
        """
        ndarray with shape(ah, aw)，each element is a bool
        其中ah aw是模板所能匹配到的形状, ah aw对应的每个元素是每个位置的模板所匹配到的数据。
        * 如果sheet的尺寸不是模板的整数倍，则会抛出NotAlignError
        :param sheet: openpyxl Worksheet object
        :param offset: tuple. 模板匹配的起始位置
        :param internal: tuple. x或y方向上连续的两个模板之间的间隔
        for a row, it contains n tpl:
            o[0] + tpl0 + i[0] + tpl1 + i[0] + tpl2 + i[0] + ... + tpln + i[0] + tpln+1
        :param tolerence: float. 用于验证模板的容忍度，即模板中的数据与实际数据的差异在一定百分比范围内是可以接受的. 0.01表示1%
        :return: np.ndarray with shape(ah, aw)，each element is a bool
        """
        if self._roi is None:
            log.error(ValueError, 'roi is None. please parse first.', exit=True)

        max_row, max_col = sheet_sizeof(sheet)

        # check align
        if (max_row - offset[1] + internal[1]) % self._roi.h != 0:
            raise NotAlignError(
                'row not align.\n sheet.max_row: {}\n offset[1]: {}\n internal[1]: {}\n roi.h: {}'.format(max_row, offset[1], internal[1],
                                                                                                          self._roi.h))
        if (max_col - offset[0] + internal[0]) % self._roi.w != 0:
            raise NotAlignError(
                'column not align.\n sheet.max_column: {}\n offset[0]: {}\n internal[0]: {}\n roi.w: {}'.format(max_col, offset[0],
                                                                                                                internal[0], self._roi.w))

        # get shape
        ah = (max_row - offset[1] + internal[1]) // self._roi.h
        aw = (max_col - offset[0] + internal[0]) // self._roi.w
        arr = np.ndarray(shape=(ah, aw), dtype=bool)

        # create sheet.merges' range4 list
        _range4 = []
        for merge in sheet.merged_cells:
            _range4.append(merge.bounds)

        for ih in range(ah):
            for iw in range(aw):
                flag = True
                starts = (offset[0] + iw * (self._roi.w + internal[0]), offset[1] + ih * (self._roi.h + internal[1]))

                ## validate merge
                for vec4 in self._merge:
                    # add bias
                    vec4 = vec4.move(*starts)
                    # check
                    r4 = vec4.range4
                    if tuple(r4) not in _range4:
                        flag = False
                        break

                if not flag:
                    arr[ih, iw] = False
                    continue

                ## validate valid
                _count = 0
                for vec4, value in self._valid.items():
                    # add bias
                    vec4 = vec4.move(*starts)
                    # check
                    cell = sheet.cell(row=vec4.row + starts[1], column=vec4.col + starts[0])
                    if cell.value != value:
                        _count += 1  # 这个不匹配在一定范围内是可以接受的
                if _count > len(self) * tolerence:
                    arr[ih, iw] = False
                    continue

        return arr

    def match(self, sheet, offset: tuple = (0, 0), internal: tuple = (0, 0)) -> np.ndarray:
        """
        ndarray with shape(ah, aw)，each element is a tpl-format-dict
        其中ah aw是模板所能匹配到的形状, ah aw对应的每个元素是每个位置的模板所匹配到的数据。
        * 如果sheet的尺寸不是模板的整数倍，则会抛出NotAlignError
        :param sheet: openpyxl Worksheet object
        :param offset: tuple. 模板匹配的起始位置
        :param internal: tuple. x或y方向上连续的两个模板之间的间隔
        for a row, it contains n tpl:
            o[0] + tpl0 + i[0] + tpl1 + i[0] + tpl2 + i[0] + ... + tpln + i[0] + tpln+1
        :return:
        """
        if self._roi is None:
            log.error(ValueError, 'roi is None. please parse first.', exit=True)

        max_row, max_col = sheet_sizeof(sheet)

        # check align
        if (max_row - offset[1] + internal[1]) % self._roi.h != 0:
            raise NotAlignError(
                'row not align.\n sheet.max_row: {}\n offset[1]: {}\n internal[1]: {}\n roi.h: {}'.format(max_row, offset[1], internal[1],
                                                                                                          self._roi.h))
        if (max_col - offset[0] + internal[0]) % self._roi.w != 0:
            raise NotAlignError(
                'column not align.\n sheet.max_column: {}\n offset[0]: {}\n internal[0]: {}\n roi.w: {}'.format(max_col, offset[0],
                                                                                                                internal[0], self._roi.w))

        # get shape
        ah = (max_row - offset[1] + internal[1]) // self._roi.h
        aw = (max_col - offset[0] + internal[0]) // self._roi.w
        arr = np.ndarray(shape=(ah, aw), dtype=object)
        for ih in range(ah):
            for iw in range(aw):
                starts = (offset[0] + iw * (self._roi.w + internal[0]), offset[1] + ih * (self._roi.h + internal[1]))
                _ = copy.deepcopy(self._tpl)
                for key, box in _.items():
                    # locate cell
                    cell = sheet.cell(row=box.row + starts[1], column=box.col + starts[0])
                    # set value
                    v = cell.value
                    _[key] = '' if v is None else str(v)
                arr[ih, iw] = _

        return arr

    def format(self, ndarr_dict: np.ndarray, internal: tuple = (0, 0)) -> Worksheet:
        """
        根据ndarr_dict中的数据，生成一个新的sheet
        :param ndarr_dict: np.ndarray with shape(ah, aw)，each element is a tpl-format-dict
        * offset: tuple. 模板匹配的起始位置 -- 该参数由self.roi确定. 不再接受该参数
        :param internal: tuple. x或y方向上连续的两个模板之间的间隔
        :return:
        """
        if self._roi is None:
            log.error(ValueError, 'roi is None. please parse first.', exit=True)

        # create new sheet
        sheet = Workbook().active

        # check
        check_ndarr_dict(ndarr_dict, False, True)

        # get shape
        ah, aw = ndarr_dict.shape

        # copy area below offset (2 times: horizontal and vertical)
        offset = self.__roi.xy  # tuple
        # horizental
        for iw in range(aw):
            start = offset[0] + iw * (self._roi.w + internal[0])
            copy_area(self._sheet, sheet, Vec4(0, 0, offset[1], self._roi.w), Vec4(0, start, offset[1], self._roi.w))
        # vertical
        for ih in range(ah):
            start = offset[1] + ih * (self._roi.h + internal[1])
            copy_area(self._sheet, sheet, Vec4(0, 0, self._roi.h, offset[0]), Vec4(start, 0, self._roi.h, offset[0]))

        # fill each template
        for ih in range(ah):
            for iw in range(aw):
                _dict = ndarr_dict[ih, iw]
                starts = (offset[0] + iw * (self._roi.w + internal[0]), offset[1] + ih * (self._roi.h + internal[1]))
                # 先拷贝一份作为基础
                copy_area(self._sheet, sheet, self.__roi, Vec4(starts[1], starts[0], self._roi.h, self._roi.w))
                # 填充其中以$开头的单元格
                for delta_ih in range(self._roi.h):
                    for delta_ix in range(self._roi.w):
                        cell = sheet.cell(row=starts[1] + delta_ih + 1, column=starts[0] + delta_ix + 1)
                        if cell.value is None:
                            continue
                        if not isinstance(cell.value, str):
                            continue
                        if cell.value.startswith('$'):
                            if cell.value not in _dict:
                                log.warn('ndarr_dict[{}, {}] has no key {}'.format(ih, iw, cell.value))
                                continue
                            cell.value = _dict[cell.value]

                # merge
                for vec4 in self._merge:
                    # add bias
                    vec4 = vec4.move(*starts)
                    # merge
                    sheet.merge_cells(vec4.letter)

        return sheet


__doc__ = """
    TplFormat
        parse(sheet, roi=None) -> bool
        '''
        从sheet中解析模板
        :param sheet: openpyxl Worksheet object
        :param roi: Vec4 object. 用于指定解析的区域. 默认为None，表示解析整个sheet
        :return: bool. True表示解析成功，False表示解析失败
        '''
        @staticmethod
        from_sheet(sheet, roi=None) -> TplFormat
        '''
        从sheet中解析模板
        :param sheet: openpyxl Worksheet object
        :param roi: Vec4 object. 用于指定解析的区域. 默认为None，表示解析整个sheet
        :return: TplFormat object
        '''
        validate(sheet, offset=(0, 0), internal=(0, 0), tolerence=0.01) -> np.ndarray
        '''
        ndarray with shape(ah, aw)，each element is a bool
        其中ah aw是模板所能匹配到的形状, ah aw对应的每个元素是每个位置的模板所匹配到的数据。
        * 如果sheet的尺寸不是模板的整数倍，则会抛出NotAlignError
        :param sheet: openpyxl Worksheet object
        :param offset: tuple. 模板匹配的起始位置
        :param internal: tuple. x或y方向上连续的两个模板之间的间隔
        for a row, it contains n tpl:
            o[0] + tpl0 + i[0] + tpl1 + i[0] + tpl2 + i[0] + ... + tpln + i[0] + tpln+1
        :param tolerence: float. 用于验证模板的容忍度，即模板中的数据与实际数据的差异在一定百分比范围内是可以接受的. 0.01表示1%
        :return: np.ndarray with shape(ah, aw)，each element is a bool
        '''
        match(sheet, offset=(0, 0), internal=(0, 0)) -> np.ndarray
        '''
        ndarray with shape(ah, aw)，each element is a tpl-format-dict
        其中ah aw是模板所能匹配到的形状, ah aw对应的每个元素是每个位置的模板所匹配到的数据。
        * 如果sheet的尺寸不是模板的整数倍，则会抛出NotAlignError
        :param sheet: openpyxl Worksheet object
        :param offset: tuple. 模板匹配的起始位置
        :param internal: tuple. x或y方向上连续的两个模板之间的间隔
        for a row, it contains n tpl:
            o[0] + tpl0 + i[0] + tpl1 + i[0] + tpl2 + i[0] + ... + tpln + i[0] + tpln+1
        :return:
        '''
        format(ndarr_dict, internal=(0, 0)) -> Worksheet
        '''
        根据ndarr_dict中的数据，生成一个新的sheet
        :param ndarr_dict: np.ndarray with shape(ah, aw)，each element is a tpl-format-dict
        * offset: tuple. 模板匹配的起始位置 -- 该参数由self.roi确定. 不再接受该参数
        :param internal: tuple. x或y方向上连续的两个模板之间的间隔
        :return:
        '''
"""


if __name__ == '__main__':
    tpl_excel: Workbook = load_workbook('tpl.xlsx')
    data_excel: Workbook = load_workbook('data.xlsx')

    tpl = TplFormat.from_sheet(tpl_excel.active)

    _ = []
    # tar = data_excel.active
    for i, tar in enumerate(data_excel.worksheets):
        # validate
        print(tpl.validate(tar))

        # match
        _data = tpl.match(tar)
        print(_data)
        _.append(_data[0, 0])

        # format&save
        # _sheet = tpl.format(_data)
        # _sheet.parent.save(f'res_{i}.xlsx')

    _ = np.array(_).reshape((len(_), 1))
    _sheet = tpl.format(_, internal=(1, 1))
    _sheet.parent.save(f'res.xlsx')