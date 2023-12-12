# ipsos-credibility-interval

A Python tool that calculates Bayesian credibility intervals for online polling using the Ipsos method

The Ipsos credibility interval is a [Bayesian](https://en.wikipedia.org/wiki/Bayesian_inference) metric that can be used to calculate the margin of error. It estimates accuracy plus or minus a number of percentage points. You can learn more by reading [the Ipsos white paper](https://www.ipsos.com/sites/default/files/2017-03/IpsosPA_CredibilityIntervals.pdf).

## Installation

The package is available in the [Python Package Index](https://pypi.org/project/ipsos-credibility-interval/). You can install it with pipenv or another package manager.

```bash
pipenv install ipsos-credibility-interval
```

## Usage

To get an estimate, you must import the library and provide the sample size to the `get` function. It will return the credibility interval in percentage points. Here’s an example with a sample size of 1,000:

```python
import ipsos_credibility_interval

ici.get(1000)
3.5333753221609374
```

You can provide a custom [confidence level](https://en.wikipedia.org/wiki/Confidence_interval). The default is 95%. This would return the interval for a 99% confidence level:

```python
ipsos_credibility_interval.get(1000, confidence_level=0.99)
4.643642315394128
```

You can also customize the weighting factor designed by Ipsos. The default is 1.3. This example would return the interval for a weighting factor of 1.5:

```python
ipsos_credibility_interval.get(1000, weight=1.5)
3.7954539356449795
```

## Other resources

- [The Ipsos white paper](https://www.ipsos.com/sites/default/files/2017-03/IpsosPA_CredibilityIntervals.pdf)
- [Code repository](https://github.com/palewire/ipsos-credibility-interval)
- [PyPI package](https://pypi.org/project/ipsos-credibility-interval/)
