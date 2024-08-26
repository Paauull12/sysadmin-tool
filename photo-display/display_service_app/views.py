from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Image

def image_list(request):
    images = Image.objects.all().order_by('-uploaded_at')
    paginator = Paginator(images, 12)  # Show 12 images per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'image_list.html', {'page_obj': page_obj})

def image_retrieve(request, image_id):


    try:
        images = Image.objects.get(id=image_id)
        return render(request, 'image_retrieve.html', {"img": images})
    except Image.DoesNotExist:
        print(f'Image with id {image_id} does not exist.')
    #images = Image.objects.get(id=image_id)

    #image = get_object_or_404(Image, id=image_id)

    return render(request, 'image_retrieve.html')