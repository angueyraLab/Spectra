from cmcrameri import cm #colormaps
from numpy import floor, zeros
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import os.path

batlow = cm.vik(range(255))
batlow = batlow[0:255:int(floor(255/8)),:]

def applyPlotStyle(plotStyleString):
    if plotStyleString=='Dark':
        # dark background
        params = {
            "ytick.color" : "w",
            "xtick.color" : "w",
            "axes.labelcolor" : "w",
            "axes.edgecolor" : "w",
            "axes.linewidth" : 3,
            "xtick.major.width" : 3,
            "ytick.major.width" : 3,
            "xtick.major.size" : 8,
            "ytick.major.size" : 8,
            "text.color" : "w"}
        plt.rcParams.update(params)
        plt.style.use('dark_background')
        baseColor = '#ffffff'
    elif plotStyleString=='Light':
        # white background
        params = {
            "ytick.color" : "k",
            "xtick.color" : "k",
            "axes.labelcolor" : "k",
            "axes.edgecolor" : "k",
            "axes.linewidth" : 2,
            "xtick.major.width" : 2,
            "ytick.major.width" : 2,
            "xtick.major.size" : 8,
            "ytick.major.size" : 8,
            "text.color" : "k"}
        baseColor = '#000000'
    plt.rcParams.update(params)
    font_prop = font_manager.FontProperties(fname='/System/Library/Fonts/Avenir.ttc')
    matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=batlow)
    print('Plotting style is ' + plotStyleString)
    return baseColor

#authors
vsdlPpl = [
        'Angueyra J',
        'Householder C',
        'Kwak L',
        'Hnilo M',
        'Tolosa U',
        'Liang I',
        'Lee A',
        ]


#gene Colors
zfC = {
    'R' : '#7d7d7d',
    'U' : '#B73AB9',
    'S' : '#4364F6',
    'M' : '#59CB3B',
    'L' : '#CE2A22',
    'H' : '#FFAF00',
    'H1' : '#FFAF00',
    'rho'  : '#7d7d7d',
    'sws1' : '#B73AB9',
    'sws2' : '#4364F6',
    'mws1' : '#59CB3B',
    'mws2' : '#59CB3B',
    'mws3' : '#59CB3B',
    'mws4' : '#59CB3B',
    'lws1' : '#CE2A22',
    'lws2' : '#CE2A22',
    'actb2': '#926645',
    'tbx2a': '#c92675',
    'tbx2b': '#7526c9',
    'six7' : '#d6ab00',
}


def ansiText(inputText,ansiKey):
    # https://tforgione.fr/posts/ansi-escape-codes/
    ansiKVP = {
        'bold': '\x1B[1m',
        'faint': '\x1B[2m',
        'italic': '\x1B[3m',
        'underlined': '\x1B[4m',
        'inverse': '\x1B[7m',
        'strikethrough': '\x1B[9m',
        'black': '\x1B[30m'	,
        'red': '\x1B[31m'	,
        'green': '\x1B[32m'	,
        'yellow': '\x1B[33m'	,
        'blue': '\x1B[34m'	,
        'magenta': '\x1B[35m'	,
        'cyan': '\x1B[36m'	,
        'white': '\x1B[37m'	,
        'blackBG': '\x1B[40m',
        'redBG': '\x1B[41m',
        'greenBG': '\x1B[42m',
        'yellowBG': '\x1B[43m',
        'blueBG': '\x1B[44m',
        'magentaBG': '\x1B[45m',
        'cyanBG': '\x1B[46m',
        'whiteBG': '\x1B[47m',
        'exit': '\x1b[0m'
    }
    return ('{0}{1}{2}'.format(ansiKVP.get(ansiKey),inputText,ansiKVP.get('exit')))

def ansiRGB(inputText,rgbKey = '122;122;122'):
    # https://tforgione.fr/posts/ansi-escape-codes/
    # rgbKey format = '0-255;0-255;0-255'
    return ('\x1B[38;2;{0}m{1}{2}'.format(rgbKey,inputText,'\x1b[0m'))

def ansiKeyColors(inputText,ansiKey = 'exit'):
    ansiKVP = {
        'R': '125;125;125',
        'U': '183;58;185',
        'S': '67;100;248',
        'M': '89;203;59',
        'L': '206;42;34',
        'exit': '\x1b[0m'
    }
    return ansiRGB(inputText,ansiKVP.get(ansiKey))

# ----------
def formatFigureMain(figH, axH, plotH):
    font_path = '/System/Library/Fonts/Avenir.ttc'
    fontTicks = font_manager.FontProperties(fname=font_path, size=20)
    fontLabels = font_manager.FontProperties(fname=font_path, size=24)
    fontTitle = font_manager.FontProperties(fname=font_path, size=26)
    axH.set_xscale('linear')
    axH.spines['top'].set_visible(False)
    axH.spines['right'].set_visible(False)
    
    for label in (axH.get_xticklabels() + axH.get_yticklabels()):
        label.set_fontproperties(fontTicks)
    axH.set_xlabel(axH.get_xlabel(), fontproperties = fontTicks)
    axH.set_ylabel(axH.get_ylabel(), fontproperties = fontTicks)
    axH.set_title(axH.get_title(), fontproperties = fontTitle)
    return fontLabels

def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import colorsys
    try:
        c = matplotlib.colors.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*matplotlib.colors.to_rgb(c))
    return matplotlib.colors.rgb2hex(colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2]))

def estimateJitter(dataArray):
    """ creates random jitter scaled by local density of points"""
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(dataArray)
    density = kde(dataArray)
    jitter = np.random.randn(len(dataArray))*density
    return jitter
        
def getFileList(dirData,fileNameMatch='',addDetails=''):
    fileList = sorted([f for f in os.listdir(dirData) if not f.startswith('.')]) # get all the files in the data directory (excluding system files) and sort them alphabatically
    fileList = ([f for f in fileList if any([s in f for s in fileNameMatch])]) # only keep relevant files
    if (addDetails=='path'):
        fileList = (['# filePath = \'' + f for f in fileList]) # add text before each file
        fileList = list(map(lambda st: str.replace(st, '.nd2', '\'; gene = \'' + gene + '\'; '), fileList)) #remove file extension (.nd2) and add text after each file
    elif (addDetails=='list'):
        fileList = (['\'' + f for f in fileList]) # add text before each file
        fileList = list(map(lambda st: str.replace(st, '.nd2', '\','), fileList)) #remove file extension (.nd2) and add text after each file
    else:
        fileList = list(map(lambda st: str.replace(st, '.nd2', ''), fileList)) #remove file extension (.nd2) and add text after each file
    return fileList

