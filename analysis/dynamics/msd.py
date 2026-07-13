import numpy as np

from MDAnalysis.analysis.msd import EinsteinMSD

def compute_msd_and_diff(
        u,
        time,
        selection,
        label):

    msd = EinsteinMSD(
        u,
        select=selection,
        msd_type="xyz"
    )

    msd.run()

    values = msd.results.timeseries

    start = int(0.3 * len(time))
    end = int(0.8 * len(time))

    slope = np.polyfit(
        time[start:end],
        values[start:end],
        1
    )[0]

    D = slope / 6.0

    return values, D
