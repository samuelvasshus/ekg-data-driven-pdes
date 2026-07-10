import numpy as np

#from ekgpde import parameters

def build(
        u_hat: np.ndarray,
        w: np.ndarray,
        f_hat: np.ndarray,
        polynomal_degree_right: int,
        coeficient_equalto_1: int,
    )-> tuple[np.ndarray, np.ndarray]:
    """
    Algorithm:
    Builds A_matrix for least square methode 
    Builds A so that coeficient at index at coeficient_equalto_1 = 1

    Algorithm is to ignore first column of A and make a new matrix M. and set b = -A_m_1. In other words
    b = - first_column_A. Then solve least square of this new system. This forces c_1 = 1. same logic for c_2, c_3...


    returns A and b.
    """

    A = np.zeros((3 + polynomal_degree_right + 1, len(u_hat)),dtype=complex)

    for i in range(3):
        A[i] = u_hat*(1j*w)**i

    for i in range (polynomal_degree_right + 1):
        A[3 + i] = -f_hat[i]


        

    #Tar transponert for å få Matriseegenskaper
    A = np.transpose(A)

    b = -A[:, coeficient_equalto_1].copy()
    #b= np.delete(b, coeficient_equalto_1)
    A = np.delete(A, coeficient_equalto_1, axis=1)


    return A, b
    