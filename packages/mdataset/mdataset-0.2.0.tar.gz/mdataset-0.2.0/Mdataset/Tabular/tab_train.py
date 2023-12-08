from pmlb import fetch_data
from ydata_synthetic.synthesizers.regular import RegularSynthesizer
from ydata_synthetic.synthesizers import ModelParameters, TrainParameters

def train_save(epochs, modelname, model_parameters, data, train_arguments, num_cols, cat_cols,
               batch_size=500, learning_rate=2e-4, beta_1=0.5, beta_2=0.9):

    ctgan_args = ModelParameters(batch_size=batch_size, lr=learning_rate, betas=(beta_1, beta_2))
    train_args = TrainParameters(epochs=epochs)

    synth = RegularSynthesizer(modelname=modelname, model_parameters=ctgan_args)
    synth.fit(data=data, train_arguments=train_args, num_cols=num_cols, cat_cols=cat_cols)

# Example usage:
# train_save(epochs=501, modelname='ctgan', model_parameters={'param1': 'value1'}, data=my_data,
#            train_arguments={'arg1': 'value1'}, num_cols=['col1', 'col2'], cat_cols=['col3', 'col4'])
