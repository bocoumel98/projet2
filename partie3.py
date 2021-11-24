#class pile 
class Pile:
    def __init__(self):
       self.element = []
    ''' Insere un noeud en tete de la pile'''
    def push(self,noeud):
        self.element.append(noeud)
    '''   Retire le noeud en tete de la pile'''
    '''
       True si  un noeud est dans la pile 
    '''
    def  contains_noeud(self,name):
        for i in self.element:
            if i.name == name:
                return True
        return False
    ''' 
     return true if the pile is empty
    '''
    def empty(self):
        if len(self.element)==0:
            return True
        else:
            return False
    '''
    Retourne et supprime l'element en tete de pile  
     Retourne une exception si la pile est vide
    '''
    def remove(self):
        if self.empty():
            raise Exception("Pile vide")
        else:
            return self.element.pop()
#Test de la classe Pile
p = Pile() 
#faire des push par default
p.push("Mamadou")   
p.push("Binta")
p.push("Tidiane")
p.push("Coumba")
#afficher la pile en l'inverser
print(p.element[::-1])
p.remove()
print(p.element[::-1])
#Implémentation de la classe File par héritage
class File(Pile):
  '''
  Classe File: voir les definitions ci-dessous Premier arrive premier servi : FIFO
  La classe dispose d'une structure de type list pour ranger les données
  Les éléments sont enfilés (insérés) du coté arrière et défilés (retirés) du coté avant
  File et Pile peuvent partager certaines methodes donc utilisez l'heritagepour definir la classe File. 
  '''
  def __init__(self):
    super().__init__()
  def enfiler(self,noeud):
    self.push(noeud)
  
  def remove(self):
      if self.element==[]:
          raise Exception("File vide")
      else:
            return self.element.pop(0)
  def empty(self):
    return super().empty()
  def contains_noeud(self,name):
    return super().contains_noeud(name)
  def __str__(self):
    return str(self.element[::1])
#Test de la classe File
f = File()
f.enfiler("Oumou")
f.enfiler("Farmata")
f.enfiler("Penda")
f.enfiler("Salif")
print(f)
f.remove()
print(f)

#afficher la 
          




    


