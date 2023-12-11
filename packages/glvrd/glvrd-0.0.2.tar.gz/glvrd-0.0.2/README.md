# glvrd - неофициальный клиент к сервису glvrd.ru

Это неофициальный и не production-ready клиент для замечательного сервиса проверки текстов - glvrd.ru. Работает в обход API, так что на особую скорость советую не расчитывать.

Устанавливается так:

```bash
pip install glvrd
```

Пример кода:

```python
from glvrd import GlvrdClient

client = GlvrdClient()
text = 'Это неофициальный и не production-ready клиент для замечательного сервиса проверки текстов - glvrd.ru. Работает в обход API, так что на особую скорость советую не расчитывать.'

def print_estimate(estimate, what_is_it):
  print(f'{what_is_it}: {estimate.estimate}')
  for error_name, examples in estimate.errors.items():
    print(f'{error_name}:')
    for example in examples:
      print(f'\t{example}')


print_estimate(client.estimate_clarity(text), 'Чистота')
print_estimate(client.estimate_readability(text), 'Читаемость')
```

... выдаст что-то вроде:

```
8.1
Необъективная оценка:
	замечательного
Усилитель:
	особую
8.8
В начале предложения нет глагола:
	Это неофициальный и не production-ready клиент для замечательного сервиса
Подозрение на парцелляцию:
	Работает в обход
```
