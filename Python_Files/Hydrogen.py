import Atom
import Axis
import Site
import Oxygen

class Hydrogen(Atom):

    def __init__(self, posX, posY, posZ):
        super().__init__(posX, posY, posZ)

    def addChemBond(self, atom):
        if len(self.getChemBonds()) == 1:
            print("This Hydrogen already has a chemical bond")
            return

        elif isinstance(atom, Oxygen):
            self.getChemBonds().append(atom)

        else:
            print("That is not an Oxygen Atom")
            return
        return
    

    def getChemBonds(self):
        if len(self.getChemBonds()) == 0:
            print("This Hydrogen has no Chemical Bonds")
            return null
        else:
            return self.getChemBonds()[0]

    def removeBond(self):
        if len(self.getChemBonds()) == 0:
            return
        else
            self.getChembonds().pop(0)


