from django.shortcuts import render
from .forms import UploadFileForm

from assembler import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_content, label_dictionary, machine_code = handle_uploaded_file(request.FILES.get('uploaded_file'))

            return render(request, 'assembler/output.html', {'file_content': file_content, 'label_dictionary':label_dictionary, 'machine_code':machine_code})
        else:
            return render(request, 'assembler/noFile.html')
    else:
        form = UploadFileForm()
    return render(request, 'assembler/upload.html', {'form': form})
