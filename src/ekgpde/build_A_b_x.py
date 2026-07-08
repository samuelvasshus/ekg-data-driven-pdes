import numpy as np

#from ekgpde import parameters

def build(
        u_hat: np.ndarray,
        w: np.ndarray,
        f_hat: np.ndarray,
        polynomal_degree_right: int,
    )-> np.ndarray:
    """
    Algorithm:
    Builds A_matrix for least square methode 
    """

    A = np.zeros(3 + polynomal_degree_right + 1)

    for i in range(3):
        A[i] = u_hat*(1j*w)**i

    for i in range (polynomal_degree_right + 1):
        A[3 + i] = f_hat[i]


        

    #Tar transponert for å få Matriseegenskaper
    return np.transpose(A)

    