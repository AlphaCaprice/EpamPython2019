"""
Написать тесты(pytest) к предыдущим 3 заданиям, запустив которые, я бы смог бы проверить их корректность
"""

import os
import pytest
import task1, task2, task3
from task1 import PrintableFile, PrintableFolder
from task2 import Graph
from task3 import CaesarCipher


def test_printable():
    work_path = os.path.abspath(r"..\..\06-advanced-python\hw_test1")
    pfolder = PrintableFolder(work_path)
    pfile1 = PrintableFile("file1.txt")
    pfile3 = PrintableFile("file3.txt")
    result = "V hw_test1\n" \
             "|-> V hw_test0\n" \
             "|\t|-> file3.txt\n" \
             "|-> file1.txt\n" \
             "|-> file2.txt\n"
    assert str(pfolder) == result
    assert pfile1 in pfolder
    assert pfile3 not in pfolder


def test_graph():
    E = {'A': ['B', 'C', 'D'], 'C': ['F'], 'D': ['A'], 'E': ['F'],
         'F': ['G'], 'G': [], 'B': ['C', 'E']}
    out = list("ABCDEFG")
    graph = Graph(E)
    for vertex, value in zip(graph, out):
        assert vertex == value


@pytest.mark.parametrize('mes, text, expected', [
    ('message', 'abc', 'efg'),
    ('another_message', 'hello', 'olssv'),
    ('out_message', 'xyz', 'abc')
])
def test_cipher(mes, text, expected):
    a = CaesarCipher()
    setattr(a, mes, text)
    assert getattr(a, mes) == expected


