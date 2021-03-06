""""

Задание 1

0) Повторение понятий из биологии (ДНК, РНК, нуклеотид, протеин, кодон)

1) Построение статистики по входящим в последовательность ДНК нуклеотидам 
для каждого гена (например: [A - 46, C - 66, G - 23, T - 34])

2) Перевод последовательности ДНК в РНК (окей, Гугл)

3) Перевод последовательности РНК в протеин*


*В папке files вы найдете файл rna_codon_table.txt - 
в нем содержится таблица переводов кодонов РНК в аминокислоту, 
составляющую часть полипептидной цепи белка.


Вход: файл dna.fasta с n-количеством генов

Выход - 3 файла:
 - статистика по количеству нуклеотидов в ДНК
 - последовательность РНК для каждого гена
 - последовательность кодонов для каждого гена

 ** Если вы умеете в matplotlib/seaborn или еще что, 
 welcome за дополнительными баллами за
 гистограммы по нуклеотидной статистике.
 (Не забудьте подписать оси)

P.S. За незакрытый файловый дескриптор - караем штрафным дезе.

"""

import pprint


def translate_from_dna_to_rna(dna):
    """ Переводит цепочку ДНК в РНК """
    # Иначально переводил в иРНК, пока не прочитал сообщение в телеграме
    dna_to_rna = {
        "G": "C",
        "C": "G",
        "A": "U",
        "T": "A"
    }
    with open("rna_from_dna.txt", "w") as out_file:
        for line in dna:
            if line.startswith(">"):
                out_file.write(line)
            else:
                out_file.write(line.replace('T', 'U'))
                # line = line.rstrip('\n')
                # out_line = [dna_to_rna.get(letter) for letter in line]
                # out_file.write("".join(out_line))
                # out_file.write('\n')


def count_symbols(s: str) -> dict:
    """ Подсчитывает количество вхождений каждого символа в строке """
    counter = {}
    for i in s:
        if i in counter:
            counter[i] += 1
        else:
            counter[i] = 1
    return counter


def count_nucleotides(dna):
    """ Функция получения статистики о нуклеотидах ДНК """
    statistics = []
    description = {}
    for line in dna:
        line = line.rstrip('\n')
        if line.startswith(">"):
            if description:
                statistics.append(description.copy())
                description.clear()
            description["name"] = line[1:]
        else:
            for i in line:
                if i in description:
                    description[i] += 1
                else:
                    description[i] = 1
    statistics.append(description.copy())
    pprint.pprint(statistics)

    # Запись в файл результатов
    with open("nucleotides_stat.txt", "w") as out_file:
        for stat in statistics:
            for key, value in stat.items():
                out_file.write(f"{key}    {value}\n")
            out_file.write("----------------------------------\n")


# Словарь соотвествий кодонов и аминокислот
def get_dict_rna_to_codon(dictionary, file_path):
    with open(file_path) as f:
        for line in f:
            line = line.rstrip('\n').split("   ")
            dictionary.update(
                {item.split(" ")[0]: item.split(" ")[1]
                    for item in line if item}
            )
    pprint.pprint(dictionary)


def translate_rna_to_protein(rna):
    """ Переводит последовательность РНК в протеин """
    # Создаём словарь для хранения таблицы кодонов
    rna_to_protein_dict = {}
    get_dict_rna_to_codon(rna_to_protein_dict, r"files\rna_codon_table.txt")

    # Проходим по каждой строке РНК файла, бьём на триплеты-кодоны,
    # кодоны преобразуем в аминокислоту по словарю
    with open(rna, "r") as rna_file:
        with open("codons_for_genes.txt", "w") as codon_file:
            for line in rna_file:
                if line.startswith(">"):
                    codon_file.write(line)
                else:
                    line = line.rstrip('\n')
                    out_list = [line[i:i+3] for i in range(0, len(line), 3)]
                    out_list = [rna_to_protein_dict.get(i)
                                for i in out_list if len(i) == 3]
                    codon_file.write("".join(out_list))
                    codon_file.write('\n')


# read the file dna.fasta
with open("files/dna.fasta", "r") as dna_file:
    count_nucleotides(dna_file)


# Второй раз потому что мы прошлись уже по файлу,
# вызвав предыдущую функцию
with open("files/dna.fasta", "r") as dna_file:
    translate_from_dna_to_rna(dna_file)
    translate_rna_to_protein("rna_from_dna.txt")

