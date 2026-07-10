import numpy as np


def solve_least_square(
    A: np.ndarray,
    b: np.ndarray,
    
    )-> tuple[np.ndarray, float]:

    """
    Solves least square, setting coeficient at index "coeficient_equalto_1" = 1.
    Solves least square of Ax=b. 

    
    returns solution to leas square problem. 
    also returns least_square_cost 
    
    """

    #Må unngå 0-løsning
    #Tror jeg må lage en ny formel for
    #least square siden c1 = 1 tvinger
    #frem noe. Men samtidig kan jo likningen alltid skaleres. 
    #Vi mister ikke noe info hvis det skjer
    #Jeg synes også det gir mye mer mening å ha noe periodisk på høyreside som sin og cos. 
    #Det virker hvertfall helt feil å ha lav orden polynom


    #left_side = np.transpose(A)@A
    #right_side = 

    x = (np.invert(np.transpose(A)@A))@np.transpose(A)*b
    cost = np.sum((A@x-b)**2)
    return x, cost

    
     
