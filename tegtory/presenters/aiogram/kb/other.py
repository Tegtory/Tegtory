from .callbacks import OtherCB
from .utils import one_inline_button_markup

working_on = one_inline_button_markup("В работе", OtherCB.working_on)
subscribed_channel = one_inline_button_markup("Готово", OtherCB.subscribe)

balance_markup = one_inline_button_markup("Кошелёк", OtherCB.balance)
