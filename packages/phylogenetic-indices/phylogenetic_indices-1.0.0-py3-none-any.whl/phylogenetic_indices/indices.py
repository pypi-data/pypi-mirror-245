import numpy as np


def species_richness(hist: np) -> int:
    """
    Conta o número de espécies de uma imagem com base em um histograma fornecido.

    Parameters:
        hist: A entrada que representa o histograma da imagem.

    Returns:
        O número de espécies presentes no histograma.

    Raises:
        ValueError: Se o tipo de características não for suportado (não é uma array NumPy).

    Examples:
        >>> import numpy as np
        >>> hist = np.array([1, 2, 3, 1, 2, 3, 4])
        >>> species_richness(hist)
        7
    """
    if not isinstance(hist, np.ndarray):
        raise ValueError('Unsupported data type')

    return len(hist)


def taxonomic_distinction(hist: np) -> float:
    """
    Calcula o índice de distinção taxonômica.

    O índice de distinção taxonômica (∆∗) calcula a distância taxonômica média entre dois indivíduos de espécies diferentes

    Args:
      hist: Histograma de abundância de espécies.

    Returns:
      O índice de distinção taxonômica.

    Raises:
        ValueError: Se o tipo de características não for suportado (não é uma array NumPy).

    Examples:
        >>> import numpy as np
        >>> hist = np.array([10, 20, 30])
        >>> taxonomic_distinction(hist)
        1.2727272727272727
    """

    if not isinstance(hist, np.ndarray):
        raise ValueError('Unsupported data type')

    richness = species_richness(hist)

    taxonomic_diversity_distancies = []
    individual_number_products = []

    for i in range(richness):
        taxonomic_distance = 0
        individual_number_product = 0
        for j in range(richness):
            if i < j:
                dist = abs(i - j)
                taxonomic_distance += dist * hist[i] * hist[j]
                individual_number_product += hist[i] * hist[j]

        taxonomic_diversity_distancies.append(taxonomic_distance)
        individual_number_products.append(individual_number_product)

    taxonomic_diversity = np.sum(taxonomic_diversity_distancies) / (
        np.sum(individual_number_products)
    )

    return taxonomic_diversity


def taxonomic_diversity(hist: np) -> float:
    """
    Calcula o índice de diversidade taxonômica.

    O índice de diversidade taxonômica (∆) calcula a distância taxonômica média entre dois indivíduos escolhidos aleatoriamente em uma comunidade

    Args:
      hist: Histograma de abundância de espécies.

    Returns:
        O índice de diversidade taxonômica.

    Examples:
        >>> import numpy as np
        >>> hist = np.array([10, 20, 30])
        >>> taxonomic_diversity(hist)
        0.7909604519774012
    """

    if not isinstance(hist, np.ndarray):
        raise ValueError('Unsupported data type')

    richness = species_richness(hist)

    taxonomic_diversity_distancies = []
    for i in range(richness):
        taxonomic_distance = 0
        for j in range(richness):
            if i < j:
                dist = abs(i - j)
                taxonomic_distance += dist * hist[i] * hist[j]

        taxonomic_diversity_distancies.append(taxonomic_distance)

    total_number_species = np.sum(hist)

    taxonomic_diversity = (
        2
        * np.sum(taxonomic_diversity_distancies)
        / (total_number_species * (total_number_species - 1))
    )

    return taxonomic_diversity


def extensive_quadratic_entropy(hist: np) -> float:

    """
    Calcula a extensa entropia quadrática (F)

    A extensa entropia quadrática (F) calcula a soma de todas as distâncias filogenéticas pareadas.

    Args:
      hist: Histograma de abundância de espécies.

    Returns:
        A extensa entropia quadrática (F).

    Examples:
        >>> import numpy as np
        >>> hist = np.array([10, 20, 30])
        >>> extensive_quadratic_entropy(hist)
        8

    """

    if not isinstance(hist, np.ndarray):
        raise ValueError('Unsupported data type')

    richness = species_richness(hist)

    taxonomic_diversity_distancies = []
    for i in range(richness):
        taxonomic_distance = 0
        for j in range(richness):
            dist = abs(i - j)
            taxonomic_distance += dist

        taxonomic_diversity_distancies.append(taxonomic_distance)

    return np.sum(taxonomic_diversity_distancies)


def intensive_quadratic_entropy(hist: np) -> float:

    """
    Calcula o índice de entropia quadrática intensiva (J)

    O índice de entropia quadrática intensiva (J) é a distância filogenética média entre duas espécies escolhidas aleatoriamente.

    Args:
      hist: Histograma de abundância de espécies.

    Returns:
        O índice de entropia quadrática intensiva (J).

    Examples:
        >>> import numpy as np
        >>> hist = np.array([10, 20, 30])
        >>> intensive_quadratic_entropy(hist)
        0.8888888888888888

    """

    if not isinstance(hist, np.ndarray):
        raise ValueError('Unsupported data type')

    richness = species_richness(hist)

    quadratic_entropy = extensive_quadratic_entropy(hist) / richness**2

    return quadratic_entropy
