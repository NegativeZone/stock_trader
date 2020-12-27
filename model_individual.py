import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import ModelCheckpoint
from glob import glob
from os.path import basename, splitext
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

filenames = glob('dataset/ML/*.csv')
dfs = {splitext(basename(fp))[0]: pd.read_csv(fp) for fp in filenames}
columns_of_interest = [
    'Date',
    'Open',
    'Close',
    'Volume',
    'Trades'
]
accuracy_file = open("accuracy.txt", "w+")

for i in dfs:
    dfs[i]['Change'] = dfs[i]["Close"] - dfs[i]["Open"]
    dfs[i]['Date'] = pd.to_datetime(
        dfs[i]['Date'], format='%Y-%m-%d', errors='coerce')
    dfs[i]['Movement'] = dfs[i]['Change'].apply(
        lambda x: 1 if x > 0 else 0)
    dfs[i] = dfs[i].sort_values(by="Date")
    dfs[i] = dfs[i].drop(columns=['Date', 'Prev Close', 'Symbol'])
    for j in range(5):
        for k in dfs[i].columns:
            dfs[i][k+" D-"+str(j+1)] = dfs[i][k].shift(j+2)
    dfs[i] = dfs[i].dropna()
    dfs[i] = dfs[i].reset_index(drop=True)
    X = dfs[i].drop(columns='Movement')
    y = dfs[i]['Movement']
    train_max = int(0.7*(X.shape[0]))
    X_train = X[:train_max]
    y_train = y[:train_max]
    X_test = X[train_max+1:]
    y_test = y[train_max+1:]
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    model = Sequential()
    model.add(Dense(16, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(4, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy'])
    chkpt_name = 'models/Weights-'+i+'.hdf5'
    checkpoint = ModelCheckpoint(
        chkpt_name,
        monitor='val_accuracy',
        verbose=1,
        save_best_only=True,
        mode='auto')
    callbacks_list = [checkpoint]
    callbacks_list.append(ModelCheckpoint(
        chkpt_name,
        monitor='val_loss',
        verbose=1,
        save_best_only=True,
        mode='auto'))
    history = model.fit(
        X_train,
        y_train,
        epochs=25,
        batch_size=40,
        validation_split=0.2,
        verbose=1,
        callbacks=callbacks_list)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title(i + ' model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('graphs/' + i + ' model accuracy.png')
    plt.close()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title(i + ' model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('graphs/' + i + ' model loss.png')
    plt.close()
    temp, output = model.evaluate(X_test, y_test, verbose=0)
    accuracy_file.write(i + ' Accuracy: %.2f' % (output*100))

accuracy_file.close()
