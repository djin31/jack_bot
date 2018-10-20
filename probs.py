#!/usr/bin/python

from random import random
import numpy as np
import sys


def deal(p):
    out = random()
    if out < p:
        return 10
    else:
        return int((out-p)/((1-p)/9))+1


def sim_dealer_full(cards,p):
    #check if we are in a terminal state
    res=[0,0,0,0,0,0,0,0]
    if(1 in cards) and sum(cards)==7:
        res[0]=1.0
    elif (1 in cards) and (10 in cards) and len(cards)==2:
        res[6]=1.0
    elif 17<=sum(cards)<=21:
        res[sum(cards)-16]=1.0
    elif 8<=sum(cards)<=11 and (1 in cards):
        res[sum(cards)-6]=1.0
    elif sum(cards)>21:
        res[-1]=1.0
    else:
        #not a terminal state
        return ((1-p)/9.0) * sum([sim_dealer_full(cards+[i+1],p) for i in range(9)])+ p*sim_dealer_full(cards+[10],p)
    return np.array(res)


# def sim_dealer(start, p, iter=1000):
#     res = [0, 0, 0, 0, 0, 0, 0, 0]
#     for i in range(iter):
#         cards = [start]
#         cards.append(deal(p))
#         while True:
#             # check for soft 17
#             if(1 in cards) and sum(cards) == 7:
#                 res[0] += 1
#                 break
#             elif (1 in cards) and (10 in cards) and len(cards) == 2:
#                 res[6] += 1
#                 break
#             elif 17 <= sum(cards) <= 21:
#                 res[sum(cards)-16] += 1
#                 break
#             elif sum(cards) > 21:
#                 res[-1] += 1
#                 break
#             else:
#                 cards.append(deal(p))
#     k = sum(res)
#     return [p*1.0/k for p in res]


def sim_dealer(start, p, iter=1000):
    return sim_dealer_full([start], p).tolist()


def sim_all(p, iter=1000):
    for i in range(10):
        print i+1, sim_dealer(i+1, p, iter)


# def list_banao(iter=100000, steps=1000):
#     bada_list = []
#     for i in range(steps):
#         p = i*1.0/steps
#         bada_list.append([sim_dealer(s+1, p, iter) for s in range(10)])
#         print i, "completed"
#     return bada_list

# returns outcome of standing with current cards
def calc_stand(cards, dlr):
    total = sum(cards)
    if total > 21:
        return 0
    if (1 in cards) and (10 in cards) and len(cards) == 2:
        # BlackJack
        return 2.5-1.5*(dlr[6])
    if 1 in cards and total <= 11:
        total += 10
    dlr[1] += dlr[0]
    dlr[0] = 0.0
    res = 2*dlr[-1]
    if(total > 16):
        res += 2*sum(dlr[:total-16])+dlr[total-16]
    return res


def sim_mdp(dlr, cards, p, depth=5):
    # check some base cases
    # dlr has dealers result probability
    # 0=soft 17, 1=17,2=18,3=19,4=20,5=21,6=BlackJack,7=Busted
    total = sum(cards)
    if total > 21:
        # busted
        return (0, "S")
    if (1 in cards) and (10 in cards) and len(cards) == 2:
        # BlackJack
        return (2.5-1.5*(dlr[6]), "S")
    if total == 21:
        # I am kinda sure that the best move here is stand, so...
        return (2*(1-dlr[6]), "S")
    else:
        non_face = ((1-p)/9.0)
        stand = calc_stand(cards, dlr)
        hit = non_face * sum([sim_mdp(dlr, cards+[i+1], p)[0]
                              for i in range(9)]) + p*sim_mdp(dlr, cards+[10], p)[0]
        # check if doubling is allowed
        if len(cards) == 2:
            double = 2 * non_face * sum([calc_stand(cards+[i+1], dlr)
                                         for i in range(9)]) + 2*p*calc_stand(cards+[10], dlr)
            # subtract the one additional bet
            double -= 1
        else:
            double = -1
        # check if split is allowed
        if len(cards) == 2 and cards[0] == cards[1] and depth > 0:
            # Check if it is a case of Aces
            if cards[0] == 1:
                split = non_face * sum([calc_stand([1, i+1], dlr)
                                        for i in range(9)]) + p*calc_stand([1, 10], dlr)
                split = 2*split-1
            else:
                split = non_face * sum([sim_mdp(dlr, [cards[0], i+1], p, depth-1)[0]
                                        for i in range(9)]) + p*sim_mdp(dlr, [cards[0], 10], p, depth-1)[0]
                split = 2*split-1
        else:
            split = -1
        return max([(stand, "S"), (hit, "H"), (double, "D"), (split, "P")])


def get_sim(p, start):
    dlr = sim_dealer(start, p, 100000)
    print ". A 2 3 4 5 6 7 8 9 F ."
    for i in range(1, 11):
        print ". A 2 3 4 5 6 7 8 9 F".split()[i],
        for j in range(1, 11):
            print sim_mdp(dlr, [i, j], p)[1],
        print "."


def get_soft(p):
    print ". A 2 3 4 5 6 7 8 9 F ."
    for start in range(1, 11):
        print ". A 2 3 4 5 6 7 8 9 F".split()[start],
        dlr = sim_dealer(start, p, 100000)
        for mc in range(1, 11):
            print sim_mdp(dlr, [1, mc], p)[1],
        print "."


def get_pair(p):
    print ". A 2 3 4 5 6 7 8 9 F ."
    for start in range(1, 11):
        print ". A 2 3 4 5 6 7 8 9 F".split()[start],
        dlr = sim_dealer(start, p, 100000)
        for mc in range(1, 11):
            print sim_mdp(dlr, [mc, mc], p)[1],
        print "."
