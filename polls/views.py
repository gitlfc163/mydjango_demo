# from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.template import loader

# 问题索引页
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    # 指定上下文对象名称，这里指定的是latest_question_list，这个名称将在模板中使用
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)
    # return HttpResponse(template.render(context, request))

# 问题详情页-按问题描述ID查看问题详情
def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("问题不存在")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
    # return HttpResponse("You're looking at question %s." % question_id)

# 问题结果页-按问题描述ID查看问题结果
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

# 投票页-按问题描述ID查看问题投票页
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

# 投票处理器-用于响应用户为某个问题的特定选项投票的操作。
def vote2(request, question_id):
    # 根据问题id获取对应的问题对象，如果不存在则返回404错误
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 根据用户提交的表单数据获取对应的选项对象
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 如果用户没有选择任何选项，或者选择了不存在的选项，重新渲染问题详情页，并显示错误信息
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # 如果用户选择了有效的选项，增加该选项的票数，并重定向到问题结果页
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))