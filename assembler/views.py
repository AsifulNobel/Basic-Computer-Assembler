from django.shortcuts import render
from .forms import UploadFileForm

from assembler import handle_uploaded_file, handle_local_file


def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():

			file_content, label_dictionary, machine_code = handle_uploaded_file(request.FILES.get('uploaded_file'))


			return render(request, 'assembler/output.html', {'file_content': file_content,
															 'label_dictionary': label_dictionary,
															 'machine_code': machine_code})
		else:
			return render(request, 'assembler/noFile.html')
	else:
		form = UploadFileForm()

	return render(request, 'assembler/upload.html', {'form': form})

def local_file(request, file_name):
	if file_name in ['XwqloqwenkjaUas', 'oqweApasdkIKASD', 'LKSDKLJsaaklSDF']:
		file_content, label_dictionary, machine_code = handle_local_file(file_name)

		return render(request, 'assembler/output.html', {'file_content': file_content,
														 'label_dictionary': label_dictionary,
														 'machine_code': machine_code})
	else:
		return render(request, 'assembler/noFile.html')