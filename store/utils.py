from django.shortcuts import redirect
import uuid

def is_logged_in(request):
    return 'admin' in request.session


def generate_ref_code():    
    code=str(uuid.uuid4()).replace("-","")[:12]
    return code