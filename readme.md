# Buying Product Prediction Tool

A Fuzzy Expert System for predicting the likelihood of a customer buying a product based on their age, income, and purchase history

## Project Overview

This project involves the development of a Fuzzy Expert System designed to predict the likelihood of a customer buying a product based on three key input factors: age, income, and purchase history. The system leverages fuzzy logic to handle the inherent uncertainty and vagueness in customer behavior.

## Input Variables

1. **Age**:
   - Young
   - Middle-aged
   - Old

2. **Income**:
   - Low
   - Medium
   - High

3. **Purchase History**:
   - Rarely
   - Occasionally
   - Frequently

## Fuzzy Rules

The system is governed by a set of 27 fuzzy rules that define how the input variables interact to produce the output. These rules are designed to mimic the decision-making process of a human expert.

## Testing the System

To validate the accuracy and reliability of the Fuzzy Expert System, a test set of 100 rules with expected outputs is generated. These test cases span a wide range of possible input combinations to ensure comprehensive coverage and robustness of the system.

## Getting Started

### Running the System

To run the system on your computer, you need a version of Python installed and you should install the main libraries by running the following commands in the terminal:

```bash
pip install numpy
pip install skfuzzy
pip install matplotlib
pip install streamlit
```

Next, navigate to the project directory in the terminal and run the following command to start the application:

```bash
streamlit run fuzzy_project_ui.py
```


The system interface will appear, and you can start using it fully.

### Expected Results

The system will output the predicted likelihood for each test case and compare it with the expected output. The results will be logged for further analysis.

## Acknowledgements

This project uses the scikit-fuzzy library for implementing fuzzy logic in Python.

---

Feel free to explore, modify, and enhance this project to suit your needs. Happy coding!
