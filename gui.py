import PySimpleGUI as sg
import json
import traceback

from entities import *
from generators import *
from automated_cql_generation import *

# Window layout
file_viewer_column = [
    [
        sg.Text("Input JSON File: "),
        sg.In(enable_events=True, key="-FILE-", size=(88, 1)),
        sg.FileBrowse()
    ],
    [sg.Multiline(key='-FILEOUT-', auto_size_text=True, font=('Courier New', 15), size=(73, 48))],
    [sg.Button('Convert', key='-STARTCONVERT-')]
]

output_viewer_column = [
    [sg.Text('Output CQL')],
    [sg.Multiline('No output generated yet', key='-CQLOUTPUT-', size=(68,49), font=('Courier New', 15))],
    [sg.Input(key='-SAVEAS-FILENAME-', visible=False, enable_events=True), sg.FileSaveAs('Save to File', default_extension='cql')]
]

column_size = (700, 900)
layout = [[
    sg.Column(file_viewer_column, size=column_size),
    sg.VSeperator(),
    sg.Column(output_viewer_column, size=column_size)
]]

sg.theme('NeutralBlue')
window = sg.Window('Automated CQL Generation', layout, size=(1400,920), resizable=True)

try:
    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == '-FILE-':
            file_input = values['-FILE-']
            with open(file_input, 'r') as f:
                file_read = f.read()
            window['-FILEOUT-'].update(file_read)
            window['-CQLOUTPUT-'].update('No output generated yet')

        if event == '-STARTCONVERT-':
            window['-CQLOUTPUT-'].update('Starting to convert to CQL')
            json_to_convert = json.loads(values['-FILEOUT-'])
            output_cql = cql_from_json_with_entities(json_to_convert)
            window['-CQLOUTPUT-'].update(output_cql)

        if event == '-SAVEAS-FILENAME-':
            outfile_name = values['-SAVEAS-FILENAME-']
            if outfile_name != '':
                with open(outfile_name, 'w') as f:
                    f.write(values['-CQLOUTPUT-'])
except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened.  Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)
window.close()