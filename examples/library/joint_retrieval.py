"""Fit one shared physical parameter to independent transit and eclipse spectra.

Run from the repository root with two TauREx YAML files and their observation
and opacity data in place. For example, with isothermal models in both files::

    python examples/library/joint_retrieval.py transit.yaml eclipse.yaml T 800 2400

Use ``model_type: transmission`` in the transit file and
``model_type: emission`` in the eclipse file. Both files need their own
``Observation.observed_spectrum``. The transit file sets up the shared
opacity caches. The likelihood assumes independent Gaussian errors within
and between spectra. The named parameter has a uniform prior in physical
units, and all other parameters keep their configured values.
"""

import argparse

import nestle
import numpy as np

from taurex.exceptions import InvalidModelException
from taurex.parameter import ParameterParser
from taurex.spectrum import ObservedSpectrum


def spectrum_log_likelihood(model, observation, parameter):
    """Bind one forward model to its observation and Gaussian likelihood."""
    if parameter not in model.fittingParameters:
        raise ValueError(
            f"{type(model).__name__} has no fitting parameter {parameter!r}"
        )

    data = observation.spectrum
    errors = observation.errorBar
    if (
        data.ndim != 1
        or data.size == 0
        or data.shape != errors.shape
        or not np.all(np.isfinite(data))
        or not np.all(np.isfinite(errors) & (errors > 0))
    ):
        raise ValueError("Expected finite spectral data and positive uncertainties")

    grid = observation.wavenumberGrid
    binner = observation.create_binner()
    log_normalization = np.sum(np.log(errors) + 0.5 * np.log(2 * np.pi))

    def evaluate(value):
        try:
            model[parameter] = value
            _, prediction, _, _ = binner.bin_model(model.model(wngrid=grid))
        except InvalidModelException:
            return -np.inf

        if prediction.shape != data.shape:
            raise ValueError("Binned model and observation have different shapes")
        if not np.all(np.isfinite(prediction)):
            return -np.inf

        residuals = (data - prediction) / errors
        return float(-0.5 * np.dot(residuals, residuals) - log_normalization)

    return evaluate


def load_spectrum_model(parser, filename):
    """Load and build the forward model for one observed spectrum."""
    observation = parser.generate_observation()
    if not isinstance(observation, ObservedSpectrum):
        raise ValueError(f"{filename} requires Observation.observed_spectrum")
    model = parser.generate_appropriate_model(obs=observation)
    model.build()
    return model, observation


def main():
    """Run nested sampling with one parameter shared between two spectra."""
    cli = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    cli.add_argument("transit")
    cli.add_argument("eclipse")
    cli.add_argument("parameter")
    cli.add_argument("lower", type=float)
    cli.add_argument("upper", type=float)
    args = cli.parse_args()
    if not np.all(np.isfinite([args.lower, args.upper])) or args.lower >= args.upper:
        cli.error("prior bounds must be finite and increasing")

    transit_parser = ParameterParser()
    transit_parser.read(args.transit)
    transit_parser.setup_globals()

    eclipse_parser = ParameterParser()
    eclipse_parser.read(args.eclipse)

    likelihoods = [
        spectrum_log_likelihood(*load_spectrum_model(parser, path), args.parameter)
        for parser, path in (
            (transit_parser, args.transit),
            (eclipse_parser, args.eclipse),
        )
    ]

    def log_likelihood(values):
        return sum(evaluate(values[0]) for evaluate in likelihoods)

    def prior(unit_cube):
        return args.lower + (args.upper - args.lower) * unit_cube

    result = nestle.sample(
        log_likelihood, prior, ndim=1, npoints=100, rstate=np.random.RandomState(0)
    )
    mean = np.average(result.samples[:, 0], weights=result.weights)
    print(f"Posterior mean of {args.parameter}: {mean:.6g}")


if __name__ == "__main__":
    main()
