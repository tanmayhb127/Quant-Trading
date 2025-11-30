"""Train LightGBM baseline for regression (predict Market_High) and classification (WithinRange).
Produces simple rolling evaluation and saves model and metrics.
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score, f1_score
import joblib

WORKDIR = os.path.dirname(__file__)
INFILE = os.path.join(WORKDIR, 'merged_predictions_1year.csv')

print('Loading', INFILE)
df = pd.read_csv(INFILE, parse_dates=['Date'])
df = df.sort_values('Date')
# create targets
# drop rows with missing market values
df = df.dropna(subset=['Market_High','Market_Low'])
# classification target: whether both market high and low are inside predicted range
df['WithinHigh'] = (df['Market_High'] <= df['Resistance']).astype(int)
df['WithinLow'] = (df['Market_Low'] >= df['Support']).astype(int)
df['WithinRange'] = ((df['WithinHigh'] == 1) & (df['WithinLow'] == 1)).astype(int)

# basic features
df['DayOfWeek'] = df['Date'].dt.dayofweek
# source encoding
src_dummies = pd.get_dummies(df['Source'], prefix='src')
X_num = df[['Support','Resistance','RangeWidth','RangeMid','DayOfWeek']]
X = pd.concat([X_num.reset_index(drop=True), src_dummies.reset_index(drop=True)], axis=1)

y_reg = df['Market_High']
y_clf = df['WithinRange']

# TimeSeriesSplit evaluation
ts = TimeSeriesSplit(n_splits=5)
rmse_scores = []
clf_acc = []
clf_prec = []
clf_rec = []
clf_f1 = []
fold = 0
models = {}
for train_idx, val_idx in ts.split(X):
    fold += 1
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y_reg.iloc[train_idx], y_reg.iloc[val_idx]

    dtrain = lgb.Dataset(X_train, label=y_train)
    dval = lgb.Dataset(X_val, label=y_val, reference=dtrain)
    params = {'objective':'regression','metric':'rmse','verbosity':-1}
    model = lgb.train(params, dtrain, num_boost_round=1000, valid_sets=[dtrain,dval], early_stopping_rounds=50)
    preds = model.predict(X_val, num_iteration=model.best_iteration)
    rmse = mean_squared_error(y_val, preds, squared=False)
    rmse_scores.append(rmse)
    print(f'Fold {fold} Regression RMSE: {rmse:.4f}')
    models[f'gbr_fold{fold}'] = model

    # classification model using same features (train a LightGBM classifier)
    clf = lgb.LGBMClassifier(n_estimators=200)
    clf.fit(X_train, y_clf.iloc[train_idx])
    preds_clf = clf.predict(X_val)
    acc = accuracy_score(y_clf.iloc[val_idx], preds_clf)
    prec = precision_score(y_clf.iloc[val_idx], preds_clf, zero_division=0)
    rec = recall_score(y_clf.iloc[val_idx], preds_clf, zero_division=0)
    f1 = f1_score(y_clf.iloc[val_idx], preds_clf, zero_division=0)
    clf_acc.append(acc); clf_prec.append(prec); clf_rec.append(rec); clf_f1.append(f1)
    print(f'Fold {fold} Classifier Acc: {acc:.4f} Prec: {prec:.4f} Rec: {rec:.4f} F1: {f1:.4f}')
    models[f'clf_fold{fold}'] = clf

# Save best model (last fold) and metrics
joblib.dump(models, os.path.join(WORKDIR, 'models_lgb_folds.joblib'))
metrics = {
    'rmse_mean': np.mean(rmse_scores), 'rmse_std': np.std(rmse_scores),
    'clf_acc_mean': np.mean(clf_acc), 'clf_prec_mean': np.mean(clf_prec), 'clf_rec_mean': np.mean(clf_rec), 'clf_f1_mean': np.mean(clf_f1)
}
import json
with open(os.path.join(WORKDIR, 'training_metrics.json'), 'w') as f:
    json.dump(metrics, f, indent=2)
print('Training complete. Metrics saved to training_metrics.json')
print(metrics)
