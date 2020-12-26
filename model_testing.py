import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
# from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = pd.read_csv('dataset/ML/data.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
# df['Day of Week'] = df['Date'].dt.dayofweek
df = df.drop(columns={'Date'})
X = df[[
    'Symbol',
    'Prev Close',
    'Volume',
    'Trades',
    'BSE Volume',
    'BSE Trades'
]]
X['Volume'] = X['Volume'].shift(1)
X['Trades'] = X['Trades'].shift(1)
X['BSE Volume'] = X['BSE Volume'].shift(1)
X['BSE Trades'] = X['BSE Trades'].shift(1)
# X = df.drop(columns={'Open', 'Close', 'Low', 'High'})
# X = X.drop(columns={'Last'})
# for i in X:
#     if i not in ['Year', 'Month', 'Day', 'Symbol']:
#         X[i] = X[i].shift(1)
X = X.dropna()
y = df[['Open', 'Close']]
y = y.iloc[1:]
# print(X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

X_train = pd.get_dummies(X_train, columns=["Symbol"])
X_sym = X_test["Symbol"]
X_test = pd.get_dummies(X_test, columns=["Symbol"])
# print(X_train.shape)
# print(X.dtypes)
# print(y.shape)

model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(2048, activation='relu'))
model.add(Dense(2048, activation='relu'))
model.add(Dense(2048, activation='relu'))
model.add(Dense(2, activation='linear'))

model.load_weights('Weights-058--121.26588.hdf5')
model.compile(
    loss='mean_absolute_error',
    optimizer='adam',
    metrics=['mae'])

# checkpoint_name = 'Weights-{epoch:03d}--{val_loss:.5f}.hdf5'
# checkpoint = ModelCheckpoint(
#     checkpoint_name,
#     monitor='val_loss',
#     verbose=1,
#     save_best_only=True,
#     mode='auto')
# callbacks_list = [checkpoint]
# model.fit(
#     X_train,
#     y_train,
#     epochs=64,
#     batch_size=500,
#     validation_split=0.2,
#     callbacks=callbacks_list)

verify = pd.DataFrame()
output = model.predict(X_test)
results = mean_absolute_error(y_test, output)
errors = output - y_test
df_output = pd.DataFrame(output, columns=['Predicted Open', 'Predicted Close'])
y_test = y_test.reset_index()
X_sym = X_sym.reset_index()
verify['Daily Trend Predicted'] = (
    df_output['Predicted Close'] - df_output['Predicted Open'])
verify['Daily Trend Actual'] = y_test['Close'] - y_test['Open']
verify['Daily Trend Gap'] = (
    abs(verify['Daily Trend Actual'] - verify['Daily Trend Predicted']))
verify['Accuracy'] = abs(y_test['Close'] - df_output['Predicted Close'])
verify['Stock Value'] = y_test['Close']
verify['Stock Name'] = X_sym['Symbol']

print(
    verify[verify['Accuracy'] < 0.1*verify['Stock Value']].sort_values(
        by=['Accuracy']))
