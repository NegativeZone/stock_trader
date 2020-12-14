import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
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
X = pd.get_dummies(X, columns=["Symbol"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

# print(X_train.shape)
# print(X.dtypes)
# print(y.shape)

model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(2048, activation='relu'))
model.add(Dense(2048, activation='relu'))
model.add(Dense(2048, activation='relu'))
model.add(Dense(2, activation='linear'))
model.compile(
    loss='mean_absolute_error',
    optimizer='adam',
    metrics=['mae'])

checkpoint_name = 'Weights-{epoch:03d}--{val_loss:.5f}.hdf5'
checkpoint = ModelCheckpoint(
    checkpoint_name,
    monitor='val_loss',
    verbose=1,
    save_best_only=True,
    mode='auto')
callbacks_list = [checkpoint]
model.fit(
    X_train,
    y_train,
    epochs=64,
    batch_size=500,
    validation_split=0.2,
    callbacks=callbacks_list)

output = model.predict(X_test)
results = mean_absolute_error(y_test, output)
errors = output - y_test
print(results)
print(errors)
