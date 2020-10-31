import re


#--- stemmer Porter ---
RVRE = re.compile(r'^(.*?[аеиоуыэюя])(.*)$')
PERFECTIVEGROUND = re.compile(r'((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[ая])(в|вши|вшись)))$')
REFLEXIVE = re.compile(r'(с[яь])$')
ADJECTIVE = re.compile(r'(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$')
VERB = re.compile(r'((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить'
                  r'|ыть|ишь|ую|ю)|((?<=[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$')
NOUN = re.compile(r'(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию'
                  r'|ью|ю|ия|ья|я)$')
I = re.compile(r'и$')
PARTICIPLE = re.compile(r'((ивш|ывш|ующ)|((?<=[ая])(ем|нн|вш|ющ|щ)))$')
DERIVATIONAL = re.compile(r'(ость|ост)$')
P = re.compile(r'ь$')
NN = re.compile(r'нн$')
SUPERLATIVE = re.compile(r'(ейше|ейш)$')
NOT_LETTER = re.compile(r'[^a-яА-Яё]$')

#--- stop-symbols ---
NEWLINE_SYMBOLS = re.compile(r'-\n|\n|\t')
STOP_SYMBOLS = re.compile(r'\s(-|а|без|более|больше|будет|будто|бы|был|была|были|было|быть|в|вам|вас|вдруг|ведь|во'
                          r'|вот|впрочем|все|всегда|всего|всех|всю|вы|г|где|говорил|да|даже|два|для|до|еще|ж|же|жизнь'
                          r'|за|зачем|здесь|и|из|из-за|или|им|иногда|их|к|кажется|как|какая|какой|когда|конечно|которого'
                          r'|которые|кто|куда|ли|лучше|между|меня|мне|много|может|можно|мой|моя|него|нее|ней|нельзя|нет'
                          r'|ни|нибудь|никогда|ним|них|ничего|но|ну|о|об|один|он|она|они|опять|от|перед|по|под|после|потом'
                          r'|потому|почти|при|про|раз|разве|с|сам|свое|сказать|со|совсем|так|такой|там|тебя|тем|теперь'
                          r'|то|тогда|того|тоже|только|том|тот|три|тут|ты|у|уж|уже|хорошо|хоть|чего|человек|чем|через'
                          r'|что|чтоб|чтобы|чуть|эти|этого|этой|другой|его|ее|ей|ему|если|есть|мы|на|над|надо|наконец'
                          r'|нас|не|свою|себе|себя|сегодня|сейчас|сказал|сказала|этом|этот|эту|я)\s')
OTHER_SYMBOLS = re.compile(r'\.|\'|\"|!|\?|,|:|&|\*|@|#|№|\(|\)|\[|\]|\{|\}|\$|%|\^|\\|/|;|\<|\>|\+|\-|\=|\s\d+|\d+\s')

#--- variables ---
dict_texts = {}                    # ключи - T1, T2... значения - текст файлов Т1, Т2 и тд


class Text:
    def __init__(self, text_file, path):
        self.text_file = text_file
        self.filename = path.split('\\')[len(path.split('\\')) - 1]
        self.checksum = []
        self.duplicates = {}

    def __repr__(self):
        return self.text_file


# функция запрашивает пути файлов для считывания и помещает весь текст в словарь dict_texts.
def input_data():
    print("Укажите пути (по умолчанию 'D:\Учёба\\7 семестр (-)\- Технологии обработки информации (Экз)\Лабораторная работа №5\Testing text 2')")
    i = 0
    while True:
        path_to_file = input("Укажите путь к файлу: ")
        if path_to_file.upper() == 'END':
            break
        text_file = get_text(path_to_file)
        if text_file[0]:
            dict_texts['T' + str(i + 1)] = Text(text_file[0], text_file[1])
            i += 1
        else:
            break


# функция считывает тексты из файлов.
def get_text(path_to_file):
    text = ''
    while True:
        try:
            file = open(path_to_file, "r")

            for line in file:
                text += line
            file.close()
            return [text, path_to_file]

        except:
            path_to_file = input("Не найден указанный путь. Попробуйте еще раз, или введите 'END', чтобы завершить: " + "\n")
            if path_to_file.upper() == "END":
                break

    return [False]


# в функцию передается текст из файла в виде строки. Из нее удаляются все ненужные символы и возвращается отформатиро-
# ванный текст.
def delete_stop_symbols(text):
    text = text.lower()
    result = NEWLINE_SYMBOLS.sub('', text)
    result = OTHER_SYMBOLS.sub('', result)
    result = ' ' + result + ' '
    result = STOP_SYMBOLS.sub(' ', result)
    return result


