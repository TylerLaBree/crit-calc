# Tyler's Tabletop Calculator: Crit-Calc

import numpy as np

### Terminology ###
# res:    the result of a roll or series of rolls.
# die:    the number of sides on a die.
# adv:    advantage score. e.g: -1, 0, and 1 for disadvantage, normal, and 
#           advantage, respectively.
# k1:     return one die roll.
# sum:    return the sum of all die rolls.
# prob:   probability.
# pdf:    probability density function.

def get_roll_result_k1_prob(res, die=20, adv=0):
  if  not(0 < res and res <= die):
    return 0
  if adv >= 0:
    numDice=1+adv
  else:
    numDice=1-adv
    res = 21-res
  return (res**numDice - (res-1)**numDice) / (die**numDice)

def get_roll_result_k1_pdf(die, adv):
  probs = np.zeros([die+1])
  for res in range(die+1):
    probs[res] = get_roll_result_k1_prob(res, die, adv)
  return probs

def get_roll_result_sum_pdf(dice, mod, acc=np.array([1])):
  if len(dice) == 0:
    acc1 = np.zeros([len(acc) + mod])
    for i in range(len(acc)):
      acc1[i+mod] = acc[i]
    return acc1
  probs = get_roll_result_k1_pdf(dice[0,0], dice[0,1])
  acc1 = np.zeros([len(acc) + len(probs)-1])
  for i in range(len(acc)):
    for j in range(len(probs)):
      acc1[i+j] += acc[i] * probs[j]
  return get_roll_result_sum_pdf(dice[1:], mod, acc1)

def get_pass_prob(threshold, dice, mod):
  pdf = get_roll_result_sum_pdf(dice, mod)
  acc = 0
  for res in range(len(pdf)):
    if res >= threshold:
      acc += pdf[res]
  return acc 

def get_equals_prob(criteria, dice, mod):
  pdf = get_roll_result_sum_pdf(dice, mod)
  acc = 0
  for res in range(len(pdf)):
    for criterion in criteria:
      if res == criterion:
        acc += pdf[res]
  return acc 
  
def get_dmg_pdf(threshold, attDice, attMod, dmgDice, dmgMod, crits=np.array([20])):
  maxDmg = dmgMod 
  maxAttRoll = 0
  for dmgDie in dmgDice:
    maxDmg += 2*dmgDie[0]
    maxAttRoll += dmgDie[0]
  pdf = np.zeros([maxDmg])
  critProb = get_equals_prob(crits, attDice, attMod)
  hitProb = get_pass_prob(threshold, attDice, attMod) - critProb
  missProb = 1 - hitProb - critProb
  hitDmgs = get_roll_result_sum_pdf(dmgDice, dmgMod)
  critDmgs = get_roll_result_sum_pdf(dmgDice, dmgMod + maxAttRoll)
  for i in range(maxDmg):
    if i<len(hitDmgs):
      pdf[i] += hitProb * hitDmgs[i]
    if i<len(critDmgs):
      pdf[i] += critProb * critDmgs[i]
  pdf[0] += missProb
  return pdf

def get_dmg_avg(probs):
  top = 0
  bot = 0
  for dmg in range(len(probs)):
    top += probs[dmg] * dmg
    bot += probs[dmg]
  return top / bot

def get_dmg_std(probs, avg):
  top = 0
  bot = 0
  for dmg in range(len(probs)):
    bot += probs[dmg]
    top += probs[dmg] * dmg**2
  return np.sqrt(top/bot - avg**2)

def get_percentile(probs, perc):
  acc = 0
  for res in range(len(probs)):
    if acc + probs[res] >= perc:
      c = (perc - acc)/probs[res]
      return res - 1 + c
    acc += probs[res]
  return -1

def get_dmg_vs_ac(attDice, attMod, dmgDice, dmgMod, crits=np.array([20])):
  maxAC = 35
  avgs = np.zeros(maxAC)
  meds = np.zeros(maxAC)
  los = np.zeros(maxAC)
  his = np.zeros(maxAC)
  #stds = np.zeros(maxAC)
  for ac in range(maxAC):
    probs = get_dmg_pdf(ac, attDice, attMod, dmgDice, dmgMod, crits)
    avgs[ac] = get_dmg_avg(probs)
    meds[ac] = get_percentile(probs, 0.5)
    los[ac] = get_percentile(probs, 0.158655)
    his[ac] = get_percentile(probs, 0.841345)
    #stds[ac] = get_dmg_std(probs, avgs[ac])
  return avgs, meds, los, his

