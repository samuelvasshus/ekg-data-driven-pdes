import numpy as np

#from ekgpde import parameters

def new_build(
        u_hat_derivs: np.ndarray,
        w: np.ndarray,
        f_hat: np.ndarray,
        polynomal_degree_right: int,
        coeficient_equalto_1: int,
    )-> tuple[np.ndarray, np.ndarray]:
    """
    U_hat_derivs is a matrix with different order deriativs


    Algorithm:
    Builds A_matrix for least square methode 
    Builds A so that coeficient at index at coeficient_equalto_1 = 1

    Algorithm is to ignore first column of A and make a new matrix M. and set b = -A_m_1. In other words
    b = - first_column_A. Then solve least square of this new system. This forces c_1 = 1. same logic for c_2, c_3...


    returns A and b.
    """

    A = np.zeros((len(u_hat_derivs) + polynomal_degree_right + 1, len(u_hat_derivs[0])),dtype=complex)

    
    

    #Her er j komplex og i index. Litt forvirrende notasjon. 
    #A = np.zeros(( + polynomal_degree_right + 1, len(u_hat)),dtype=complex)
    for i in range (polynomal_degree_right + 1):
        A[i] = f_hat[i]

    for i in range(len(u_hat_derivs)):
        A[i + polynomal_degree_right + 1] = u_hat_derivs[i]
    

    #Tar transponert for å få Matriseegenskaper
    A = np.transpose(A)

    A_real = np.vstack([
        A.real,
        A.imag,
    ]) 
    print("Shape A_real")
    print(A_real.shape)

    


        

    

    b_real = -A_real[:, coeficient_equalto_1].copy()
    
    print("Shape b_real")
    print(b_real.shape)
    
    #b= np.delete(b, coeficient_equalto_1)
    A_real = np.delete(A_real, coeficient_equalto_1, axis=1)


    return A_real, b_real
    