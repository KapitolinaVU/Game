# Определение персонажей игры.
define s = Character('Студент', color="#615ac4")
define narrator = Character(None, kind = nvl, what_color="#ffffff", size = 12)
define p1 = Character('Препод', color="#d20606")

# стресс в диапозоне 1-10
default stress_level = 2

# уровень энергии (в %)
default energy_level = 30

# деньги в рублях
default money = 5000

default ToL_mark = 3
default PfL_mark = 3


#Всякие дефолтные условия
default day1_hunger = True

#функции
init python:

    def check_stress(stress_level):
        if stress_level > 10:
            return False
        return True

    def check_energy(energy_level):
        if energy_level < 1:
            return False
        return True

# Игра начинается здесь:
label start:

    '''Добро пожаловать в игру "Заботать все экзамены за неделю".
    Ваша задача - помочь студенту подготовиться и не улететь на пересдачу
    
    И помните - Все персонажи и события вымышлены, любые совпадения с реальностью случайны'''
    nvl clear

    scene bg dorm_room
    with fade
    
    'До сессии осталось 7 дней'
    'Попробуйте пережить их'
    nvl clear

    "ДЕНЬ 1. Пятница"

    play music 'alarm.mp3'
    "звонит будильник"
    nvl clear

    s 'Вчера был насыщенный день. Еле-еле открываю глаза'
    s '7:50!! Етитская богомышь, я проспал!'

    stop music
    
    menu:
        s 'Чертовы пары в 8 утра. Есть ли смысл ехать?'
        
        "Конечно. Нельзя пропускать занятия!":
            jump day1_go_8
        
        "Ну нафиг, я лучше посплю":
            jump day1_sleep1
        
    return


label day1_go_8:
    
    menu:
        s 'Так. Дорога на автобусе займет полчаса. Так жестко опаздывать некрасиво...'
        
        "Да пофиг. Поеду на автобусе":
            scene bg black
            with fade
            $ money -= 30
            "Осталось [money] рублей"
            nvl clear
            jump day1_canceled1
        
        'Поеду на такси':
            scene bg black
            with fade
            $ money -= 500
            "Осталось [money] рублей"
            nvl clear
            jump day1_canceled1


label day1_sleep1:
    'Пара отменилась'
    nvl clear

    $ energy_level += 10

    s 'Офигенно. Как чувствовал'

    menu:
        s 'Пора вствавать, если я хочу успеть на вторую пару'

        'Как хорошо, что я не хочу успеть на вторую пару':
            jump day1_sleep2
        
        'Встаю':
            jump day1_go_930


label day1_canceled1:
    scene bg kostina with fade
    s 'Уфф... Наконец-то доехал'
    
    'Пара отменилась'
    nvl clear

    s 'Черт! Зря ездил'

    menu:
        s 'Что мне делать и куда теперь идти?'
        
        'Пойду посижу в коворкинге, может что-то полезное сделаю':
            jump day1_coworking
        
        'Мак, жди меня':
            jump day1_mac


label day1_coworking:
    scene bg coworking
    with fade
    'Что-то полезное поделать не получилось'
    "Студент уснул в мешке и проспал вторую пару"
    nvl clear

    $ energy_level += 8

    label day1_lesson2_skipped:
        'Вы пропустили семинар по теории языка'
        'Препод вам это еще припомнит'
        nvl clear
        $ stress_level += 1
        if not check_stress(stress_level):
            jump stressed_end

        $ ToL_mark -= 2

    s 'Черт!'
    s 'Ну хоть на третью пару схожу...'
    
    $ day1_lesson2_skipped = True

    jump day1_lesson3


label day1_mac:
    scene bg mac with fade
    s 'Вкусно'

    $ day1_hunger = False
    $ energy_level += 15
    $ money -= 500
    "Осталось [money] рублей"
    nvl clear

    s 'Теперь можно и на пару'
    jump day1_lesson2


label day1_sleep2:
    $ energy_level += 10

    'Вы пропустили семинар по теории языка'
    'Препод вам это еще припомнит'
    nvl clear
    $ stress_level += 1
    if not check_stress(stress_level):
        jump stressed_end
    $ ToL_mark -= 2

    s 'Зато поспал'

    s "Как хорошо в кровати"
    s 'Я еще могу успеть на третью пару'

    menu:
        s 'А надо ли мне туда?'

        "Ну хоть на одну пару можно сходить":
            jump day1_go_1110
        "А зачем вставать, если можно не вставать?":
            jump day1_sleep3


label day1_go_930:
    'трясемся в автобусе'
    
    $ money -= 30
    '-30 р.'
    "Осталось [money] рублей"
    nvl clear

    jump day1_lesson2


label day1_go_1110:
    'трясемся в автобусе'
    
    $ money -= 30
    '-30 р.'
    "Осталось [money] рублей"
    nvl clear

    jump day1_lesson3


