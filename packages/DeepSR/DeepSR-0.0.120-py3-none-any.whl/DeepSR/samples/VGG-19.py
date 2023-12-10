#
# VGG-19 from
#
# VERY DEEP CONVOLUTIONAL NETWORKS FOR LARGE-SCALE IMAGE RECOGNITION
#
# Karen Simonyan & Andrew Zisserman
#
# https://arxiv.org/pdf/1409.1556.pdf
#
# https://www.robots.ox.ac.uk/~vgg/research/very_deep/
#


from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dense
from tensorflow.keras.utils import plot_model


eps = 1.1e-6

# PARAMETER INSTRUCTION RELATED TO SCALE FACTOR #

settings = \
{
"activation": "relu",
'augment':[], # must be any or all lof [90,180,270, 'flipud', 'fliplr', 'flipudlr' ]
'backend': 'tensorflow',
'batchsize':128,
'channels':1,
'colormode':'RGB', # 'YCbCr' or 'RGB'
'crop': 0,
'crop_test': 6,
'decay':1e-6,
'dilation_rate':(1,1),
'decimation': 'bicubic',
'espatience' : 50,
'epoch':5,
'inputsize':16, #
'interp_compare': 'lanczos',
'interp_up': 'bicubic',
'kernel_initializer': 'glorot_uniform',
'lrate':1e-3,
'lrpatience': 25,
'lrfactor' : 0.5,
'metrics': ["PSNR"],
'minimumlrate' : 1e-7,
'modelname': basename(__file__).split('.')[0],
'noise':'',
'normalization':['divide', '255.0'], # ['standard', "53.28741141", "40.73203139"],
'normalizeback': False,
'normalizeground':False,
'outputdir':'',
'scale':2,
'seed': 19,
'shuffle' : True,
'stride':5, # adımın 72 nin 1/3 ü olmasını istiyoruz. yani 24. 4 ölçek için 6 adım çıkışta 24 eder.
'target_channels': 1,
'target_cmode' : 'RGB',
'testpath': [r'D:\calisma\datasets\US\UltrasoundCases\USCases Database\test\1'],
'traindir': r"D:\calisma\datasets\US\UltrasoundCases\USCases Database\train\1",
'upscaleimage': False,
'valdir': r'D:\calisma\datasets\US\UltrasoundCases\USCases Database\val\1',
'weightpath':'',
'workingdir': '',
}


def vgg_block(prev_layer, layer_in_blocks):

    for blok in layer_in_blocks:
        for _ in range(blok[0]):
            prev_layer = Conv2D(blok[1], (3,3), padding='same', activation='relu')(prev_layer)

        prev_layer = MaxPooling2D((2,2), strides=(2,2))(prev_layer)

    return prev_layer



def build_model(self, testmode=False):
    if testmode:
        input_size = None
    else:
        input_size = self.inputsize

    input_shape = (input_size, input_size, self.channels)

    layer_in_blocks = [(2,64), (2,128), (4,256), (4, 512), (4,256)]

    visible = Input(shape=input_shape)

    layer = vgg_block(visible, layer_in_blocks)

    last= Dense(4096, activation='relu')(layer)
    last= Dense(4096, activation='relu')(last)
    last_layer= Dense(1000, activation='softmax')(last)

    model = Model(inputs=visible, outputs=last_layer)

    model.summary()

    return model


def fn_user_metrics(img_ground, img):

    return 1


