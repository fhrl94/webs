from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

Score_CHOICES = (
    ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
    ('9', '9'), ('10', '10'),)
Department_CHOICES = (('y', '运营增值部'), ('k', '客户发展部'),)


class InformationEmployees(models.Model):
    """
    用户信息
    """

    # Sex_CHOICES = (
    #     ('m', '男'),
    #     ('w', '女'),
    # )

    # Level_CHOICES = (
    #     ('s', '试用'),
    #     ('z', '正式'),
    # )

    Section_CHOICES = (
        ('y1', '1-28天'), ('y2', '29-49天'), ('y3', '50-77天'), ('y4', '78-105天'), ('y5', '106-133天'), ('y6', '134-161天'),
        ('k1', '1-14天'), ('k2', '15-30天'), ('k3', '31-60天'), ('k4', '61-90天'),)

    name = models.CharField('姓名', max_length=10)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES)
    group = models.CharField('组别', max_length=30)
    superior_name = models.CharField('调查上级', max_length=10)
    # sex = models.CharField('性别', max_length=1, choices=Sex_CHOICES)
    # level = models.CharField('级别', max_length=1, choices=Level_CHOICES)
    # position = models.CharField('岗位', max_length=20, )
    enter_date = models.DateField('入职日期', )
    #  正则验证
    tel = models.CharField('联系方式', max_length=11, validators=[RegexValidator(r'^^[\d]{11}')], unique=True)
    #  自动计算
    enter_days = models.PositiveIntegerField('入职天数', default=0)
    #  主键关联
    section_one = models.BooleanField('阶段一')
    section_two = models.BooleanField('阶段二')
    section_three = models.BooleanField('阶段三')
    section_four = models.BooleanField('阶段四')
    section_five = models.BooleanField('阶段五')
    section_six = models.BooleanField('阶段六')
    #  自动计算
    current_section = models.CharField('当前阶段', max_length=2, choices=Section_CHOICES, )
    # user_name = models.CharField('用户', max_length=50)
    # password = models.CharField('密码', max_length=20, blank=True)
    # email = models.EmailField(blank=True)
    emp_user = models.OneToOneField(User, )

    def __str__(self):
        return self.name

    pass


class CustomerOne(models.Model):
    #  限定分数大小
    question_one = models.CharField('您与主管相互介绍，并留下联系方式', max_length=2, choices=Score_CHOICES)
    question_two = models.CharField('部门内利用早会或者夕会，介绍部门里的每个人给您认识', max_length=2, choices=Score_CHOICES)
    question_three = models.CharField('在部门内有为您安排属于自己的工位', max_length=2, choices=Score_CHOICES)
    question_four = models.CharField('主管有向您介绍阐述客服岗位工作职责内容及自身的发展空间、价值', max_length=2, choices=Score_CHOICES)
    question_five = models.CharField('主管有明确安排您前期学习的工作及学习内容，包括：基础知识的学习、日常维护工作流程、后台操作等学习计划', max_length=2,
                                     choices=Score_CHOICES)
    question_six = models.CharField('主管或者师傅在日常工作中能及时发现及时纠正您工作中的不足，好的地方及时肯定和表扬', max_length=2, choices=Score_CHOICES)
    question_seven = models.CharField('在部门中，带您学习的主管或者老员工会与主动与您多接触，帮助消除陌生感，让您尽快融入团队，有归属感', max_length=2,
                                      choices=Score_CHOICES)
    question_eight = models.CharField('主管有与您进行单独沟通：让您了解公司文化、发展战略等，并了解您在培训期间的专业能力、家庭背景、职业规划与兴趣爱好', max_length=2,
                                      choices=Score_CHOICES)
    question_nine = models.CharField('明确安排一位老员工带着你学习及工作，包括：每天要做什么、怎么做', max_length=2, choices=Score_CHOICES)
    score_sum = models.PositiveIntegerField('分数合计')
    question_summary = models.CharField('评估总结', max_length=200)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES, )
    group = models.CharField('组别', max_length=30, )
    employees = models.ForeignKey(InformationEmployees, on_delete=models.CASCADE)

    length_field = 9

    def __str__(self):
        return self.employees

    pass


