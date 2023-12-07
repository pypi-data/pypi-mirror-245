from enum import Enum


class LossType(Enum):
  """
  Implemented Loss Functions

  - ":math:`h(\mathbf{x}) = \mathbf{w} \cdot \mathbf{x} + b`" is a linear classifier.
  - The hyperplane  :math:`h` defined by this equation represents the decision boundary that separates classes in a linearly separable space.
  - The hypothesis space :math:`H` consists of all possible linear classifiers.

  Let :math:`\hat{h}^{(D)}` be the best empirical classifier in the dictionary :math:`H` for the dataset :math:`D` with :math:`d` features and :math:`n` samples, i.e., the classifier :math:`h` in :math:`H` with the minimum empirical error rate. Under these conditions, we can define three error rates:
    - :math:`L(\hat{h}^{(D)}) =` the theoretical error rate of the classifier :math:`\hat{h}^{(D)}`
    - :math:`\hat{L}(\hat{h}^{(D)}) =` the empirical error rate of the classifier :math:`\hat{h}^{(D)}`
    - :math:`\hat{L}(\hat{h}^{(D)},D') =` the empirical error rate of the classifier :math:`\hat{h}^{(D)}` using a test dataset :math:`D'`

  The Bayes Error (also: Bayes Risk) is defined as the minimum theoretical achievable error rate:
      - :math:`\min_{h\in H} L(h) =` the smallest theoretically achievable error rate for a classifier :math:`h` in dictionary :math:`H`.

  Attributes:
    - THEORETICAL: estimated using probability theory
    - EMPIRICALTRAIN: estimated using empirical approach with train data
    - EMPIRICALTEST: estimated using empirical approach with test data

  """
  THEORETICAL = 'THEORETICAL'
  EMPIRICALTRAIN = 'EMPIRICAL_TRAIN'
  EMPIRICALTEST = 'EMPIRICAL_TEST'


class DictionaryType(Enum):
  """Implemented Dictionary Types

  Attributes:
    - LINEAR: dictionary with linear classifiers

  """

  LINEAR = 'LINEAR'
