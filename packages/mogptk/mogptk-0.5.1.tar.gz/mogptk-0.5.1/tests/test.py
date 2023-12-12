import torch
import matplotlib.pyplot as plt

i = 1
n = 1000
bins = 50
mu = torch.tensor([1.0, 2.0])
var = torch.tensor([0.1, 0.5])
var = var.diagflat()

samples = torch.distributions.multivariate_normal.MultivariateNormal(mu, var).sample([n])
print(samples.shape)
plt.hist(samples[:,i], bins=bins, density=True, label='torch')

jitter = 1e-9
eye = torch.eye(var.shape[0])
var += jitter * var.diagonal().mean() * eye  # MxM
u = torch.normal(
        torch.zeros(var.shape[0], n),
        torch.tensor(1.0))  # MxS
L = torch.linalg.cholesky(var)  # MxM
samples = mu.reshape(-1,1) + L.mm(u)  # MxS
samples = samples.T
print(samples.shape)
plt.hist(samples[:,i], bins=bins, density=True, label='mogptk')

plt.legend()
plt.show()
