# MLHessian-TSopt

This repository contains wrapper scripts for running and analyzing transition state calculations using NewtonNet deep learning model and Sella optimizer.

## Script overview

- `Scripts/split.ipynb`: Wrapper notebook for model training data splitting from Transition-1x dataset with augmentation from ANI-1x dataset.
- `Scripts/test.ipynb`: Wrapper notebook for model testing using the holdout test reactions in Transition-1x dataset.
- `Scripts/noise.ipynb`: Wrapper notebook for initial guess geometry generation and subsequent noising of Sella benchmark reactions.
- `Scripts/opt/nn_sella_quacc.py`: Wrapper script for NewtonNet-based optimizations.
- `Scripts/opt/dft_sella_quacc.py`: Wrapper script for DFT (Density Functional Theory) method, specifically using the wb97x/6-31G* level of theory.
- `Scripts/gather.ipynb`: Wrapper notebook for optimization data retrieval.

## Models

- `Models/PretrainedModels/training_1`: Pre-trained model in NewtonNet paper, trained on ANI dataset.
- `Models/PretrainedModels/training_9`: Pre-trained model in NewtonNet paper, trained on ANI-1x dataset.
- `Models/FinetunedModels/training_44`: Fine-tuned model from `training_1` above, trained on Transition-1x dataset composition split 5.
- `Models/FinetunedModels/training_56`: Fine-tuned model from `training_1` above, trained on Transition-1x dataset composition split 5.
- `Models/FinetunedModels/training_64`: Fine-tuned model from `training_1` above, trained on Transition-1x dataset composition split 51.
- `Models/FinetunedModels/training_63`: Fine-tuned model from `training_1` above, trained on Transition-1x dataset composition split 52.
- `Models/FinetunedModels/training_58`: Fine-tuned model from `training_1` above, trained on Transition-1x dataset composition split 53.
- `Models/FinetunedModels/training_52`: Fine-tuned model from `training_1` above, trained on Transition-1x dataset conformation split 0.
- `Models/FinetunedModels/training_54`: Fine-tuned model from `training_1` above, trained on Transition-1x dataset conformation split 1.
- `Models/FinetunedModels/training_53`: Fine-tuned model from `training_1` above, trained on Transition-1x dataset conformation split 2.
- `Models/FinetunedModels/training_55`: Fine-tuned model from `training_1` above, trained on Transition-1x dataset conformation split 3.

## Analysis

- `Analysis/Figure1b.ipynb`: Wrapper notebook for dataset interatomic distance distribution analysis.
- `Analysis/Figure1cd.ipynb` and `Analysis/FigureS1.ipynb`: Wrapper notebook for model testing regarding energy and force predictions.
- `Analysis/Figure2.ipynb` and `Analysis/Figure4bc.ipynb`: Wrapper notebook for model testing regarding Hessian predictions.
- `Analysis/Figure3.ipynb`: Wrapper notebook for optimization path comparisons.
- `Analysis/Figure4c.ipynb`: Wrapper notebook for optimized transition state comparisons.
- `Analysis/Figure4abd.ipynb`: Wrapper notebook for optimized reactant/product comparisons.

## Note

For detailed information on setup and configuration, please refer to the following:

1. **Sella Package:**
   - [GitHub Repository](https://github.com/zadorlab/sella)
   - [Documentation](https://github.com/zadorlab/sella/wiki)

2. **NewtonNet:**
   - [GitHub Repository](https://github.com/THGLab/NewtonNet)

3. **QuAcc Recipes for NewtonNet and QChem:**
   - [GitHub Repository](https://github.com/Quantum-Accelerators/quacc/blob/main/src/quacc/recipes/newtonnet/ts.py)
   - [Documentation](https://quantum-accelerators.github.io/quacc/reference/quacc/recipes/newtonnet/ts.html)

4. **Corresponding Paper Authors:**
   - Feel free to reach out to them (including me) for assistance.
