import scipy.stats as stats


def gauss_truncated(lower, upper, mu, sigma):
    """
    Computes a value according to a gaussian truncated distribution
    :param lower: (float) lower bound
    :param upper: (float) upper bound
    :param mu: (float) mean of the gaussian
    :param sigma: (float) standard deviation of the gaussian
    :return: (float) x, value drawn according to gaussian truncated distribution
    """

    X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    x = X.rvs()
    return x
