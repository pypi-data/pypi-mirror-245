import sys
import os.path
import logging
import matplotlib.scale as mscale
import matplotlib.transforms as mtransforms
import matplotlib.ticker as ticker
import numpy as np

logger = logging.getLogger('mgwas_data_exploration_app.utils')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class RecursionLimit:
    """
    Context manager to temporarily change the recursion limit.

    Example:

    with RecursionLimit(10 ** 6):
        some_function_that_requires_lots_of_recursions()
    """
    new: int
    old: int

    def __init__(self, new_recursion_limit: int):
        self.new = new_recursion_limit

    def __enter__(self):
        self.old = sys.getrecursionlimit()
        logger.debug(f'Setting new recursion limit: {self.old} -> {self.new}')
        sys.setrecursionlimit(self.new)

    def __exit__(self, *args, **kwargs):
        logger.debug(f'Setting old recursion limit: {self.new} -> {self.old}')
        sys.setrecursionlimit(self.old)


class SquareRootScale(mscale.ScaleBase):
    """
    ScaleBase class for generating square root scale.
    """

    name = 'squareroot'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self, axis)

    def set_default_locators_and_formatters(self, axis):
        axis.set_major_locator(ticker.AutoLocator())
        axis.set_major_formatter(ticker.ScalarFormatter())
        axis.set_minor_locator(ticker.NullLocator())
        axis.set_minor_formatter(ticker.NullFormatter())

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return max(0., vmin), vmax

    class SquareRootTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def transform_non_affine(self, a):
            return np.array(a) ** 0.5

        def inverted(self):
            return SquareRootScale.InvertedSquareRootTransform()

    class InvertedSquareRootTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def transform(self, a):
            return np.array(a) ** 2

        def inverted(self):
            return SquareRootScale.SquareRootTransform()

    def get_transform(self):
        return self.SquareRootTransform()


mscale.register_scale(SquareRootScale)


class MinusLog10Scale(mscale.ScaleBase):
    """
    ScaleBase class for generating -log10 scale. (Manhattan plot)
    """

    name = '-log10'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self, axis)

    def set_default_locators_and_formatters(self, axis):
        axis.set_major_locator(ticker.AutoLocator())
        axis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'-log10({x:.0e})'))
        axis.set_minor_locator(ticker.NullLocator())
        axis.set_minor_formatter(ticker.NullFormatter())

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return max(0., vmin), vmax

    class MinusLog10Transform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def transform_non_affine(self, a):
            return -np.log10(np.array(a))

        def inverted(self):
            return MinusLog10Scale.InvertedMinusLog10Transform()

    class InvertedMinusLog10Transform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def transform(self, a):
            return 10 ** -np.array(a)

        def inverted(self):
            return MinusLog10Scale.MinusLog10Transform()

    def get_transform(self):
        return self.MinusLog10Transform()


mscale.register_scale(MinusLog10Scale)
