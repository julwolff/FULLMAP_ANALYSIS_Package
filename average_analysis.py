from averaging.matrix import average_matrix
from averaging.diffusion import average_diffusion
from averaging.jumps import average_jumps
from averaging.occupancy import average_occupancy

if NAME == "diffusion":

    average_diffusion(files)

elif NAME == "jump_matrix":

    average_jumps(files)

elif NAME == "site_occupancy":

    average_occupancy(files)

else:

    average_matrix(files)
