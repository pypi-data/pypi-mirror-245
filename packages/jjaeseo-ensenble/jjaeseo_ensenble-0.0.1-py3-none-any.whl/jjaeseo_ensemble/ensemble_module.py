from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
import numpy as np

class BlendingClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self):
        # 클래스 내에서 고정된 모델 객체를 생성
        self.base_models = [RandomForestClassifier(n_estimators=100, random_state=10),
                            DecisionTreeClassifier(max_depth=5, random_state=10),
                            SVC(kernel='linear', C=1.0, probability=True, random_state=10)]
        self.blender_model = LogisticRegression(max_iter = 1000)
    
    def fit(self, x, y):
        x_train, x_blend, y_train, y_blend = train_test_split(x, y, test_size=0.2, random_state=10)
        
        # Train the base models on the first half of the data
        self.base_models_ = [clf.fit(x_train, y_train) for clf in self.base_models]
        
        # Generate predictions for the second half of the data
        predictions = [clf.predict(x_blend) for clf in self.base_models_]
        blend_data = np.column_stack(predictions)
        
        # Train the blender model on the blended data
        self.blender_model_ = self.blender_model.fit(blend_data, y_blend)
    
    def predict(self, x):
        # Generate predictions from base models
        predictions = [clf.predict(x) for clf in self.base_models_]
        blend_data = np.column_stack(predictions)
        
        # Use the blender model to make the final prediction
        return self.blender_model_.predict(blend_data)
