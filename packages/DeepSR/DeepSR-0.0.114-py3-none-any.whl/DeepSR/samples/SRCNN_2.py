# SRCNN.py. A modified SRCNN model for a 3 channel RGB image super resolution.
import numpy as np
from keras import losses
from keras.layers import Input
from keras.layers.convolutional import Conv2D
from keras.models import Model
from keras.optimizer_v2 import Adam
from os.path import basename
from keras.callbacks import LearningRateScheduler

# hyper-parameters in order. Can be overriden when given as command arguments.
# please, refer to program manual or website for other hyper-parameters.
settings = \
    {   'activation': 'relu',
        'augment': [90, 180, 270],  # augment dataset by rotating images by these degrees.
        'backend': 'tensorflow',  # use tensorflow as Keras’ backend
        'batchsize': 64,  # batch size. Do backpropagation after processing 64 images.
        'channels': 3,  # input image is of 3 channels.
        'colormode': 'RGB',  # use 'RGB' color space.
        'crop': 6,  # number of pixels cropped from borders of input images.
        'crop_test': 0,  # number of pixels cropped from borders of test images.
        'decay': 0.9,  # weight decay value for the optimizer.
        'decimation': 'bicubic',  # downsample images with bicubic interpolation.
        'dilation_rate': (1, 1),  # dilation factor for Keras’ dilated layers.
        'espatience': 5,  # wait for 5 epochs to stop when no improvement achieved.
        'epoch': 50,  # train the model for 50 epochs at maxium.
        'inputsize': 33,  # train with image patches of size 33x33 pixels.
        'interp_compare': '',  # no interpolation method given to compare the model.
        'interp_up': 'bicubic',  # upscale images with bicubic interpolation method.
        'kernel_initializer': 'glorot_uniform',  # kernel initialization method.
        'lrate': 0.001,  # initial learning rate value for training the model.
        'lrpatience': 3,  # wait for 3 epochs before reducing ‘lrate’ by ‘lrfactor’.
        'lrfactor': 0.5,  # reduce learning rate by a half when no improvement.
        'metrics': ['PSNR', 'SSIM', 'VIF'],  # evaluate the model with these IQMs.
        'minimumlrate': 1e-7,  # the minimum learning rate value.
        'modelname': basename(__file__).split('.')[0],  # same name as this file.
        'noise': '',  # noise to be added to input image before feeding.
        'normalization': ['divide', 255.0],  # divide values by 255.0 prior to feeding.
        'outputdir': '',  # provide a path to change the output directory.
        'scale': 2,  # LR image will be upscaled by factor of 2.
        'seed': 19,  # fix the randomness to make results reproducible.
        'shuffle': True,  # shuffle images before feeding.
        'stride': 11,  # size of image patches for training the model.
        'target_channels': 3,  # model should yield 3 channel image.
        'target_cmode': 'RGB',  # process image in RGB color space.
        'testpath': [r'C:\datasets\set5'],  # path(s) to test folders or files.
        'traindir': r'C:\datasets\BSDS100',
        'upscaleimage': True,  # upscale downsampled image before feeding to model.
        'valdir': r'C:\datasets\set14',  # path to the folder of validation files.
        'weightpath': '',  # no path to a weight file is given to load the model with.
        'workingdir': '',  # provide a path to change current working directory.
    }


def build_model(self, testmode=False):
    """Construction method for modified SRCNN model for 3 channel processing in RGB"""
    # full size image for test, otherwise given size image patch for training
    input_size = None if testmode else self.inputsize
    input_shape = (input_size, input_size, self.channels)

    INPUT = Input(shape=input_shape)
    SRCNN = Conv2D(64,(9,9), kernel_initializer=self.kernel_initializer,
   	  padding='valid', input_shape=input_shape, activation=self.activation)(INPUT)
    SRCNN = Conv2D(32, (1,1), kernel_initializer=self.kernel_initializer,
                   		padding='valid', activation=self.activation)(SRCNN)
    SRCNN = Conv2D(self.channels,(5,5), kernel_initializer=self.kernel_initializer,
                   		padding='valid', activation=self.activation)(SRCNN)
    SRCNN = Model(INPUT, outputs=SRCNN)
    SRCNN.compile(optimizer = Adam(self.lrate, self.decay), loss=losses.mean_squared_error)
    return SRCNN


def fn_user_callbacks(self):
    """User-defined callback for learning rate scheduling"""
    callbacks_list = []

    def step_decay(epoch):
        from tensorflow.math import pow, floor
        initial_lrate = self.lrate  # take learning rate from the class
        drop = 0.5  # reduce learning rate by a half
        epochs_drop = 20.0  # after every 20 epochs
        lrate = initial_lrate * pow(drop, floor((1 + epoch) / epochs_drop))
        return np.float(lrate)

    lrate = LearningRateScheduler(step_decay)  # Keras' learning rate scheduler.
    callbacks_list.append(lrate)

    return callbacks_list


def fn_user_metrics(self, img_ground, img):
    """User-defined evaluation metrics."""
    # return log10 of mean absolute deviation between reference and test image.
    return {'LOGMAD': np.log10(np.abs(img_ground - img).mean())}


def fn_user_augmentation(self, img):
    """User-defined augmentation. Rotate image by 10 degrees.
    :parameter img: source image to be augmented by rotating by 10 degrees.
    """
    from PIL import Image
    im_list = []
    im_list.append(np.asarray(Image.fromarray(img).rotate(10)))  # rotate by 10 degrees
    return im_list


#
# # An example of how to use the DeepSR as a class.
# # It is assumed that this code snippet is within the SRCNN.py file
#
# from DeepSR import DeepSR
# DSR = DeepSR(settings)   # an instance of DeepSR object
#
# DSR.make_member([build_model, fn_user_metrics, fn_user_augmentation, fn_user_callbacks])
# DSR.train()   # train the model.
# DSR.set_settings(settings)
