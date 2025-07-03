import numpy as np
from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

import warnings
from typing import Dict, Any, Tuple
warnings.filterwarnings('ignore')


def cv_trainer(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    cv: int,
    models: Dict[str, Tuple[BaseEstimator, Dict[str, Any]]]
) -> Dict[str, Dict[str, Any]]:
    def train_single_model(name: str, estimator: BaseEstimator, param_grid: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Training {name}...")

        grid_search = GridSearchCV(
            estimator=estimator,
            param_grid=param_grid,
            cv=cv,
            scoring='accuracy',
            n_jobs=-1,
            verbose=2
        )

        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_
        test_predictions = best_model.predict(X_test)  # type: ignore
        test_score = accuracy_score(y_test, test_predictions)

        results = {
            'best_estimator': best_model,
            'best_params': grid_search.best_params_,
            'best_cv_score': grid_search.best_score_,
            'cv_results': grid_search.cv_results_,
            'test_score': test_score,
            'test_predictions': test_predictions
        }

        print(
            f"{name} - Best CV Score: {grid_search.best_score_:.4f}, Test Score: {test_score:.4f}")
        return results

    all_results = {}

    for model_name, (estimator, param_grid) in models.items():
        try:
            model_results = train_single_model(
                model_name, estimator, param_grid)
            all_results[model_name] = model_results
        except Exception as e:
            print(f"Error training {model_name}: {str(e)}")
            all_results[model_name] = {'error': str(e)}

    best_model_name = None
    best_test_score = -1

    for name, results in all_results.items():
        if 'test_score' in results and results['test_score'] > best_test_score:
            best_test_score = results['test_score']
            best_model_name = name

    summary = {
        'best_model_name': best_model_name,
        'best_test_score': best_test_score,
    }

    all_results['summary'] = summary
    print(
        f"\nBest Model: {best_model_name} (Test Score: {best_test_score:.4f})")

    return all_results


def is_in_colab():
    try:
        import google.colab  # type: ignore
        return True
    except ImportError:
        return False
