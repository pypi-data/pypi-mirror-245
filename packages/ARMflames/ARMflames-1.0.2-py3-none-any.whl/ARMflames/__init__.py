import ARMflames.FLAMES as fl
import ARMflames.Split as sp
import ARMflames.gui as ui
import sys

__version__=1.0.2
__doc__="""\nThis Is Fun Games
\n To Campare Between two person Relationship Prediction in this game\n

import ARMflames as d\n
d.getnames()

\n This function returns the given two person Relationship Prediction :

    Prediction Means

    FLAMES :
      * Friends   --- Your Relationship is Friends...
      * Love      --- Your Relationship is Loving...
      * Affection --- Your Relationship is Affection...
      * Marriage  --- Your Relationship is Marriage...
      * Enemy     --- Your Relationship is Enemy...
      * Sibilings --- Your Relationship is Siblings...

"""
try:
    def getnames():
        a=input("Enter The Name 1:")
        b=input("Enter The Name 2:")
        s=sp.setnames(a,b)
        return s
    def gui():
        ui.UI()
    if __name__=='__main__':
        print(fl.times(getnames()))
except Exception as Argument:
    print("The Error Argument:"+Argument)