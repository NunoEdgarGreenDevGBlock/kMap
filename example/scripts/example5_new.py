import os, sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,path + os.sep + '..' + os.sep + '..' + os.sep)
data_path = path + os.sep + '..' + os.sep + 'data' + os.sep

####
import matplotlib.pyplot as plt
import numpy as np

# Own Imports
from kmap.library.sliceddata import SlicedData
from kmap.library.orbitaldata import OrbitalData
from kmap.model.lmfit_model import LMFitModel

# load experimental data as SlicedData object
exp_data = SlicedData.init_from_hdf5(data_path + 'example5_6584.hdf5') 

# load orbitals for fitting as OrbitalData objects
orbital_paths = ['PTCDA_C.cube', 'PTCDA_D.cube',
                 'PTCDA_E.cube', 'PTCDA_F.cube']
orbitals = [OrbitalData.init_from_file(
            data_path + path, ID) for ID, path in enumerate(orbital_paths)]


# Initialize fit as LMFitModel object
lmfit = LMFitModel(exp_data, orbitals)

# Set common range and delta-k-grid for exp. and sim. kmaps
range_, dk = [-3.0, 3.0], 0.04  
lmfit.set_axis_by_step_size(range_, dk)
lmfit.set_polarization('toroid', 'p')

# Set parameters not intended for fitting to desired value
lmfit.edit_parameter('E_kin', value=27.2, vary=False)
lmfit.edit_parameter('alpha', value=40, vary=False)

# Activate fitting for background ('c') and all orbital weights 
lmfit.edit_parameter('c', value=1, vary=True)  # constant background
for i in [0, 1, 2, 3]:
    lmfit.edit_parameter('w_' + str(i), vary=True)

# Set slices to be used and perform fit
lmfit.set_slices('all', combined=False)
lmfit.set_fit_method(method='leastsq', xtol=1e-7)
results = lmfit.fit()

# extract fitting results
weights = np.array([[result.params['w_0'].value,
                     result.params['w_1'].value,
                     result.params['w_2'].value,
                     result.params['w_3'].value]
                        for result in results])

print(weights)

# Plot results: weights of orbitals (pDOS) vs. kinetic energy
names  = ['PTCDA_C','PTCDA_D','PTCDA_E','PTCDA_F']
styles = ['.r-','k-','r--','^g-']
fig,ax  = plt.subplots(figsize=(12,5))
x       = exp_data.axes[0].axis
x_label = exp_data.axes[0].label + '(' + exp_data.axes[0].units + ')'
for j,p in enumerate(names):
    ax.plot(x,weights[:,j],styles[j],label=p)
plt.legend()
plt.xlabel(x_label)
plt.ylabel('weights (arb. units)')
#plt.savefig('Fig6_deconvolution.png',dpi=300)
plt.show()
