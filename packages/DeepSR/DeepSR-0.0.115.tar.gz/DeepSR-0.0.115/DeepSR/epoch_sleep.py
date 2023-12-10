
# sleep time for cooling the GPU
from keras.callbacks import Callback
from time import sleep


class EpochSleep(Callback):

    def __init__(self, sleep_time=120):

        self.sleep_time= sleep_time

    def on_train_begin(self, logs={}):
        # keys = list(logs.keys())
        # self.history = {'loss': [], 'val_loss': []}
        pass

    def on_batch_end(self, batch, logs={}):
        # keys = list(logs.keys())
        # self.history['loss'].append(logs.get('loss'))
        # print("End epoch {} of training; got log keys: {}".format(epoch, keys))
        pass


    def on_epoch_end(self, epoch, logs={}):
        # keys = list(logs.keys())
        # self.history['loss'].append(logs.get('val_loss'))
        # print("End epoch {} of training; got log keys: {}".format(epoch, keys))
        print("\nEpoch lasted. Sleeping for", self.sleep_time, "seconds")
        sleep(self.sleep_time)
