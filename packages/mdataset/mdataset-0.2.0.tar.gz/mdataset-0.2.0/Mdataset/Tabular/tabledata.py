from ydata_synthetic.synthesizers.regular import RegularSynthesizer

def table_generate(model_filename='default_model.pkl', num_samples=1000):
    synth = RegularSynthesizer.load(model_filename)
    synth_data = synth.sample(num_samples)
    return synth_data

