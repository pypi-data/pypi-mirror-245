from tpltable.tpl_format import TplFormat, NotAlignError
from tpltable.tabel_flow import TableFlow
from tpltable.tabel_io import TableIO
from tpltable.pipe import Pipe
from tpltable.utils import Vec4, load_workbook, log as tpl_log

# filefinder
from tpltable.filefinder import FileFinder, tHWEXCEL_find

if __name__ == '__main__':
    t = TableIO()
    print(t)
    t.extend(['tpl.xlsx', 'res.xlsx', 'data.xlsx'])
    print(t)
