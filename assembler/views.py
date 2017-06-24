from django.shortcuts import render
from .forms import UploadFileForm

from .assembler2 import handle_uploaded_file, handle_local_file, list_to_str


def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():

			file_content, adr_sym, machine_code = handle_uploaded_file(request.FILES.get('uploaded_file'))
			adr_table = []
			count = 1
			countNest = 0

			for elem in adr_sym:
				adr_table.append([count, elem[0], list_to_str(elem[1], 0),
								  list_to_str(elem[2][countNest], 0)])

				count += 1
				countNest += 1

				if ',' in elem[0]:
					adr_table.append([count, '(LC)', list_to_str(elem[3], 0),
									  list_to_str(elem[4], 1)])
					count += 1
					countNest = 0

			return render(request, 'assembler/output.html', {'file_content': file_content,
															 'adr_table': adr_table,
															 'machine_code': machine_code})
		else:
			return render(request, 'assembler/noFile.html')
	else:
		form = UploadFileForm()

	return render(request, 'assembler/upload.html', {'form': form})

def local_file(request, file_name):
	if file_name in ['XwqloqwenkjaUas', 'oqweApasdkIKASD', 'LKSDKLJsaaklSDF']:
		file_content, adr_sym, machine_code = handle_local_file(file_name)
		adr_table = []
		count = 1
		countNest = 0

		for elem in adr_sym:
			adr_table.append([count, elem[0], list_to_str(elem[1], 0),
							  list_to_str(elem[2][countNest], 0)])

			count += 1
			countNest += 1

			if ',' in elem[0]:
				adr_table.append([count, '(LC)', list_to_str(elem[3], 0),
												 list_to_str(elem[4], 1)])
				count += 1
				countNest = 0

		return render(request, 'assembler/output.html', {'file_content': file_content,
														 'adr_table': adr_table,
														 'machine_code': machine_code})
	else:
		return render(request, 'assembler/noFile.html')
