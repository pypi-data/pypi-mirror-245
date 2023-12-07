import numpy as np
from numpy import float_
from numpy.typing import NDArray


def gen_cdf(pdf: NDArray[float_]) -> NDArray[float_]:
    """
    Create a cumulative distribution from a probability distribution.
    """
    cdf = np.zeros(len(pdf))

    for n in range(len(pdf)):
        cdf[n] = np.sum(pdf[:n])

    return cdf / cdf.max()


def gen_dist(n_samples: int, x: NDArray[float_], cdf: NDArray[float_]) -> NDArray[float_]:
    """
    Generate a distribution sample from a CDF.
    """
    dist = np.zeros(n_samples)

    for n in range(n_samples):
        y = np.random.rand()
        dist[n] = np.interp(y, cdf, x)

    return dist


def weibull_curve(x: NDArray[float_], mean: float, shape: float) -> NDArray[float_]:
    """
    Create a weibull curve.
    """
    return (shape / mean) * (x / mean) ** (shape - 1) * np.exp(-((x / mean) ** shape))


def weibull_samples(n_samples: int, mean: float, sigma: float) -> NDArray[float_]:
    """
    Generate a random wind value based on a weibull.
    """
    if sigma > 0.0:
        shape = mean / sigma
    else:
        shape = 1e6

    return mean * np.random.weibull(shape, n_samples)


def weibull_reverse_samples(n_samples, mean, sigma, scale=1.0):
    """
    Generate a random absorptivity/emissivity based on a weibull between 0 and 1.
    """
    mean_backward = scale - mean

    if sigma > 0.0:
        shape = mean_backward / sigma
    else:
        shape = 1e12

    return np.abs(scale - mean_backward * np.random.weibull(shape, n_samples))


def gen_wind_samples(n_samles, speed_mean, speed_sigma):
    """
    Generate wind distribution.
    """
    air_speed_fraction = abs(speed_mean) / 5.0

    air_speed_flops = weibull_samples(
        n_samples=n_samples,
        mean=speed_mean,
        sigma=speed_sigma * air_speed_fraction,
    )

    air_speed_flops[air_speed_flops > 2 * speed_mean] = 8 * speed_mean

    return air_speed_flops


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    n_samples = 10000
    n_bins = int(np.sqrt(n_samples) / 3)

    # Air Speed
    air_speed_mean = 1.5
    air_speed_sigma = 1.0
    air_speed_dist = weibull_samples(n_samples, air_speed_mean, air_speed_sigma)

    as_fig, as_ax = plt.subplots(1, 1)
    as_ax.set(xlabel="Air Speed [m/s]", xlim=(0, 5.2))

    label = "$\\sigma$" + f" = {air_speed_sigma} m/s"
    as_ax.hist(air_speed_dist, n_bins, alpha=0.7, color="skyblue", histtype="stepfilled", lw=2, label=label)
    as_ax.axvline(air_speed_mean, color="blue", ls="--", label="mean")

    # Emissivity
    emissivity_mean = 0.8
    emissivity_sigma = 0.03
    emissivity_dist = weibull_reverse_samples(n_samples, emissivity_mean, emissivity_sigma, scale=1.0)

    em_fig, em_ax = plt.subplots(1, 1)
    em_ax.set(xlabel="Absorptivity / Emissivity", xlim=(0, 1.1))

    label = "$\\sigma$" + f" = {emissivity_sigma:.2f}"
    em_ax.hist(emissivity_dist, n_bins, alpha=0.7, color="green", histtype="stepfilled", lw=2, label=label)
    em_ax.axvline(emissivity_mean, color="darkgreen", ls="--", label="mean")

    # Conductor Temperature
    cond_temp_mean = 30.0
    cond_temp_sigma = 2.0
    cond_temp_dist = np.random.normal(cond_temp_mean, cond_temp_sigma, n_samples)

    ct_fig, ct_ax = plt.subplots(1, 1)
    ct_ax.set(xlabel="Conductor Temperature [$^{\\circ} C$]", xlim=(18, 42))

    label = "$\\sigma$" + f" = {cond_temp_sigma:.1f}" + " $^{\\circ} C$"
    ct_ax.hist(cond_temp_dist, n_bins, alpha=0.7, color="red", histtype="stepfilled", lw=2, label=label)
    ct_ax.axvline(cond_temp_mean, color="darkred", ls="--", label="mean")

    # Axes
    for ax in [as_ax, em_ax, ct_ax]:
        ax.minorticks_on()
        ax.grid()
        ax.legend()

    # SHOW
    plt.show()
