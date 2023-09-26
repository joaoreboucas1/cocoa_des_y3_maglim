from cobaya.likelihoods.des_y3_maglim._cosmolike_prototype_base import _cosmolike_prototype_base
import cosmolike_des_y3_maglim_interface as ci
import numpy as np

class des_xi_ggl(_cosmolike_prototype_base):
  # ------------------------------------------------------------------------
  # ------------------------------------------------------------------------
  # ------------------------------------------------------------------------

  def initialize(self):
    super(des_xi_ggl,self).initialize(probe="xi_ggl")

  # ------------------------------------------------------------------------
  # ------------------------------------------------------------------------
  # ------------------------------------------------------------------------

  def logp(self, **params_values):
    if self.create_baryon_pca:
      self.generate_baryonic_PCA(**params_values)
      self.force_cache_false = True

    self.set_cosmo_related()

    self.set_lens_related(**params_values)

    self.set_source_related(**params_values)

    if self.create_baryon_pca:
      self.force_cache_false = False

    # datavector C++ returns a list (not numpy array)
    datavector = np.array(ci.compute_data_vector_masked())

    if self.use_baryon_pca:
      # Warning: we assume the PCs were created with the same mask
      # We have no way of testing user enforced that
      self.set_baryon_related(**params_values)
      datavector = self.add_baryon_pcs_to_datavector(datavector)

    if self.print_datavector:
      size = len(datavector)
      out = np.zeros(shape=(size, 2))
      out[:,0] = np.arange(0, size)
      out[:,1] = datavector
      fmt = '%d', '%1.8e'
      np.savetxt(self.print_datavector_file, out, fmt = fmt)

    return self.compute_logp(datavector)

