from sklearn.model_selection import train_test_split
import numpy as np

class PreProcessador:

    def __init__(self):
        """Inicializa o preprocessador."""
        pass

    def preparar_form(self, form):
        """ Prepara os dados recebidos do front para serem usados no modelo. """
        
        # A ordem dos atributos DEVE ser a mesma usada no treinamento do modelo
        # Ordem do notebook: ['thal', 'ca', 'cp', 'oldpeak', 'thalach', 'exang', 'age']
        X_input = np.array([form.thal, 
                            form.ca, 
                            form.cp, 
                            form.oldpeak, 
                            form.thalach, 
                            form.exang, 
                            form.age
                        ])
        # Faremos o reshape para que o modelo entenda que estamos passando um único registro
        X_input = X_input.reshape(1, -1)
        return X_input
