"""
Standalone Machine Learning Estimators & Transformers for AgriSense AI.
Pure NumPy implementations ensuring 100% platform portability and zero binary DLL issues.
"""

import numpy as np
import pandas as pd


class StandardScaler:
    """Standardizes numerical features by removing the mean and scaling to unit variance."""

    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit(self, X):
        X = np.asarray(X, dtype=float)
        self.mean_ = np.mean(X, axis=0)
        self.scale_ = np.std(X, axis=0)
        self.scale_[self.scale_ == 0.0] = 1.0  # Prevent division by zero
        return self

    def transform(self, X):
        X = np.asarray(X, dtype=float)
        return (X - self.mean_) / self.scale_

    def fit_transform(self, X):
        return self.fit(X).transform(X)


class OneHotEncoder:
    """One-hot encodes categorical features."""

    def __init__(self):
        self.categories_ = []

    def fit(self, X):
        X = np.asarray(X, dtype=str)
        self.categories_ = [sorted(list(set(X[:, col]))) for col in range(X.shape[1])]
        return self

    def transform(self, X):
        X = np.asarray(X, dtype=str)
        encoded_cols = []
        for col, cats in enumerate(self.categories_):
            cat_map = {c: i for i, c in enumerate(cats)}
            one_hot = np.zeros((X.shape[0], len(cats)), dtype=float)
            for row in range(X.shape[0]):
                val = X[row, col]
                if val in cat_map:
                    one_hot[row, cat_map[val]] = 1.0
            encoded_cols.append(one_hot)
        return np.hstack(encoded_cols)

    def fit_transform(self, X):
        return self.fit(X).transform(X)


class ColumnTransformer:
    """Applies numerical scaling and categorical encoding to specified DataFrame columns."""

    def __init__(self, num_cols, cat_cols):
        self.num_cols = num_cols
        self.cat_cols = cat_cols
        self.num_scaler = StandardScaler()
        self.cat_encoder = OneHotEncoder()

    def fit(self, df):
        num_data = df[self.num_cols].values
        cat_data = df[self.cat_cols].values
        self.num_scaler.fit(num_data)
        self.cat_encoder.fit(cat_data)
        return self

    def transform(self, df):
        num_data = df[self.num_cols].values
        cat_data = df[self.cat_cols].values
        num_transformed = self.num_scaler.transform(num_data)
        cat_transformed = self.cat_encoder.transform(cat_data)
        return np.hstack([num_transformed, cat_transformed])

    def fit_transform(self, df):
        return self.fit(df).transform(df)


class Node:
    """Decision Tree Node."""
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    @property
    def is_leaf(self):
        return self.value is not None


class DecisionTreeClassifier:
    """CART Decision Tree Classifier with Gini Impurity."""

    def __init__(self, max_depth=10, min_samples_split=2, random_state=42):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.random_state = random_state
        self.root = None
        self.classes_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        self.root = self._grow_tree(X, y)
        return self

    def _gini(self, y):
        _, counts = np.unique(y, return_counts=True)
        probs = counts / len(y)
        return 1.0 - np.sum(probs ** 2)

    def _best_split(self, X, y):
        best_gain = -1.0
        split_idx, split_thresh = None, None
        current_gini = self._gini(y)
        n_samples, n_features = X.shape

        for feat_idx in range(n_features):
            X_column = X[:, feat_idx]
            thresholds = np.unique(X_column)
            for thresh in thresholds:
                left_mask = X_column <= thresh
                right_mask = ~left_mask

                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue

                n_l, n_r = np.sum(left_mask), np.sum(right_mask)
                gain = current_gini - ((n_l / n_samples) * self._gini(y[left_mask]) +
                                       (n_r / n_samples) * self._gini(y[right_mask]))

                if gain > best_gain:
                    best_gain = gain
                    split_idx = feat_idx
                    split_thresh = thresh

        return split_idx, split_thresh

    def _grow_tree(self, X, y, depth=0):
        n_samples = X.shape[0]
        n_labels = len(np.unique(y))

        # Stopping conditions
        if depth >= self.max_depth or n_labels == 1 or n_samples < self.min_samples_split:
            # Majority vote
            vals, counts = np.unique(y, return_counts=True)
            return Node(value=vals[np.argmax(counts)])

        feat_idx, thresh = self._best_split(X, y)
        if feat_idx is None:
            vals, counts = np.unique(y, return_counts=True)
            return Node(value=vals[np.argmax(counts)])

        left_mask = X[:, feat_idx] <= thresh
        left = self._grow_tree(X[left_mask], y[left_mask], depth + 1)
        right = self._grow_tree(X[~left_mask], y[~left_mask], depth + 1)
        return Node(feature=feat_idx, threshold=thresh, left=left, right=right)

    def _traverse_tree(self, x, node):
        if node.is_leaf:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        return np.array([self._traverse_tree(x, self.root) for x in X])


