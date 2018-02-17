# parkinson-detection

## Description
A machine learning based approach to detecting the presence of Parkinson's disease from spiral tests of patients. The dataset was obtained from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Parkinson+Disease+Spiral+Drawings+Using+Digitized+Graphics+Tablet).

The dataset contains tests of 15 people from the control group and 62 tests of people suffering from Parkinson's disease.

### Results-
We tested several classification algorithms such as Logistic Regression, Random Forest, SVM etc. The best results were obtained using SVM-

| Accuracy  | 100 % |
|-----------|-------|
| F1        | 0.66  |
| Precision | 0.5   |
| Recall    | 1     |

## Future work
As indicated in Results, not all handwriting tasks provide the same level of discrimination power. After evaluating our results, it is evident that some features are more useful for diagnosis than others. We can use actual handwriting to improve on our results.

Decision support tools are gaining significant research interest due to their potential to improve health-care provision. Among many possible approaches, those that provide noninvasive monitoring and diagnosis of diseases are of increased interest to clinicians and biomedical engineers.

We aim to provide this diagnosis to people in remote areas where healthcare is not just lacking but extremely inadequate.


## References
1. [Analysis of in-air movement in handwriting: A novel marker for Parkinson’s disease](https://www.sciencedirect.com/science/article/pii/S0169260714003204)
2. [Evaluation of handwriting kinematics and pressure for differential diagnosis of Parkinson’s disease](https://www.sciencedirect.com/science/article/pii/S0933365716000063)
3. [Parkinson's Foundation: Better Lives. Together.](http://parkinson.org/understanding-parkinsons)
4. [Parkinson's Disease Information Page | National Institute of Neurological Disorders and Stroke](https://www.ninds.nih.gov/Disorders/All-Disorders/Parkinsons-Disease-Information-Page)
