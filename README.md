# OMVmodel
This repository contains firmware and the tf.lite file for the OpenMV. This firmware will have the openMV run until awoken by an external interrupt in which it will then print and uart write flood or no flood to the Boron. The openMV would then be machine.sleep() until woken again. 

