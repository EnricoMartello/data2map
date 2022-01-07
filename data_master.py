import openpyxl
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import PySimpleGUI as sg

def read_measures(dataname):
	wb = load_workbook(dataname, data_only = True);
	sh = wb['Confezionamento'];
	print(len(wb.sheetnames))
	data = list(sh.values);

	print(data)

	#print(wb.sheetnames)
	#for i in range(20):
	#	print(sh.cell(row=3, column=i+1).value)

#if color_in_hex !=0 we are considering a wall!!!


def select_sheet(dataname):
	wb = load_workbook(dataname, data_only = True);
	event, values = sg.Window(
		'Scegli un foglio di lavoro', 
		[[sg.Text('Scegli->'), 
		sg.Listbox(wb.sheetnames, size=(20, 3), key='LB')],
    [sg.Button('Ok'), sg.Button('Cancel')]]).read(close=True)

	# if event == 'Ok':
	# 	sg.popup(f'Hai scelto {values["LB"][0]}')
	# else:
	# 	sg.popup_cancel('User aborted')

	sh = wb[str(values["LB"][0])];	
	data = []
	for rowNumber in range(1, sh.max_row + 1):
		if sh.cell(row=rowNumber, column=1).value != None:
			data.append(sh.cell(row=rowNumber, column=1).value)

	return data

def select_datatype():
	event, values = sg.Window(
		'Scegli il tipo di misurazione effettuata', 
		[[sg.Text('Scegli->'), 
		sg.Listbox(["Sorgenti luminose", "Fonti di rumore"], size=(20, 3), key='LB')],
    [sg.Button('Ok'), sg.Button('Cancel')]]).read(close=True)

	# if event == 'Ok':
	# 	sg.popup(f'Hai scelto {values["LB"][0]}')
	# else:
	# 	sg.popup_cancel('User aborted')

	return (f'{values["LB"][0]}' == "Sorgenti luminose")