# функция реализует алгоритм стемминга. Принимает слово, возвращает основу слова.
def stemming(word):
    word = word.lower()
    word = word.replace('ё', 'e')
    area = re.match(RVRE, word)

    if area is not None:
        PREFIX = area.group(1)
        RV = area.group(2)

        # step 1
        template = PERFECTIVEGROUND.sub('', RV, 1)
        if template == RV:
            RV = REFLEXIVE.sub('', RV, 1)
            template = ADJECTIVE.sub('', RV, 1)

            if template != RV:
                RV = template
                RV = PARTICIPLE.sub('', RV, 1)
            else:
                template = VERB.sub('', RV, 1)
                if template == RV:
                    RV = NOUN.sub('', RV, 1)
                else:
                    RV = template
        else:
            RV = template

        # step 2
        RV = I.sub('', RV, 1)

        # step 3
        RV = DERIVATIONAL.sub('', RV, 1)

        # step 4
        template = NN.sub('н', RV, 1)
        if template == RV:
            template = SUPERLATIVE.sub('', RV, 1)
            if template != RV:
                RV = template
                RV = NN.sub('н', RV, 1)
            else:
                RV = P.sub('', RV, 1)
        else:
            RV = template
        word = PREFIX + RV
    return word


# функция для разбиения текста на шинглы и перевода их в контрольные суммы. Вовращает список контрольных сумм шинглов.
def get_checksum(source):
    import binascii     # для получения контрольной суммы CRC32
    shingle_length = 4  # длина шингла
    array_checksum = []
    for i in range(len(source)-(shingle_length-1)):
        array_checksum.append(binascii.crc32(' '.join([x for x in source[i:i+shingle_length]]).encode('utf-8')))
    return array_checksum


# функция для сравнения двух списков чексумм. Возвращает степень схожести документов в процентах.
def comparison(array_checksum1, array_checksum2):
    duplicate = 0
    for i in range(len(array_checksum1)):
        if array_checksum1[i] in array_checksum2:
            duplicate = duplicate + 1
    return duplicate * 2/float(len(array_checksum1) + len(array_checksum2))*100


# функция ищет дубликаты и выводит их. Результат зависит от процента схожести. Принимает словарь объектов и степень
# схожести
def search_duplicates(objects, similarity):
    keys = list(objects.keys())         # получили список ключей словаря.
    print("---------------------------------")
    print("Ключи: " + str(keys))
    print("---------------------------------")
    for obj in objects:
        print(str(obj) + ' ' + str(objects[obj].filename) + ' ' + str(objects[obj].text_file))
        for i in range(len(keys)):
            if objects[obj] is not objects[keys[i]]:
                texts_similarity = comparison(objects[obj].checksum, objects[keys[i]].checksum)
                if texts_similarity > similarity:
                    objects[obj].duplicates[objects[keys[i]].filename] = texts_similarity


# --- start program ---
input_data()
for key in dict_texts:
    print(dict_texts.get(key))
# step 1 - удаляем все стоп символы, знаки препинания, пробельные символы и дт.
for obj in dict_texts:
    dict_texts[obj].text_file = delete_stop_symbols(dict_texts[obj].text_file)

# step 2
# 2.1. разбиваем всё на массивы слов.
for key in dict_texts:
    dict_texts[key].text_file = dict_texts[key].text_file.strip() # удалить все пробельные символы в начале и в конце.
    dict_texts[key].text_file = dict_texts[key].text_file.split(' ')
    # print(dict_texts[text])
# 2.2. проводим операцию стемминга.
# step 3 - помещаем в словарь all_words все слова. Оставляем только повторяющиеся.
i = 0
for T in dict_texts:
    j = 0
    for word in dict_texts[T].text_file:
        dict_texts[T].text_file[j] = stemming(word)
        j += 1
    i += 1

# step 4 - создаем словарь со списками контрольных сумм
for T in dict_texts:
    dict_texts[T].checksum = get_checksum(dict_texts[T].text_file)
    print(dict_texts[T].checksum)
similarity = int(input("Введите искомую схожесть документов: "))
search_duplicates(dict_texts, similarity)

print("---------------------------------------------")
print("---------------------------------------------")

for obj in dict_texts:
    if dict_texts[obj].duplicates:
        print("Дубликаты текста " + dict_texts[obj].filename)
        print(dict_texts[obj].duplicates)
        print("---------------------------------------------")


