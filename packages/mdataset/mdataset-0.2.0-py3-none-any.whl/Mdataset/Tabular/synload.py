from pmlb import fetch_data
from ydata_synthetic.synthesizers.regular import RegularSynthesizer
from ydata_synthetic.synthesizers import ModelParameters, TrainParameters

def syn_load(synth, model_filename='model.pkl'):
    synth.save(model_filename)