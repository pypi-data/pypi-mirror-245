
import numpy as np

class LassoRegression:
    def __init__(self, alpha=1.0, max_iter=1000, tol=1e-4):
        self.alpha = alpha  # Regularization strength
        self.max_iter = max_iter  # Maximum number of iterations for optimization
        self.tol = tol  # Tolerance to determine convergence
        self.weights = None  # Coefficients


    def fit(self, X, y):
        # Initialize coefficients with zeros
        self.weights = np.zeros(X.shape[1] + 1)
        X_augmented = np.column_stack([np.ones(X.shape[0]), X])
        cost, gradient = self._cost_and_gradient(X_augmented, y, self.weights)

        for iteration in range(self.max_iter):

            self.weights -= self.alpha * gradient
            new_cost, new_gradient = self._cost_and_gradient(X_augmented, y, self.weights)
            if np.abs(new_cost - cost) < self.tol:
                break
            cost, gradient = new_cost, new_gradient

    def _cost_and_gradient(self, X, y, weights):
        n_samples   = X.shape[0]
        predictions = np.dot(X, weights)
        residuals   = predictions - y
        cost        = (1 / (2 * n_samples)) * np.sum(residuals**2)
        l1_term     = self.alpha * np.sum(np.abs(weights[1:]))
        total_cost  = cost + l1_term
        gradient    = (1 / n_samples) * np.dot(X.T, residuals) + self.alpha * np.sign(weights)
        gradient[0] -= self.alpha * np.sign(weights[0])  # Exclude the intercept term
        return total_cost, gradient

    def predict(self, X):
        X_augmented = np.column_stack([np.ones(X.shape[0]), X])
        return np.dot(X_augmented, self.weights)