class CustomerTwo(models.Model):
    #  限定分数大小
    question_one = models.CharField('您熟悉公司环境和各部门情况，例：怎么写规范的公司邮件，怎么发传真，电脑出现问题找哪个人，如何接内部电话等', max_length=2,
                                    choices=Score_CHOICES)
    question_two = models.CharField('您坐在老同事附近，方便对工作进行观察，并能得到指导', max_length=2, choices=Score_CHOICES)
    question_three = models.CharField('您的情绪状态反馈后，能给予及时引导调整您的情绪状态反馈后，能给予及时引导调整', max_length=2, choices=Score_CHOICES)
    question_four = models.CharField('主管或师傅有适时把自己的经验及时传授给您，能让您在实战中学习，做到学中干，干中学', max_length=2, choices=Score_CHOICES)
    question_five = models.CharField('您的成长和进步有较突出的表现时，能受到及时肯定和赞扬，并会给您提出更高的期望', max_length=2, choices=Score_CHOICES)
    score_sum = models.PositiveIntegerField('分数合计')
    question_summary = models.CharField('评估总结', max_length=200)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES, )
    group = models.CharField('组别', max_length=30, )
    employees = models.ForeignKey(InformationEmployees, on_delete=models.CASCADE)

    length_field = 5

    def __str__(self):
        return self.employees

    pass


class CustomerThree(models.Model):
    #  限定分数大小
    question_one = models.CharField('主管知道您的长处及掌握的技能，并对您讲清工作要求及考核要求', max_length=2, choices=Score_CHOICES)
    question_two = models.CharField('您有机会多参与部门会议或活动，展示优点和能力，可以让主管帮助自己扬长提短进行培养成长', max_length=2, choices=Score_CHOICES)
    question_three = models.CharField('您出现负面情绪并反馈时，能受到及时指引与调整', max_length=2, choices=Score_CHOICES)
    question_four = models.CharField('当公司有重大事情或振奋人心的消息时，部门内均有分享', max_length=2, choices=Score_CHOICES)
    question_five = models.CharField('能获得培训的机会，鼓励您多学习，多看书', max_length=2, choices=Score_CHOICES)
    score_sum = models.PositiveIntegerField('分数合计')
    question_summary = models.CharField('评估总结', max_length=200)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES, )
    group = models.CharField('组别', max_length=30, )
    employees = models.ForeignKey(InformationEmployees, on_delete=models.CASCADE)

    length_field = 5

    def __str__(self):
        return self.employees

    pass


class CustomerFour(models.Model):
    #  限定分数大小
    question_one = models.CharField('您有机会多参与部门会议或活动，展示优点和能力，可以让主管帮助自己扬长提短进行培养成长', max_length=2, choices=Score_CHOICES)
    question_two = models.CharField('您犯错误时会得到指正，并了解您在遇到困难时的的心态与行为', max_length=2, choices=Score_CHOICES)
    question_three = models.CharField('鼓励您积极参与团队会议，并在发言之后获得点评', max_length=2, choices=Score_CHOICES)
    question_four = models.CharField('您出现负面情绪并反馈时，能受到及时指引与调整', max_length=2, choices=Score_CHOICES)
    question_five = models.CharField('当公司有重大事情或振奋人心的消息时，部门内均有分享', max_length=2, choices=Score_CHOICES)
    question_six = models.CharField('能开始独立自行完成工作', max_length=2, choices=Score_CHOICES)
    question_seven = models.CharField('能获得培训的机会，鼓励您多学习，多看书，参加公司的培训', max_length=2, choices=Score_CHOICES)
    question_eight = models.CharField('主管能关注到您的生活', max_length=2, choices=Score_CHOICES)
    question_nine = models.CharField('明确安排一位老员工带着你学习及工作，包括：每天要做什么、怎么做', max_length=2, choices=Score_CHOICES)
    score_sum = models.PositiveIntegerField('分数合计')
    question_summary = models.CharField('评估总结', max_length=200)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES, )
    group = models.CharField('组别', max_length=30, )
    employees = models.ForeignKey(InformationEmployees, on_delete=models.CASCADE)

    length_field = 9

    def __str__(self):
        return self.employees

    pass


