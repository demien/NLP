# encoding=utf-8
import json
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render_to_response
from nlp.learning import predict


class HomeView(View):
    
    def get(self, request, *args, **kwargs):
        return render_to_response('home.html', {'content': []})


class EstimateView(View):
    
    def get(self, request, *args, **kwargs):
        complain = request.GET.get('complain', '')
        re = predict(complain)
        formatted = []
        for item in re:
            category_list, score = item
            formatted_item = (re.index(item) + 1, category_list[0], category_list[1])
            formatted.append(formatted_item)
        return HttpResponse(json.dumps(formatted), content_type="application/json")
