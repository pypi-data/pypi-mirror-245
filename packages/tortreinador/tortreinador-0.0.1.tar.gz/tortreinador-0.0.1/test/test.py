import pandas as pd
from tortreinador import train
import torch
from tortreinador.MDN import mdn, Mixture, NLLLoss

data = pd.read_excel('D:\\Resource\\Gas_Giants_Core_Earth20W.xlsx')
data['M_total (M_E)'] = data['Mcore (M_J/10^3)'] + data['Menv (M_E)']

input_parameters = [
    'Mass (M_J)',
    'Radius (R_E)',
    'T_sur (K)',
]

output_parameters = [
    'M_total (M_E)',
    'T_int (K)',
    'P_CEB (Mbar)',
    'T_CEB (K)'
]

trainer = train.TorchTrainer()

t_data = trainer.load_data(data=data, input_parameters=input_parameters, output_parameters=output_parameters,
                           if_normal=True, if_shuffle=True)


model = mdn(len(input_parameters), len(output_parameters), 10, 256)
criterion = NLLLoss()
pdf = Mixture()
optim = torch.optim.Adam(model.parameters(), lr=0.0001984)


t_l, v_l, val_r2, train_r2, mse = trainer.fit_for_MDN(t_data[0], t_data[1], criterion, model=model, mixture=pdf, model_save_path='D:\\Resource\\MDN\\', optim=optim, best_r2=0.5)







