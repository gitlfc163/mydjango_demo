# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.views import generic

# 问题索引页
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

# 问题详情页-按问题描述ID查看问题详情
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

# 问题结果页-按问题描述ID查看问题结果
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# 投票处理器-用于响应用户为某个问题的特定选项投票的操作。
def vote(request, question_id):
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
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))