class CustomerFive(models.Model):
    #  限定分数大小
    question_one = models.CharField('您有机会多参与部门会议或活动，展示优点和能力，可以让主管帮助自己扬长提短进行培养成长', max_length=2, choices=Score_CHOICES)
    question_two = models.CharField('您犯错误时会得到指正，并了解您在遇到困难时的的心态与行为', max_length=2, choices=Score_CHOICES)
    question_three = models.CharField('对团队产品落地等活动能参与商讨，提出建议', max_length=2, choices=Score_CHOICES)
    question_four = models.CharField('您出现负面情绪并反馈时，能受到及时指引与调整', max_length=2, choices=Score_CHOICES)
    question_five = models.CharField('有学习企业的使命，公司的愿景和文化价值', max_length=2, choices=Score_CHOICES)
    question_six = models.CharField('当公司有重大事情或振奋人心的消息时，部门内均有分享', max_length=2, choices=Score_CHOICES)
    question_seven = models.CharField('主管能协助您制定目标和措施，指定项目负责人监督检查目标进度，协助达成既定目标', max_length=2, choices=Score_CHOICES)
    question_eight = models.CharField('能获得培训的机会，鼓励您多学习，多看书', max_length=2, choices=Score_CHOICES)
    score_sum = models.PositiveIntegerField('分数合计')
    question_summary = models.CharField('评估总结', max_length=200)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES, )
    group = models.CharField('组别', max_length=30, )
    employees = models.ForeignKey(InformationEmployees, on_delete=models.CASCADE)
    length_field = 8

    def __str__(self):
        return self.employees

    pass


class CustomerSix(models.Model):
    #  限定分数大小
    question_one = models.CharField('您有机会多参与部门会议或活动，展示优点和能力，可以让主管帮助自己扬长提短进行培养成', max_length=2, choices=Score_CHOICES)
    question_two = models.CharField('取得成绩时，获得分享成功的经验的机会', max_length=2, choices=Score_CHOICES)
    question_three = models.CharField('与老同事发生矛盾时，寻求协助后主管给予及时处理', max_length=2, choices=Score_CHOICES)
    question_four = models.CharField('能认清对工作的定位与认识工作的价值、意义、责任、使命，找到目标和方向', max_length=2, choices=Score_CHOICES)
    question_five = models.CharField('当公司有重大事情或振奋人心的消息时，部门内均有分享', max_length=2, choices=Score_CHOICES)
    question_six = models.CharField('每季度至少有1次主管与您的面谈', max_length=2, choices=Score_CHOICES)
    question_seven = models.CharField('能获得培训的机会，鼓励您多学习，多看书', max_length=2, choices=Score_CHOICES)
    question_eight = models.CharField('主管能关注到您的生活', max_length=2, choices=Score_CHOICES)
    question_nine = models.CharField('每季有不限形式的团队集体活动，增加团队的凝聚力', max_length=2, choices=Score_CHOICES)
    score_sum = models.PositiveIntegerField('分数合计')
    question_summary = models.CharField('评估总结', max_length=200)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES, )
    group = models.CharField('组别', max_length=30, )
    employees = models.ForeignKey(InformationEmployees, on_delete=models.CASCADE)
    length_field = 9

    def __str__(self):
        return self.employees

    pass


