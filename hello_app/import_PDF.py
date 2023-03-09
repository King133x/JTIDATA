import PySimpleGUI as sg
import PyPDF2
import os
import datetime

sg.theme('DarkBlue')

layout = [[sg.Text('Select a PDF file to convert:')],
          [sg.Input(key='-FILE-', enable_events=True, visible=False), sg.FileBrowse()],
          [sg.Multiline(key='-OUTPUT-', size=(50, 10), font=('Courier New', 12))],
          [sg.Button('Convert'), sg.Button('Clear'), sg.Button('Save as Text'), sg.Button('Exit')]]

window = sg.Window('PDF to Text Converter', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        window['-OUTPUT-'].update('')
        continue
    if event == 'Convert':
        if not values['-FILE-']:
            sg.popup_error('Please select a file to convert.')
            continue
        with open(values['-FILE-'], 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            page_count = len(pdf_reader.pages)
            text = ''
            for i in range(page_count):
                page = pdf_reader.pages[i]
                text += page.extract_text()
            window['-OUTPUT-'].update(text)
    if event == 'Save as Text':
        if not values['-OUTPUT-']:
            sg.popup_error('No text to save.')
            continue
        file_name = os.path.splitext(os.path.basename(values['-FILE-']))[0]
        date_today = datetime.datetime.now().strftime('%Y-%m-%d')
        default_file_name = f'{file_name}_{date_today}.txt'
        file = sg.popup_get_file('Save as', save_as=True, default_extension='.txt', default_path=default_file_name)
        if file:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(values['-OUTPUT-'])

window.close()



'''
pdf_reader = PyPDF2.PdfReader(file)
            page_count = len(pdf_reader.pages)
         
                page = pdf_reader.pages[i]
                text += page.extract_text()
'''