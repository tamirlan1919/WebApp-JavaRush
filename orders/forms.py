from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        label='Получатель',
        widget=forms.TextInput(attrs={'class': "Input", 'placeholder': "Иван Иванов"})
    )
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        widget=forms.TextInput(attrs={'class': "Input", 'placeholder': "+7 999 000-00-00"})
    )
    city = forms.CharField(
        max_length=100,
        label='Город',
        widget=forms.TextInput(attrs={'class': "Input"})
    )
    address = forms.CharField(

        label='Адрес доставки',
        widget=forms.TextInput(attrs={'class': "TextArea", 'rows': '3'})
    )

    payment_method = forms.ChoiceField(
        choices=[
            ('card', "Банковская карта"),
            ('wallet', "Электронный кошелек"),
            ('cod', "Наличные при получении"),
        ],
        widget=forms.RadioSelect,
        label='Способ оплаты'
    )

