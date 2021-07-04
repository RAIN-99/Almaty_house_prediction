import pandas as pd
import dill
import shap
import matplotlib.pyplot as plt
regions=['alatauski','almalinski','auezovski','bostandykski','jetysuski','turksibski','medeuski','nauryzbaiski']
def explanation_of_single_example():
    explainer = shap.Explainer(model['regressor'])
    shap_values=explainer(X_test)
    shap.plots.waterfall(shap_values[2],max_display=20)#6
    pass
def explanation_of_all_features():
    explainer = shap.TreeExplainer(model['regressor'])
    shap_values = explainer.shap_values(X_test)
    shap.summary_plot(shap_values,X_test,max_display=20)#6
    shap.summary_plot(shap_values, X_test, plot_type='bar')
    pass



for i in regions:
    X_test=pd.read_csv(f"../Models/{i}/X_test.csv")
    model = dill.load(open(f'../Models/{i}/Xgboost_model.pkl','rb'))
    X_test=model['encoder'].transform(X_test)
    explanation_of_single_example()
    explanation_of_all_features()
