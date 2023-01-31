import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

'''
Data loaders for different input formats.
'''


def load_data(data_path):
    '''
    Original data loader from reg_go2.
    '''
    df = (pd.read_csv(data_path, skiprows=1).values).astype("float32")

    df_y = df[:, 0].astype("float32")
    df_x = df[:, 1:PL].astype(np.float32)

    #    scaler = MaxAbsScaler()

    scaler = StandardScaler()
    df_x = scaler.fit_transform(df_x)

    X_train, X_test, Y_train, Y_test = train_test_split(
        df_x, df_y, test_size=0.20, random_state=42
    )

    print("x_train shape:", X_train.shape)
    print("x_test shape:", X_test.shape)

    return X_train, Y_train, X_test, Y_test


def load_data_from_parquet(data_path):
    print("reading {}".format(data_path))
    df = pd.read_parquet(data_path)
    df_y = df['reg'].values.astype("float32")
    
    # use for covid docking dataframes
    # df_x = df.iloc[:, 6:].values.astype("float32")
    
    # use for cancer docking dataframes
    df_x = df.iloc[:, 5:].values.astype("float32")

    print('df_y: {}'.format(df_y.shape))
    print('df_x: {}'.format(df_x.shape))

    scaler = StandardScaler()
    df_x = scaler.fit_transform(df_x)

    X_train, X_test, Y_train, Y_test = train_test_split(
        df_x, df_y, test_size=0.20, random_state=42
    )
    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)
    print("Y_train shape:", Y_train.shape)
    print("Y_test shape:", Y_test.shape)

    return X_train, Y_train, X_test, Y_test