class RandomForestClassifier:
    """Random Forest Ensemble Classifier."""

    def __init__(self, n_estimators=30, max_depth=10, min_samples_split=2, random_state=42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.random_state = random_state
        self.trees = []
        self.classes_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        rng = np.random.RandomState(self.random_state)
        n_samples = X.shape[0]

        self.trees = []
        for i in range(self.n_estimators):
            tree = DecisionTreeClassifier(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                random_state=self.random_state + i
            )
            # Bootstrap sample
            indices = rng.choice(n_samples, size=n_samples, replace=True)
            tree.fit(X[indices], y[indices])
            self.trees.append(tree)
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        tree_preds = np.array([tree.predict(X) for tree in self.trees])
        # Majority voting across all trees
        final_preds = []
        for sample_idx in range(X.shape[0]):
            preds_for_sample = tree_preds[:, sample_idx]
            vals, counts = np.unique(preds_for_sample, return_counts=True)
            final_preds.append(vals[np.argmax(counts)])
        return np.array(final_preds)


class DummyClassifier:
    """Baseline classifier predicting most frequent class."""

    def __init__(self):
        self.majority_class_ = None

    def fit(self, X, y):
        vals, counts = np.unique(y, return_counts=True)
        self.majority_class_ = vals[np.argmax(counts)]
        return self

    def predict(self, X):
        X = np.asarray(X)
        return np.array([self.majority_class_] * len(X))


class LogisticRegression:
    """Multinomial Softmax Logistic Regression with L2 Regularization."""

    def __init__(self, lr=0.05, n_iters=500, reg=0.01, random_state=42):
        self.lr = lr
        self.n_iters = n_iters
        self.reg = reg
        self.random_state = random_state
        self.W = None
        self.b = None
        self.classes_ = None

    def _softmax(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        n_samples, n_features = X.shape
        n_classes = len(self.classes_)

        rng = np.random.RandomState(self.random_state)
        self.W = rng.randn(n_features, n_classes) * 0.01
        self.b = np.zeros(n_classes)

        class_to_idx = {c: i for i, c in enumerate(self.classes_)}
        y_indices = np.array([class_to_idx[val] for val in y])
        Y_one_hot = np.zeros((n_samples, n_classes))
        Y_one_hot[np.arange(n_samples), y_indices] = 1.0

        for _ in range(self.n_iters):
            scores = np.dot(X, self.W) + self.b
            probs = self._softmax(scores)

            grad_W = (np.dot(X.T, (probs - Y_one_hot)) / n_samples) + self.reg * self.W
            grad_b = np.sum(probs - Y_one_hot, axis=0) / n_samples

            self.W -= self.lr * grad_W
            self.b -= self.lr * grad_b

        return self

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        scores = np.dot(X, self.W) + self.b
        probs = self._softmax(scores)
        pred_indices = np.argmax(probs, axis=1)
        return self.classes_[pred_indices]


class FertilizerPipeline:
    """Unified Pipeline chaining ColumnTransformer and Model Estimator."""

    def __init__(self, preprocessor: ColumnTransformer, model):
        self.preprocessor = preprocessor
        self.model = model

    def fit(self, df_X, y):
        X_trans = self.preprocessor.fit_transform(df_X)
        self.model.fit(X_trans, y)
        return self

    def predict(self, df_X):
        X_trans = self.preprocessor.transform(df_X)
        return self.model.predict(X_trans)


# Metric calculation utilities
def compute_metrics(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    classes = np.unique(np.concatenate([y_true, y_pred]))

    acc = np.mean(y_true == y_pred)

    precisions = []
    recalls = []
    f1s = []

    for c in classes:
        tp = np.sum((y_true == c) & (y_pred == c))
        fp = np.sum((y_true != c) & (y_pred == c))
        fn = np.sum((y_true == c) & (y_pred != c))

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        precisions.append(prec)
        recalls.append(rec)
        f1s.append(f1)

    # Confusion Matrix
    cm = []
    for actual in classes:
        row = []
        for pred in classes:
            row.append(int(np.sum((y_true == actual) & (y_pred == pred))))
        cm.append(row)

    return {
        "accuracy": round(float(acc), 4),
        "macro_precision": round(float(np.mean(precisions)), 4),
        "macro_recall": round(float(np.mean(recalls)), 4),
        "macro_f1": round(float(np.mean(f1s)), 4),
        "confusion_matrix": cm,
        "classes": list(classes),
    }
