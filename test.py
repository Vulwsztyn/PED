import pandas
import pickle
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.decomposition import PCA
import lime
import lime.lime_tabular
import imagenet_labels
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

EXCLUDED_COLUMNS = ['id', 'score', 'comms_num']


# def indices_to_be_removed(test):
#     indices = []
#     for i in EXCLUDED_COLUMNS:
#         if i in test.columns:
#             indices.append(test.columns.get_loc(i))
#     return indices

def analyze(attributes, cls, score_or_comms_num='score', image_or_text='text'):
    if image_or_text not in ['image', 'text']:
        raise AttributeError
    if score_or_comms_num not in ['score', 'comms_num']:
        raise AttributeError

    train, test = train_test_split(attributes, test_size=0.2)

    exclude = lambda x: x[x.columns.difference(EXCLUDED_COLUMNS)]

    train_without_exculded = exclude(train)
    test_without_excluded = exclude(test)
    attributes_without_excluded = exclude(attributes)

    cls.fit(train_without_exculded, train[score_or_comms_num])
    y_pred = cls.predict(test_without_excluded)

    mse = mean_squared_error(y_pred, test[score_or_comms_num])
    rmse = np.sqrt(mse)

    pca = PCA(n_components=2)
    pca.fit(attributes_without_excluded)
    components = pca.transform(attributes_without_excluded)

    print(components.T)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(components.T[0], components.T[1], attributes[score_or_comms_num])
    feature_names = np.array([])
    if image_or_text == 'image':
        feature_names = np.array([
            x if not x.startswith('class') else 'p_' + imagenet_labels.imagenet_labels(int(x[x.find('_') + 1:]))[:11]
            for x in attributes.columns[:-1]])
    else:
        feature_names = np.array([x.replace('body', 'b').replace('title', "t") for x in attributes.columns[:-1]])

    explainer = lime.lime_tabular.LimeTabularExplainer(train_without_exculded.to_numpy(),
                                                       feature_names=feature_names,
                                                       class_names=[score_or_comms_num],
                                                       categorical_features=[],
                                                       verbose=True,
                                                       mode='regression')

    i = 1235
    exp = explainer.explain_instance(test_without_excluded.to_numpy()[i], cls.predict,
                                     num_features=30)  # TODO: num features
    # print(test.to_numpy()[i][-1])
    return rmse, exp, cls



def nasza_pienkna_funkcja(image_or_text='image', all_or_pruned='pruned', mlp_or_rf='mlp', score_or_comms_num='score',
                          unchanged_or_bracketed='unchanged'):
    if image_or_text not in ['image', 'text']:
        raise AttributeError
    if all_or_pruned not in ['all', 'pruned']:
        raise AttributeError
    if mlp_or_rf not in ['mlp', 'rf']:
        raise AttributeError
    if score_or_comms_num not in ['score', 'comms_num']:
        raise AttributeError
    if unchanged_or_bracketed not in ['unchanged', 'bracketed']:
        raise AttributeError

    attributes = pickle.load(open(
        "./pickle/{}_attributes{}.pkl".format(image_or_text,
                                              '' if all_or_pruned == 'pruned' else '_all'), "rb"))

    train, test = train_test_split(attributes, test_size=0.2)

    exclude = lambda x: x[x.columns.difference(EXCLUDED_COLUMNS)]

    train_without_exculded = exclude(train)
    test_without_excluded = exclude(test)
    attributes_without_excluded = exclude(attributes)

    cls = None
    if mlp_or_rf == 'mlp':
        cls = MLPRegressor(hidden_layer_sizes=(30, 60), max_iter=300, learning_rate='adaptive')
    else:
        cls = RandomForestRegressor()
    cls.fit(train_without_exculded, train[score_or_comms_num])
    y_pred = cls.predict(test_without_excluded)

    mse = mean_squared_error(y_pred, test[score_or_comms_num])
    rmse = np.sqrt(mse)

    pca = PCA(n_components=2)
    pca.fit(attributes_without_excluded)
    components = pca.transform(attributes_without_excluded)

    print(components.T)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(components.T[0], components.T[1], attributes['score'])
    feature_names = np.array([])
    if image_or_text == 'image':
        feature_names = np.array([
            x if not x.startswith('class') else 'p_' + imagenet_labels.imagenet_labels(int(x[x.find('_') + 1:]))[:11]
            for x in attributes.columns[:-1]])
    else:
        feature_names = np.array([x.replace('body', 'b').replace('title', "t") for x in attributes.columns[:-1]])

    explainer = lime.lime_tabular.LimeTabularExplainer(train_without_exculded.to_numpy(),
                                                       feature_names=feature_names,
                                                       class_names=['score'],
                                                       categorical_features=[],
                                                       verbose=True,
                                                       mode='regression')

    i = 1235
    exp = explainer.explain_instance(test_without_excluded.to_numpy()[i], cls.predict,
                                     num_features=30)  # TODO: num features
    # print(test.to_numpy()[i][-1])
    return rmse, exp


# to jest tylko po to, żeby zobaczyć czy erroryn't
if __name__ == '__main__':
    for image_or_text in ['image', 'text']:
        for all_or_pruned in ['pruned', 'all']:
            for mlp_or_rf in ['mlp', 'rf']:
                for score_or_comms_num in ['score', 'comms_num']:
                    for unchanged_or_bracketed in ['unchanged']:  # TODO: bracketed
                        print(image_or_text, all_or_pruned, mlp_or_rf, score_or_comms_num, unchanged_or_bracketed)
                        error, exp = nasza_pienkna_funkcja(image_or_text=image_or_text, all_or_pruned=all_or_pruned,
                                                           mlp_or_rf=mlp_or_rf,
                                                           score_or_comms_num=score_or_comms_num,
                                                           unchanged_or_bracketed=unchanged_or_bracketed)
                        plt.show()
                        print(error)
                        exp.show_in_notebook(show_table=True)