class SellOne(models.Model):
    #  限定分数大小
    question_one = models.CharField('大区有为您准备卡片等小礼物', max_length=2, choices=Score_CHOICES)
    question_two = models.CharField('在部门内有为您安排属于自己的工位，配置好电脑，并安装好Foxmail、erp、百度hi等常用办公软件', max_length=2,
                                    choices=Score_CHOICES)
    question_three = models.CharField('部门内利用早会或者夕会，介绍部门里的每个人给您认识，并留联系方式。', max_length=2, choices=Score_CHOICES)
    question_four = models.CharField('明确安排一位老员工带着你学习及工作，包括：每天要做什么、怎么做', max_length=2, choices=Score_CHOICES)
    question_five = models.CharField('主管或者师傅帮您安排了第一周的工作任务，包括每天要做什么、怎么做', max_length=2, choices=Score_CHOICES)
    question_six = models.CharField('主管有向您介绍阐述销售岗位工作职责内容及自身的发展空间、价值', max_length=2, choices=Score_CHOICES)
    question_seven = models.CharField('部门有针对新人大礼包的使用对您进行讲解。', max_length=2, choices=Score_CHOICES)
    question_eight = models.CharField('主管有与您进行单独沟通：让您了解公司文化、发展战略等，并了解您在培训期间的专业能力、家庭背景、职业规划与兴趣爱好', max_length=2,
                                      choices=Score_CHOICES)
    question_nine = models.CharField('主管或者师傅在日常工作中能及时发现及时纠正您工作中的不足，好的地方及时肯定和表扬', max_length=2, choices=Score_CHOICES)
    question_ten = models.CharField('在部门中，带您学习的主管或者老员工会与主动与您多接触，帮助消除陌生感，让您尽快融入团队，有归属感', max_length=2,
                                    choices=Score_CHOICES)
    score_sum = models.PositiveIntegerField('分数合计')
    question_summary = models.CharField('评估总结', max_length=200)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES, )
    group = models.CharField('组别', max_length=30, )
    employees = models.ForeignKey(InformationEmployees, on_delete=models.CASCADE)
    length_field = 10

    def __str__(self):
        return self.employees

    pass


