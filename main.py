# This is an example of how one can use the calculator.
# It represents one round of damage as a gloomstalker ranger from 5th edition.

import matplotlib.pyplot as plt
import numpy as np
import critcalc as cc

def one_roll(ac):
  dmgDice = np.array([[6,0],[6,0],[8,0]]) # Hunter's mark and dread ambusher
  dmgMod  = 14                            # Includes sharpshooter

  probs = cc.get_dmg_pdf(ac, np.array([[20,0]]), 5, dmgDice, dmgMod)
  plt.errorbar(range(len(probs)),probs,None,0.5,linestyle='')
  plt.xlabel("Damage")
  plt.ylabel("Probability")
  plt.show()

def advantage_compare():
  dmgDice = np.array([[6,0],[6,0],[8,0]]) # Hunter's mark and dread ambusher
  dmgMod  = 14                            # Includes sharpshooter
  ac = range(35)

  for adv in range(-1,3):
    avgs, meds, los, his = cc.get_dmg_vs_ac(np.array([[20,adv]]), 5, dmgDice, dmgMod)
    #plt.plot(ac, meds, label="median damage")
    plt.errorbar(ac, avgs,None,0.5,linestyle='', label="average damage")
    #plt.fill_between(ac, los, his, color='b', alpha=.1, label="68th percentile")
  plt.xlabel("Enemy AC")
  plt.ylabel("Damage")
  #plt.legend()
  plt.show()

def avg_median_compare():
  dmgDice = np.array([[6,0],[6,0],[8,0]]) # Hunter's mark and dread ambusher
  dmgMod  = 14                            # Includes sharpshooter
  ac = range(35)

  avgs, meds, los, his = cc.get_dmg_vs_ac(np.array([[20,0]]), 5, dmgDice, dmgMod)
  plt.errorbar(ac, avgs,None,0.5,linestyle='', label="average damage")
  plt.plot(ac, meds, label="median damage")
  #plt.plot(ac, his, label="84th percentile")
  #plt.plot(ac, los, label="16th percentile")
  plt.fill_between(ac, los, his, color='b', alpha=.1, label="68th percentile")
  plt.xlabel("Enemy AC")
  plt.ylabel("Damage")
  plt.legend()
  plt.show()

def main():
  one_roll(10)
  advantage_compare()
  avg_median_compare()

if __name__=="__main__":
    main()

