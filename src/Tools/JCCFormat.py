#using the pickle library to save and load data into a file with any extension
#The file extension doesn't matter to the pickle library, as it simply processes the data
#as a byte stream.
import pickle


class JCCFormat :
    '''
    class that allows to create and interact with .jcc format files    
    '''
    def save (fichier,infos):
        with open(fichier, "wb") as fichier:
            pickle.dump(infos, fichier)

    def load (fichier):
        with open(fichier, "rb") as fichier:
            donnees = pickle.load(fichier)
        
        return donnees 
    
    def display_data(file):
        data = JCCFormat.load(file)
        for element in data :
            print(element,": ",data[element]," type: ",type(data[element]))
    
if __name__ == "__main__":
    path = r"C:\Users\marai\Desktop\GitHub\Joy-Con_Control\src\Ressources\Configuration\Controllers_configuration"
  