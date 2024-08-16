from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Image

def image_list(request):
    images = Image.objects.all().order_by('-uploaded_at')
    paginator = Paginator(images, 12)  # Show 12 images per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'image_list.html', {'page_obj': page_obj})