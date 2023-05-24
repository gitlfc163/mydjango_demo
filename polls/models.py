from django.db import models

# Create your models here.

# 问题描述
# Question 模型包括问题描述和发布时间
class Question(models.Model):
    # 问题描述
    question_text = models.CharField(max_length=200)
    # 发布时间
    # pub_date = models.DateTimeField("date published")
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

# 选项描述
# Choice 模型包括选项描述和投票数
class Choice(models.Model):
    # 所属问题
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # 选项描述
    choice_text = models.CharField(max_length=200)
    # 投票数
    # votes = models.IntegerField(default=0)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice_text