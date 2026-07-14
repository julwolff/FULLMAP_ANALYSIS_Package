from averaging.matrix import average_matrix
from averaging.diffusion import average_diffusion
from averaging.occupancy import average_site_occupancy
from averaging.residence import average_residence_time
from averaging.jumps import accumulate_jump_matrix
from averaging.xrd import average_xrd



if NAME == "diffusion":

    average_diffusion(
        files,
        OUTPUT
    )

elif NAME == "site_occupancy":

    average_site_occupancy(
        files,
        OUTPUT
    )

elif NAME == "residence_time":

    average_residence_time(
        files,
        OUTPUT
    )

elif NAME == "jump_matrix":

    accumulate_jump_matrix(
        files,
        OUTPUT
    )

elif NAME.startswith("xrd_"):

    average_xrd(
        files,
        OUTPUT
    )

else:

    average_matrix(
        files,
        OUTPUT,
        compute_std=COMPUTE_STD
    )
