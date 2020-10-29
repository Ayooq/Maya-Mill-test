import random
from functools import partial

import maya.cmds as cmds
import maya.mel as mel


def offset_selected_animation(offset_field, *args):
    time_offset = cmds.intField(offset_field, query=True, value=True)

    # ������������ ������ ���������� ��������, ������� ���� ����������.
    selection_list = cmds.ls(selection=True, type='transform')

    # ���������� ������� ������ �������� �� ���������� ������� ��������� �����.
    time_slider = mel.eval('$tmpVar=$gPlayBackSlider')
    time_range_selected = cmds.timeControl(time_slider, query=True, rangeArray=True)
    start, stop = time_range_selected

    cmds.cutKey(
        selection_list,
        time=(start, stop),
        option='curve',
    )
    cmds.pasteKey(
        selection_list,
        timeOffset=time_offset,
        option='replace',
    )


def close_window(window_id, *args):
    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id, window=True)


def create_window(window_title, apply_callback, cancel_callback):
    window_id = 'myWindowID'
    cancel_callback(window_id)    # ���� �� ������ ����������� ������ ������ ��.

    new_window = cmds.window(
        window_id,
        title=window_title,
        widthHeight=(1, 1),    # ���������� ��� ���������� ������ ���������� �����.
        resizeToFitChildren=True,
        sizeable=False,
        toolbox=True,
    )
    
    # ��������� ������� ��� ����.
    cols_width = [(1, 150), (2, 60)]
    col_offset = (1, 'right', 3)
    col_gutter = (1, 10)
    row_gutter = (1, 5)
    cmds.rowColumnLayout(
        numberOfColumns=2,
        columnWidth=cols_width,
        columnOffset=col_offset,
        columnSpacing=col_gutter,
        rowSpacing=row_gutter,
    )

    # ������ ���.
    cmds.text(label='������ ��������:')
    offset_field = cmds.intField(value=0)

    # ������ ���.
    cmds.button(
        label='���������',
        command=partial(apply_callback, offset_field),
    )
    cmds.button(
        label='������',
        command=partial(cancel_callback, window_id),
    )

    return new_window


window_title = '���������� �������� ��������'
window = create_window(window_title, offset_selected_animation, close_window)
cmds.showWindow(window)