# Welcome-project
## Тестовое задание для инженера

**Привет!**

Это тестовое домашнее задание, которое поможет нам сэкономить время и избежать дополнительных вопросов на очной встрече.

По результатам выполнения этого задания, мы хотели бы увидеть, как Вы:

- Пишете и структурируете код
- Тестируете написанный код (unit tests)
- Документируете свое решение


Мы ценим Ваше время, поэтому не ожидаем полноценного и законченного решения.
Но, просим сделать следующее:

1. Напишите алгоритм
2. 2–3 unit теста будет достаточно
3. Несколько строк документации по какой-либо части решения

Ниже доступно описание задачи, которую предлагаеться решить.

Сделайте fork этого репозитория и отправьте нам ссылку на PR, когда решение будет готово.
Пожалуйста задавайте вопросы и/или уточнения по задаче — это нормально, мы готовы ответить. 
Просто создайте issue и мы постараемся оперативно ответить.

Удачи! И Увидимся позже!

## Задача

Даны сервисы и описание API к ним, это описание и станет входными данными для задачи.

Необходимо, использовать описание ниже и разработать решение, которое будет:

- принимать эти данные
- формировать из них map/json

### Пример входных данных


Каждый запрос это массив кортежей (verb, path). 

```
                 verb           path
                  |              |
                  |              |

    service1 = [("GET", "/api/v1/cluster/metrics"),
                ("POST", "/api/v1/cluster/{cluster}/plugins"),
                ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")]


    service2 = [("GET", "/api/v1/cluster/freenodes/list"),
                ("GET", "/api/v1/cluster/nodes"),
                ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
                ("POST", "/api/v1/cluster/{cluster}/plugins")]
```

> **_NOTE:_** значения в фигурных скобках `{}` - параметры

### Решение

Необходимо реализовать следующую логику:

*Сценарий 1*. Первый вызов

```
    IN ->    [("GET", "/api/v1/cluster/metrics"),
              ("POST", "/api/v1/cluster/{cluster}/plugins"),
              ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")]

                                |

    LOGIC ->            parse and collect data
                        
        Разбить path на составляющие (split "/") и сформировать структуру типа дерево, 
        ключами и узлами которого будут эти составляющие слова, а значением конечного пути - verb (метод - POST, GET..). 
        При формировании этого дерева исключить версию (/api/v1) и параметры ({cluster})

                                |

    OUT ->      {'cluster': 
                    {'metrics': 'GET', 
                    'plugins': 'POST'}
                }    
```

*Сценарий 2*. Второй и последующие вызовы

```
    IN ->    [("GET", "/api/v1/cluster/freenodes/list"),
              ("GET", "/api/v1/cluster/nodes"),
              ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
              ("POST", "/api/v1/cluster/{cluster}/plugins")]

                                |

    LOGIC ->            parse and collect data

        1. Ранее обработанные данные участвуют в обработке
        2. Если путь/поддерево не существует - создать новую ветвь
        3. Если путь/поддерево существует - проверить verb
            3.1 Если verb такой же - пропустить
            3.2 Если verb отличается - вызвать Exception с полным путем до этого verb
                                |

    OUT ->     {'cluster': 
                    {'metrics': 'GET', 
                    'plugins': 'POST', 
                    'freenodes': {'list': 'GET'}, 
                    'nodes': 'GET'
                    }
                }
```

### Проверка

```bash
$ docker-compose up tests
```
