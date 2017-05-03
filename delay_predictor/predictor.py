import pandas as pd
from sklearn import linear_model
import numpy as np


def predict(data_frame, airport_code):
    data_frame = data_frame.dropna(axis=0)

    data_frame = data_frame.sample(frac=1)

    def split_train_test(data, test_ratio):
        shuffled_indices = np.random.permutation(len(data))
        test_set_size = int(len(data) * test_ratio)
        test_indices = shuffled_indices[:test_set_size]
        train_indices = shuffled_indices[test_set_size:]
        return data.iloc[train_indices], data.iloc[test_indices]

    train_set, test_set = split_train_test(data_frame, 0.3)

    x_test = test_set['airport_code'].values.reshape(-1, 1)
    y_test = test_set['departure_delay']

    x_train = train_set['airport_code'].values.reshape(-1, 1)
    y_train = train_set['departure_delay']

    ols = linear_model.LinearRegression()

    model = ols.fit(x_train, y_train)

    model.score(x_test, y_test)

    list(model.predict(x_test)[0:20])

    result = model.predict(airport_code)

    return result


if __name__ == '__main__':
    df1 = pd.read_csv('../data/flightsWithAirportCode.csv')
    df2 = pd.read_csv('../data/flightsWithAirportCode1.csv')
    df3 = pd.read_csv('../data/flightsWithAirportCode2.csv')
    df4 = pd.read_csv('../data/flightsWithAirportCode3.csv')
    df5 = pd.read_csv('../data/flightsWithAirportCode4.csv')
    frames = [df1, df2, df3, df4, df5]
    merged_csv = pd.concat(frames)
    predict(merged_csv)