label day1_lesson2:
    scene bg classroom with fade
    'Пара 2. Теория языка'
    nvl clear

    menu:
        s 'Чем бы заняться на паре?'

        "Проявлять активность":
            show prof1 right
            $ energy_level -= 10
            if not check_energy(energy_level):
                jump energless_ending

            s 'Мне нужен хороший накоп, так что я сегодня отвечаю на семинаре'
            $ stress_level -= 1
            $ ToL_mark += 2
        
        "Готовиться к другому экзамену":
            $ energy_level -= 10
            if not check_energy(energy_level):
                jump energless_ending

            s 'Проект по проге сам себя не сделает'
            $ PfL_mark += 1
            'Препод видит, что студент не слушает'
            show prof1 norm at center
            'Ей это не нравится'
            nvl clear
            'Рандомный вопрос'
            nvl clear
            
            transform alpha_dissolve:
                alpha 0.0
                linear 0.5 alpha 1.0
                on hide:
                    linear 0.5 alpha 0
            
            screen countdown():
                timer 0.01 repeat True action If(time > 0, true=SetVariable('time', time - 0.01), false=[Hide('countdown'), Jump(timer_jump)])
                bar value time range timer_range xalign 0.5 yalign 0.9 xmaximum 300 at alpha_dissolve # This is the timer bar.

            init:
                $ timer_range = 0
                $ timer_jump = 0

            # time = the time the timer takes to count down to 0.
            # timer_range = a number matching time (bar only)
            # timer_jump = the label to jump to when time runs out

            label menu1:
                $ time = 5
                $ timer_range = 5
                $ timer_jump = 'menu1_slow'
                show screen countdown
                menu:
                    p1 'Назовите тип придаточного в предложении: 
                        "Вы себялюбивы до сумасшествия, чему доказательством служат и ваши письма ко мне"'

                    "присубстантивное":
                        hide screen countdown
                        p1 "Неправильно"
                        'Она посмотрела осуждающе и что-то пометила у себя в блокноте'
                        nvl clear
                        $ ToL_mark -= 1
                        jump menu1_end
                    
                    "присоединительное":
                        hide screen countdown
                        p1 "Верно"
                        $ stress_level -= 1

                        $ ToL_mark += 1
                        jump menu1_end
                    
                    "изъяснительное":
                        hide screen countdown
                        p1 "Неправильно"
                        'Она посмотрела осуждающе и что-то пометила у себя в блокноте'
                        nvl clear
                        $ ToL_mark -= 1
                        jump menu1_end
                
                label menu1_slow:
                    p1 "Вы не успели ответить"
                    'Она посмотрела осуждающе и что-то пометила у себя в блокноте'
                    nvl clear
    
                label menu1_end:
                    hide prof1
                    s "..."
                    s 'Это было страшно'

        "Спать":
            "Ваши отношения с преподавателем ухудшились"
            show prof1 right
            "Этот сон вам еще аукнется"
            nvl clear
            $ stress_level += 2
            if not check_stress(stress_level):
                jump stressed_end
            $ ToL_mark -= 2
    hide prof1
        
    "Конец занятия"
    "Пора на следующую пару"
    nvl clear
    jump day1_lesson3


label day1_lesson3:
    scene bg classroom with fade
    'Пара 3. Программирование'
    nvl clear

    $ energy_level -= 10
    if not check_energy(energy_level):
                jump energless_ending

    $ PfL_mark += 2

    s 'Как быстро пролетело занятие'
    s 'Пора в общагу'

    $ money -= 30
    jump day1_evening


label day1_sleep3:
    $ energy_level += 10
    s "Уже почти три часа дня, а я даже не встал с кровати"
    s 'День прожит зря'
    s '*прокрастинирует*'
    $ stress_level += 3
    if not check_stress(stress_level):
        jump stressed_end
    $ PfL_mark -= 2

    jump day1_evening


label day1_evening:
    scene bg dorm_room
    with fade
    s 'Наверное, теперь пора заняться подготовкой к экзаменам'

    if energy_level > 30:
        "Студент активно ботает"
        nvl clear
        s 'Теперь я на шаг ближе к хорошим отметкам'
        $ PfL_mark += 1
        $ ToL_mark += 1
    else:
        s 'Но я слишком устал...'
        s 'Пожалуй, вздремну ненадолго'
        scene bg black with fade
        
        $ energy_level += 15
        $ stress_level += 3
        if not check_stress(stress_level):
            jump stressed_end
        
        $ PfL_mark -= 1
        $ ToL_mark -= 1

        '21:00'
        nvl clear
        scene bg dorm_room with fade
        s 'Ой, Уже вечер. 
        Я чувствую себя таким разбитым. Нет сил ботать'
    
    if day1_hunger:
        s '...'
        s 'Хочу есть'
        s "Придется заказать доставку"
        $ money -= 800
        "Осталось [money] рублей"
        nvl clear
    
    "Тут раздался звук уведомления"
    nvl clear
    s "Подруга прислала приглашение на тусу завтра вечером"
    s "Круто! Хочу развеяться и сбросить напряжение
    Но с другой стороны скоро экзамены...
    Что же делать?"

    jump to_be_continued


label stressed_end:
    'Уровень стресса превышен'
    "У вас нервный срыв"
    nvl clear
    jump the_end


label energless_ending:
    'Слишком мало энергии'
    nvl clear
    jump the_end


label the_end:
    "GAME OVER"
    jump references


label to_be_continued:
    "Продолжение следует..."
    jump references


label references:
    'Спасибо за то, что выбрали нашу игру'