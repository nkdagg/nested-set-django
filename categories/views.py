import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .serializers import CategorySerializer
from .models import Category
from . import utils

@csrf_exempt
def update(request):
    try:
        data = utils.validate_json(request.body)
        utils.validate_input_data(data)
        
        to_db = utils.prepare_categories_data(data)
            
        with transaction.atomic():
            for entry in to_db:
                Category.create(to_db[entry]["parent"], entry, to_db[entry]["lft"], to_db[entry]["rgt"]).save()
        
        return JsonResponse("Request successful", status=status.HTTP_200_OK, safe = False)
    except ValueError:
        return JsonResponse("Invalid POST request", status=status.HTTP_400_BAD_REQUEST, safe = False)  
    

def get_category_by_id(id):
    return(CategorySerializer(Category.objects.get(id=id)).data)


def get_children_by_id(id):
    categorySet = Category.objects.raw('''SELECT * 
                                    FROM categories_category AS node, categories_category AS parent
                                    WHERE node.lft BETWEEN parent.lft AND parent.rgt 
                                    AND parent.id = "%s" AND NOT node.id = "%s"
                                    ORDER BY node.lft''' % (id, id))
    serializer = CategorySerializer(categorySet, many=True)
    return serializer.data


def get_ancestors_by_id(id):
    categorySet = Category.objects.raw('''SELECT ancestor.id 
                                        FROM categories_category AS child
                                        JOIN categories_category AS ancestor 
                                        ON child.lft BETWEEN ancestor.lft AND ancestor.rgt 
                                        WHERE child.id = %s AND NOT ancestor.id = %s 
                                        ORDER BY ancestor.lft DESC''' % (id, id))
    serializer = CategorySerializer(categorySet, many=True)
    return serializer.data


def get_siblings_by_id(id):
    categorySet = Category.objects.raw('''SELECT * FROM categories_category 
                                        WHERE parent IN (SELECT parent 
                                        FROM categories_category WHERE id = %s) AND id IS NOT %s''' % (id, id))
    serializer = CategorySerializer(categorySet, many=True)
    return serializer.data


def compose_get_by_id_response(request, id):

    target_category = get_category_by_id(id)
    siblings = get_siblings_by_id(id)
    parents = get_ancestors_by_id(id)
    children = get_children_by_id(id)

    response = {
        "id": target_category["id"],
        "name": target_category["name"],
        "parents": utils.extract_values_from_ord_dicts(parents),
        "children": utils.extract_values_from_ord_dicts(children),
        "siblings": utils.extract_values_from_ord_dicts(siblings)
    }

    return JsonResponse(response, status=status.HTTP_200_OK, safe = False)