class SellTwo(models.Model):
    #  限定分数大小
    question_one = models.CharField('主管或师傅为您做电话录音分析', max_length=2, choices=Score_CHOICES)
    question_two = models.CharField('您坐在老同事附近，方便对工作进行观察，并能得到指导', max_length=2, choices=Score_CHOICES)
    question_three = models.CharField('您的情绪状态反馈后，能给予及时引导调整', max_length=2, choices=Score_CHOICES)
    question_four = models.CharField('主管或师傅有适时把自己的经验及时传授给您，能让您在实战中学习，做到学中干，干中学', max_length=2, choices=Score_CHOICES)
    question_five = models.CharField('您的成长和进步有较突出的表现时，能受到及时肯定和赞扬，并会给您提出更高的期望', max_length=2, choices=Score_CHOICES)
    question_six = models.CharField('您有机会主持大区大早会', max_length=2, choices=Score_CHOICES)
    question_seven = models.CharField('每季度至少有1次主管与您的面谈（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                      choices=Score_CHOICES)
    question_eight = models.CharField('每季至少有1次不限形式的团队集体活动，增加团队的凝聚力（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                      choices=Score_CHOICES)
    question_nine = models.CharField('部门主管有不少2次的陪同外访，师傅或老员工有不少于3次的陪同外访（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                     choices=Score_CHOICES)
    question_ten = models.CharField('在您转正时，经理有给您做正式的转正面谈（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                    choices=Score_CHOICES)
    score_sum = models.PositiveIntegerField('分数合计')
    question_summary = models.CharField('评估总结', max_length=200)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES, )
    group = models.CharField('组别', max_length=30, )
    employees = models.ForeignKey(InformationEmployees, on_delete=models.CASCADE)
    length_field = 10

    def __str__(self):
        return self.employees

    pass


class SellThree(models.Model):
    #  限定分数大小
    question_one = models.CharField('主管知道您的长处及掌握的技能，并对您讲清工作要求及考核要求', max_length=2, choices=Score_CHOICES)
    question_two = models.CharField('您有机会多参与部门会议或活动，展示优点和能力，可以让主管帮助自己扬长提短进行培养成长', max_length=2, choices=Score_CHOICES)
    question_three = models.CharField('您出现负面情绪并反馈时，能受到及时指引与调整', max_length=2, choices=Score_CHOICES)
    question_four = models.CharField('当公司有重大事情或振奋人心的消息时，部门内均有分享', max_length=2, choices=Score_CHOICES)
    question_five = models.CharField('能获得培训的机会，鼓励您多学习，多看书', max_length=2, choices=Score_CHOICES)
    question_six = models.CharField('鼓励您积极参与团队会议，并在发言之后获得点评', max_length=2, choices=Score_CHOICES)
    question_seven = models.CharField('能开始独立自行完成工作', max_length=2, choices=Score_CHOICES)
    question_eight = models.CharField('每季度至少有1次主管与您的面谈（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                      choices=Score_CHOICES)
    question_nine = models.CharField('每季至少有1次不限形式的团队集体活动，增加团队的凝聚力（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                     choices=Score_CHOICES)
    question_ten = models.CharField('部门主管有不少2次的陪同外访，师傅或老员工有不少于3次的陪同外访（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                    choices=Score_CHOICES)
    score_sum = models.PositiveIntegerField('分数合计')
    question_summary = models.CharField('评估总结', max_length=200)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES, )
    group = models.CharField('组别', max_length=30, )
    employees = models.ForeignKey(InformationEmployees, on_delete=models.CASCADE)
    length_field = 10

    def __str__(self):
        return self.employees

    pass


class SellFour(models.Model):
    #  限定分数大小
    question_one = models.CharField('您有机会多参与部门会议或活动，展示优点和能力，可以让主管帮助自己扬长提短进行培养成长', max_length=2, choices=Score_CHOICES)
    question_two = models.CharField('您犯错误时会得到指正，并了解您在遇到困难时的的心态与行为', max_length=2, choices=Score_CHOICES)
    question_three = models.CharField('对激励机制、团队建设、任务等活动能参与商讨，提出建议', max_length=2, choices=Score_CHOICES)
    question_four = models.CharField('对团队、任务等活动能参与商讨，提出建议', max_length=2, choices=Score_CHOICES)
    question_five = models.CharField('您出现负面情绪并反馈时，能受到及时指引与调整', max_length=2, choices=Score_CHOICES)
    question_six = models.CharField('有学习企业的使命，公司的愿景和文化价值', max_length=2, choices=Score_CHOICES)
    question_seven = models.CharField('当公司有重大事情或振奋人心的消息时，部门内均有分享', max_length=2, choices=Score_CHOICES)
    question_eight = models.CharField('主管能协助您制定目标和措施，指定项目负责人监督检查目标进度，协助达成既定目标', max_length=2, choices=Score_CHOICES)
    question_nine = models.CharField('能获得培训的机会，鼓励您多学习，多看书，参加公司的培训', max_length=2, choices=Score_CHOICES)
    question_ten = models.CharField('主管能关注到您的生活', max_length=2, choices=Score_CHOICES)
    question_eleven = models.CharField('取得成绩时，获得分享成功的经验的机会', max_length=2, choices=Score_CHOICES)
    question_twelve = models.CharField('与老同事发生矛盾时，寻求协助后主管给予及时处理', max_length=2, choices=Score_CHOICES)
    question_thirteen = models.CharField('能认清对工作的定位与认识工作的价值、意义、责任、使命，找到目标和方向', max_length=2, choices=Score_CHOICES)
    question_fourteen = models.CharField('每季度至少有1次主管与您的面谈（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                         choices=Score_CHOICES)
    question_fifteen = models.CharField('每季至少有1次不限形式的团队集体活动，增加团队的凝聚力（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                        choices=Score_CHOICES)
    question_sixteen = models.CharField('部门主管有不少2次的陪同外访，师傅或老员工有不少于3次的陪同外访（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                        choices=Score_CHOICES)
    question_seventeen = models.CharField('在您转正时，经理有给您做正式的转正面谈（如果有，请评分；如果没有，该项不填）', blank=True, max_length=2,
                                          choices=Score_CHOICES)
    score_sum = models.PositiveIntegerField('分数合计')
    question_summary = models.CharField('评估总结', max_length=200)
    department = models.CharField('部门', max_length=1, choices=Department_CHOICES, )
    group = models.CharField('组别', max_length=30, )
    employees = models.ForeignKey(InformationEmployees, on_delete=models.CASCADE)
    length_field = 17

    def __str__(self):
        return self.employees

    pass
