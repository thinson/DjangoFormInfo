from django.shortcuts import render, get_object_or_404
from .models import Answer, Question, Questionnaire

# from django.http import HttpResponseRedirect

# Create your views here.
def showlist(request):
    context = {}
    if request.user.is_authenticated:
        question_sheet_all = Questionnaire.objects.all()
        final_list = []
        for sheet in question_sheet_all:
            answer = sheet.answer_set.all()
            answer_user = answer.filter(author=request.user)
            if not answer_user:
                final_list.append(sheet)
        context['list'] = final_list
    return render(request, 'list.html', context)

def sheet_detail(request, sheet_pk):
    context={}
    sheet = get_object_or_404(Questionnaire, pk=sheet_pk)
    questions = Question.objects.filter(question_sheet=sheet)
    context['questions'] = questions
    context['sheet'] = sheet
    return render(request, 'detail.html', context)

def submit(request):
    if (request.method == 'POST'):
        temp = request.POST
        post_list = list(temp.keys())
        for key in post_list[1:-1]:
            answer = Answer()

            answer.author = request.user

            form_name = key
            answer.answer_name = request.POST.get(form_name, '')
            if answer.answer_name == '':
                return render(request, 'message.html', {'message': '不要留空格，谢谢'})
            question_id = int(form_name[7:])
            question = Question.objects.get(pk=question_id)
            answer.question = question

            sheet_id = int(request.POST.get('sheet_id', ''))
            sheet = Questionnaire.objects.get(pk=sheet_id)
            answer.question_sheet = sheet

            answer.save()
        return render(request, 'message.html', {'message': '提交成功'})
    else:
        return render(request, 'message.html', {'message': '未知错误'})
