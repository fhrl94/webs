from django import forms
from .models import CustomerOne, InformationEmployees, CustomerTwo, CustomerThree, CustomerFour, CustomerFive, \
    CustomerSix, SellOne, SellTwo, SellThree, SellFour


class UserForm(forms.Form):
    账号 = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'user', 'placeholder': '请输入用户名', 'aria-describedby': 'sizing-addon1', }))
    密码 = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'user', 'placeholder': '请输入密码', 'aria-describedby': 'sizing-addon2', }))
    pass


self_fields = ['question_one', 'question_two', 'question_three', 'question_four', 'question_five', 'question_six',
               'question_seven', 'question_eight', 'question_nine', 'question_ten', 'question_eleven',
               'question_twelve', 'question_thirteen', 'question_fourteen', 'question_fifteen', 'question_sixteen',
               'question_seventeen', 'question_summary', ]

self_widgets = {'question_one': forms.Select(
    attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon1', }),
    'question_two': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon2', }),
    'question_three': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon3', }),
    'question_four': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon4', }),
    'question_five': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon5', }),
    'question_six': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon6', }),
    'question_seven': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon7', }),
    'question_eight': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon8', }),
    'question_nine': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon9', }),
    'question_ten': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon10', }),
    'question_eleven': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon11', }),
    'question_twelve': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon12', }),
    'question_thirteen': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon13', }),
    'question_fourteen': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon14', }),
    'question_fifteen': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon15', }),
    'question_sixteen': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon16', }),
    'question_seventeen': forms.Select(
        attrs={'class': 'form-control', 'placeholder': '请输入分数', 'aria-describedby': 'sizing-addon17', }),
    'question_summary': forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
               'rows': 3, 'cols': 80, }), }


class CustomerOneForm(forms.ModelForm):
    class Meta:
        model = CustomerOne
        # 字典
        fields = self_fields[:model.length_field]
        fields.append(self_fields[-1])
        widgets = {}
        for j, one in enumerate(self_fields[:model.length_field]):
            widgets[one] = forms.Select(attrs={'class': 'form-contro', 'placeholder': '请输入分数',
                                               'aria-describedby': 'sizing-addon{j}'.format(j=j), })
        widgets['question_summary'] = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
                   'rows': 3, 'cols': 80, })
        pass


class CustomerTwoForm(forms.ModelForm):
    class Meta:
        model = CustomerTwo
        # 字典
        fields = self_fields[:model.length_field]
        fields.append(self_fields[-1])
        widgets = {}
        for j, one in enumerate(self_fields[:model.length_field]):
            widgets[one] = forms.Select(attrs={'class': 'form-contro', 'placeholder': '请输入分数',
                                               'aria-describedby': 'sizing-addon{j}'.format(j=j), })
        widgets['question_summary'] = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
                   'rows': 3, 'cols': 80, })
        pass


class CustomerThreeForm(forms.ModelForm):
    class Meta:
        model = CustomerThree
        # 字典
        fields = self_fields[:model.length_field]
        fields.append(self_fields[-1])
        widgets = {}
        for j, one in enumerate(self_fields[:model.length_field]):
            widgets[one] = forms.Select(attrs={'class': 'form-contro', 'placeholder': '请输入分数',
                                               'aria-describedby': 'sizing-addon{j}'.format(j=j), })
        widgets['question_summary'] = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
                   'rows': 3, 'cols': 80, })
        pass


class CustomerFourForm(forms.ModelForm):
    class Meta:
        model = CustomerFour
        # 字典
        fields = self_fields[:model.length_field]
        fields.append(self_fields[-1])
        widgets = {}
        for j, one in enumerate(self_fields[:model.length_field]):
            widgets[one] = forms.Select(attrs={'class': 'form-contro', 'placeholder': '请输入分数',
                                               'aria-describedby': 'sizing-addon{j}'.format(j=j), })
        widgets['question_summary'] = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
                   'rows': 3, 'cols': 80, })
        pass


class CustomerFiveForm(forms.ModelForm):
    class Meta:
        model = CustomerFive
        # 字典
        fields = self_fields[:model.length_field]
        fields.append(self_fields[-1])
        widgets = {}
        for j, one in enumerate(self_fields[:model.length_field]):
            widgets[one] = forms.Select(attrs={'class': 'form-contro', 'placeholder': '请输入分数',
                                               'aria-describedby': 'sizing-addon{j}'.format(j=j), })
        widgets['question_summary'] = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
                   'rows': 3, 'cols': 80, })
        pass


class CustomerSixForm(forms.ModelForm):
    class Meta:
        model = CustomerSix
        # 字典
        fields = self_fields[:model.length_field]
        fields.append(self_fields[-1])
        widgets = {}
        for j, one in enumerate(self_fields[:model.length_field]):
            widgets[one] = forms.Select(attrs={'class': 'form-contro', 'placeholder': '请输入分数',
                                               'aria-describedby': 'sizing-addon{j}'.format(j=j), })
        widgets['question_summary'] = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
                   'rows': 3, 'cols': 80, })
        pass


class SellOneForm(forms.ModelForm):
    class Meta:
        model = SellOne
        # 字典
        fields = self_fields[:model.length_field]
        fields.append(self_fields[-1])
        widgets = {}
        for j, one in enumerate(self_fields[:model.length_field]):
            widgets[one] = forms.Select(attrs={'class': 'form-contro', 'placeholder': '请输入分数',
                                               'aria-describedby': 'sizing-addon{j}'.format(j=j), })
        widgets['question_summary'] = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
                   'rows': 3, 'cols': 80, })
        pass


class SellTwoForm(forms.ModelForm):
    class Meta:
        model = SellTwo
        # 字典
        fields = self_fields[:model.length_field]
        fields.append(self_fields[-1])
        widgets = {}
        for j, one in enumerate(self_fields[:model.length_field]):
            widgets[one] = forms.Select(attrs={'class': 'form-contro', 'placeholder': '请输入分数',
                                               'aria-describedby': 'sizing-addon{j}'.format(j=j), })
        widgets['question_summary'] = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
                   'rows': 3, 'cols': 80, })
        pass


class SellThreeForm(forms.ModelForm):
    class Meta:
        model = SellThree
        # 字典
        fields = self_fields[:model.length_field]
        fields.append(self_fields[-1])
        widgets = {}
        for j, one in enumerate(self_fields[:model.length_field]):
            widgets[one] = forms.Select(attrs={'class': 'form-contro', 'placeholder': '请输入分数',
                                               'aria-describedby': 'sizing-addon{j}'.format(j=j), })
        widgets['question_summary'] = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
                   'rows': 3, 'cols': 80, })
        pass


class SellFourForm(forms.ModelForm):
    class Meta:
        model = SellFour
        # 字典
        fields = self_fields[:model.length_field]
        fields.append(self_fields[-1])
        widgets = {}
        for j, one in enumerate(self_fields[:model.length_field]):
            widgets[one] = forms.Select(attrs={'class': 'form-contro', 'placeholder': '请输入分数',
                                               'aria-describedby': 'sizing-addon{j}'.format(j=j), })
        widgets['question_summary'] = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': '请输入评价(不要超过200字)', 'aria-describedby': 'sizing-addon10',
                   'rows': 3, 'cols': 80, })
        pass
