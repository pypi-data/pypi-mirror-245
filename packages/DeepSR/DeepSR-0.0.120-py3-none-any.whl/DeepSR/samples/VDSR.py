"""
VDSR model
https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Kim_Accurate_Image_Super-Resolution_CVPR_2016_paper.pdf
"""
import numpy as np
from keras import losses
from keras.layers import Input,  add
from keras.layers.convolutional import Conv2D
from keras.models import Model
from keras.optimizer_v2.adam import Adam
from os.path import basename
from keras.callbacks import LearningRateScheduler

eps = 1.1e-6

settings = \
    {
        'augment': [],  # must be any or all lof [90,180,270, 'flipud', 'fliplr', 'flipudlr' ]
        'backend': 'tensorflow',
        'batchsize': 64,
        'channels': 3,
        'colormode': 'RGB',  # 'YCbCr' or 'RGB'
        'crop': 0,
        'crop_test': 0,
        'decay': 0.9,
        'decimation': 'bicubic',
        'dilation_rate':(1,1),
        'espatience': 5,
        'epoch': 2,
        'inputsize': 41,  #
        'interp_compare': '',
        'interp_up': 'bicubic',
        'kernel_initializer': 'he_normal',
        'lrate': 0.01,
        'lrpatience': 3,
        'lrfactor': 0.5,
        'metrics': 'ALL',
        'minimumlrate': 1e-7,
        'modelname': basename(__file__).split('.')[0],
        'noise': '',
        'normalization': ['divide', 255.0],  # ['standard', "53.28741141", "40.73203139"],
        'normalizeback': False,
        'normalizeground': False,
        'outputdir': '',
        'scale': 2,
        'seed': 19,
        'shuffle': True,
        'stride': 41,  # the same with input size, to have no overlap as is in the paper.
        'target_channels': 3,
        'target_cmode': 'RGB',
        'testpath': [r'D:\calisma\datasets\SRCNN\set5'],
        'traindir': r"D:\calisma\datasets\SRCNN\set5",
        'upscaleimage': True,
        'valdir': r'D:\calisma\datasets\SRCNN\set5',
        'weightpath': '',
        'workingdir': '',
    }


def build_model(self, testmode=False):
    """Construction method for VDSR model"""

    # use the full size of image if model is tested, otherwise take image patches of given size while training
    input_size = None if testmode else self.inputsize
    input_shape = (input_size, input_size, self.channels)
    input_img = Input(shape=input_shape, name='main_input')

    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(input_img)
    model = self.apply_activation(model, self.activation, self.activation + "_001")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_002")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_003")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_004")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_005")

    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_006")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_007")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_008")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_009")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_010")

    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_011")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_012")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_013")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_014")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_015")

    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_016")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_017")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_018")
    model = Conv2D(64, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    model = self.apply_activation(model, self.activation, self.activation + "_019")
    model = Conv2D(self.target_channels, (3, 3), padding='same', kernel_initializer=self.kernel_initializer, dilation_rate=self.dilation_rate)(model)
    res_img = model

    output_img = add([res_img, input_img])
    model = Model(input_img, output_img)

    optimizer = Adam(learning_rate=self.lrate) # optimizing method: ADAM
    model.compile( loss=losses.mean_squared_error, optimizer=optimizer) # compile the model

    # model.summary() # print model structure

    return model


def fn_user_callbacks(self):
    """User-defined callback for learning rate scheduling"""
    callbacks_list=[]

    def step_decay(epoch):
        from tensorflow.math import pow, floor
        initial_lrate = self.lrate # take learning rate from the class
        drop = 0.5 # reduce learning rate by a half
        epochs_drop = 20.0 # after every 20 epochs
        lrate = initial_lrate * pow(drop, floor((1 + epoch) / epochs_drop))
        return np.float(lrate)

    lrate = LearningRateScheduler(step_decay) # Keras' method for learning rate scheduler

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
    im_list =[]
    im_list.append(np.asarray(Image.fromarray(img).rotate(10))) # rotate 10 degrees
    return im_list
