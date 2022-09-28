"""
TicTacToe model

Board coordinate encoding

00|01|01
--------
10|11|11
--------
20|21|21
"""

# coding for board locations
m00 = "00"
m01 = "01"
m02 = "02"

m10 = "10"
m11 = "11"
m12 = "12"

m20 = "20"
m21 = "21"
m22 = "22"


def v1(fn, cell, role):

    player = role("player")

    # declare locations
    l00 = fn(m00, role=player)
    l01 = fn(m01, role=player)
    l02 = fn(m02, role=player)

    l10 = fn(m10, role=player)
    l11 = fn(m11, role=player)
    l12 = fn(m12, role=player)

    l20 = fn(m20, role=player)
    l21 = fn(m21, role=player)
    l22 = fn(m22, role=player)

    # no repetition
    cell(m00, initial=1).tx(1, l00)
    cell(m01, initial=1).tx(1, l01)
    cell(m02, initial=1).tx(1, l01)

    cell(m10, initial=1).tx(1, l10)
    cell(m11, initial=1).tx(1, l11)
    cell(m12, initial=1).tx(1, l12)

    cell(m20, initial=1).tx(1, l20)
    cell(m21, initial=1).tx(1, l21)
    cell(m22, initial=1).tx(1, l22)

    # one move at a time
    move = cell("moving", initial=0, capacity=1)

    # annotate each move with its location
    move.tx(1, l00)
    move.tx(1, l01)
    move.tx(1, l02)

    move.tx(1, l10)
    move.tx(1, l11)
    move.tx(1, l12)

    move.tx(1, l20)
    move.tx(1, l21)
    move.tx(1, l22)

    # start each move by annotating player role
    sendX = fn("X", role=role("playerX")).tx(1, move)
    sendO = fn("O", role=role("playerO")).tx(1, move)

    # x goes first
    turnX = cell("x_turn", initial=1, capacity=1).tx(1, sendX)
    turnO = cell("o_turn", initial=0, capacity=1).tx(1, sendO)

    # alternate turns
    sendX.tx(1, turnO)
    sendO.tx(1, turnX)
