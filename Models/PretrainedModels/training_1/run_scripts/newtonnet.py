import torch
from torch.optim import Adam
import yaml

from combust.layers import get_activation_by_string
from combust.models import NewtonNet

from combust.train import Trainer
from combust.data import parse_ani_data

# torch.autograd.set_detect_anomaly(True)
torch.set_default_tensor_type(torch.DoubleTensor)

# settings
settings_path = 'ani-newtonnet.yml'
settings = yaml.safe_load(open(settings_path, "r"))

# device
if type(settings['general']['device']) is list:
    device = [torch.device(item) for item in settings['general']['device']]
else:
    device = [torch.device(settings['general']['device'])]

# data
train_gen, val_gen, test_gen, tr_steps, val_steps, test_steps, n_train_data, n_val_data, n_test_data, normalizer, test_energy_hash = parse_ani_data(settings,device[0])
print('normalizer: ', normalizer)

# model
# activation function
activation = get_activation_by_string(settings['model']['activation'])

model = NewtonNet(resolution=settings['model']['resolution'],
               n_features=settings['model']['n_features'],
               activation=activation,
               n_interactions=settings['model']['n_interactions'],
               dropout=settings['training']['dropout'],
               max_z=10,
               cutoff=settings['data']['cutoff'],  ## data cutoff
               cutoff_network=settings['model']['cutoff_network'],
               normalizer=normalizer,
               normalize_atomic=settings['model']['normalize_atomic'],
               requires_dr=settings['model']['requires_dr'],
               device=device[0],
               create_graph=True,
               shared_interactions=settings['model']['shared_interactions'],
               return_latent=settings['model']['return_latent'],
               layer_norm=settings['model']['use_layer_norm']
               )

# laod pre-trained model
if settings['model']['pre_trained']:
    model_path = settings['model']['pre_trained']
    model.load_state_dict(torch.load(model_path)['model_state_dict'])

# optimizer
trainable_params = filter(lambda p: p.requires_grad, model.parameters())
optimizer = Adam(trainable_params,
                 lr=settings['training']['lr'],
                 weight_decay=settings['training']['weight_decay'])

# loss
w_energy = settings['model']['w_energy']
w_force = settings['model']['w_force']
w_f_mag = settings['model']['w_f_mag']
w_f_dir = settings['model']['w_f_dir']

def custom_loss(preds, batch_data, w_e=w_energy, w_f=w_force, w_fm=w_f_mag, w_fd=w_f_dir):
    # compute the mean squared error on the energies
    batch_energy = batch_data["E"].reshape((-1, 1))
    diff_energy = preds['E'] - batch_energy
    assert diff_energy.shape[1] == 1
    err_sq_energy = torch.mean(diff_energy**2)

    # compute the mean squared error on the forces
    if w_f > 0:
        diff_forces = preds['F'] - batch_data["F"]
        err_sq_forces = torch.mean(diff_forces**2)
    else:
        err_sq_forces = 0

    # compute the mean square error on the force magnitudes
    if w_fm > 0:
        diff_forces = torch.norm(preds['F'], p=2, dim=-1) - torch.norm(batch_data["F"], p=2, dim=-1)
        err_sq_mag_forces = torch.mean(diff_forces ** 2)

    if w_fd > 0:
        cos = torch.nn.CosineSimilarity(dim=-1, eps=1e-6)
        direction_diff = 1 - cos(preds['F'], batch_data["F"])
        direction_diff *= torch.norm(batch_data["F"], p=2, dim=-1)
        direction_loss = torch.mean(direction_diff)

    if settings['checkpoint']['verbose']:
        print('\n',
              '        energy loss: ', err_sq_energy, '\n',
              '        force loss: ', err_sq_forces, '\n')
              # '        mag force loss: ', err_sq_mag_forces, '\n',
              # '        direction loss: ', direction_loss)

    # build the combined loss function
    err_sq = w_e * err_sq_energy + \
             w_f * err_sq_forces
             # w_fm * err_sq_mag_forces + \
             # w_fd * err_sq_mag_forces

    return err_sq


# training
trainer = Trainer(model=model,
                  loss_fn=custom_loss,
                  optimizer=optimizer,
                  requires_dr=settings['model']['requires_dr'],
                  device=device,
                  yml_path=settings['general']['me'],
                  output_path=settings['general']['output'],
                  script_name=settings['general']['driver'],
                  lr_scheduler=settings['training']['lr_scheduler'],
                  energy_loss_w= w_energy,
                  force_loss_w=w_force,
                  loss_wf_decay=settings['model']['wf_decay'],
                  checkpoint_log=settings['checkpoint']['log'],
                  checkpoint_val=settings['checkpoint']['val'],
                  checkpoint_test=settings['checkpoint']['test'],
                  checkpoint_model=settings['checkpoint']['model'],
                  verbose=settings['checkpoint']['verbose'],
                  hooks=settings['hooks'],
                  mode="energy")

trainer.print_layers()
trainer.log_statistics(n_train_data, n_val_data, n_test_data, normalizer, test_energy_hash)

# tr_steps=1; val_steps=0; irc_steps=0; test_steps=0

trainer.train(train_generator=train_gen,
              epochs=settings['training']['epochs'],
              steps=tr_steps,
              val_generator=val_gen,
              val_steps=val_steps,
              irc_generator=None,
              irc_steps=None,
              test_generator=test_gen,
              test_steps=test_steps,
              clip_grad=1.0)

print('done!')
