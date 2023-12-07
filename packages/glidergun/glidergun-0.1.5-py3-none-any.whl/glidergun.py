""" Map Algebra with NumPy and Rasterio """
import dataclasses
import IPython
import numpy as np
import rasterio
import warnings
from base64 import b64encode
from concurrent import futures
from dataclasses import dataclass
from io import BytesIO
from matplotlib import pyplot
from numpy import arctan, arctan2, cos, gradient, ndarray, pi, sin, sqrt
from numpy.lib.stride_tricks import as_strided
from rasterio.crs import CRS
from rasterio.drivers import driver_from_extension
from rasterio.transform import Affine
from rasterio.warp import calculate_default_transform, reproject, Resampling
from typing import Callable, List, Literal, Tuple, Union, overload

# Types

ColorMap = Literal[
    "Accent",
    "afmhot",
    "autumn",
    "binary",
    "Blues",
    "bone",
    "BrBG",
    "brg",
    "BuGn",
    "BuPu",
    "bwr",
    "cividis",
    "CMRmap",
    "cool",
    "coolwarm",
    "copper",
    "cubehelix",
    "Dark2",
    "flag",
    "gist_earth",
    "gist_gray",
    "gist_heat",
    "gist_ncar",
    "gist_rainbow",
    "gist_stern",
    "gist_yarg",
    "GnBu",
    "gnuplot",
    "gnuplot2",
    "gray",
    "Greens",
    "Greys",
    "hot",
    "hsv",
    "inferno",
    "jet",
    "magma",
    "nipy_spectral",
    "ocean",
    "Oranges",
    "OrRd",
    "Paired",
    "Pastel1",
    "Pastel2",
    "pink",
    "PiYG",
    "plasma",
    "PRGn",
    "prism",
    "PuBu",
    "PuBuGn",
    "PuOr",
    "PuRd",
    "Purples",
    "rainbow",
    "RdBu",
    "RdGy",
    "RdPu",
    "RdYlBu",
    "RdYlGn",
    "Reds",
    "seismic",
    "Set1",
    "Set2",
    "Set3",
    "Spectral",
    "spring",
    "summer",
    "tab10",
    "tab20",
    "tab20b",
    "tab20c",
    "terrain",
    "turbo",
    "twilight",
    "twilight_shifted",
    "viridis",
    "winter",
    "Wistia",
    "YlGn",
    "YlGnBu",
    "YlOrBr",
    "YlOrRd",
]

DataType = Literal[
    "float32",
    "float64",
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
]


class Extent(Tuple[float, float, float, float]):
    def __new__(cls, xmin: float, ymin: float, xmax: float, ymax: float):
        return super(Extent, cls).__new__(cls, (xmin, ymin, xmax, ymax))

    def intersect(self, extent: "Extent"):
        return Extent(*[f(x) for f, x in zip((max, max, min, min), zip(self, extent))])

    def union(self, extent: "Extent"):
        return Extent(*[f(x) for f, x in zip((min, min, max, max), zip(self, extent))])

    __and__ = intersect
    __rand__ = __and__
    __or__ = union
    __ror__ = __or__


Operand = Union["Grid", float, int]


@dataclass(frozen=True)
class Grid:
    data: ndarray
    crs: CRS
    transform: Affine
    cmap: ColorMap = "gray"

    def __post_init__(self):
        self.data.flags.writeable = False

    def __repr__(self):
        d = 3 if self.dtype.startswith("float") else 0
        return (
            f"image: {self.width}x{self.height} {self.dtype} | range: {self.min:.{d}f}~{self.max:.{d}f}"
            + f" | mean: {self.mean:.{d}f} | std: {self.std:.{d}f} | crs: {self.crs} | cell: {self.cell_size}"
        )

    # Properties

    @property
    def width(self) -> int:
        return self.data.shape[1]

    @property
    def height(self) -> int:
        return self.data.shape[0]

    @property
    def dtype(self) -> DataType:
        return str(self.data.dtype)  # type: ignore

    @property
    def nodata(self):
        if self.dtype == "bool":
            return None
        if self.dtype.startswith("float"):
            return np.finfo(self.dtype).min
        if self.dtype.startswith("uint"):
            return np.iinfo(self.dtype).max
        return np.iinfo(self.dtype).min

    @property
    def has_nan(self) -> bool:
        return self.is_nan().data.any()

    @property
    def xmin(self) -> float:
        return self.transform.c

    @property
    def ymin(self) -> float:
        return self.ymax + self.height * self.transform.e

    @property
    def xmax(self) -> float:
        return self.xmin + self.width * self.transform.a

    @property
    def ymax(self) -> float:
        return self.transform.f

    @property
    def extent(self) -> Extent:
        return Extent(self.xmin, self.ymin, self.xmax, self.ymax)

    @property
    def mean(self) -> float:
        return np.nanmean(self.data)

    @property
    def std(self) -> float:
        return np.nanstd(self.data)

    @property
    def min(self) -> float:
        return np.nanmin(self.data)

    @property
    def max(self) -> float:
        return np.nanmax(self.data)

    @property
    def cell_size(self) -> float:
        return self.transform.a

    # Operators

    def __add__(self, n: Operand):
        return self._apply(self, n, np.add)

    __radd__ = __add__

    def __sub__(self, n: Operand):
        return self._apply(self, n, np.subtract)

    def __rsub__(self, n: Operand):
        return self._apply(n, self, np.subtract)

    def __mul__(self, n: Operand):
        return self._apply(self, n, np.multiply)

    __rmul__ = __mul__

    def __pow__(self, n: Operand):
        return self._apply(self, n, np.power)

    def __rpow__(self, n: Operand):
        return self._apply(n, self, np.power)

    def __truediv__(self, n: Operand):
        return self._apply(self, n, np.true_divide)

    def __rtruediv__(self, n: Operand):
        return self._apply(n, self, np.true_divide)

    def __floordiv__(self, n: Operand):
        return self._apply(self, n, np.floor_divide)

    def __rfloordiv__(self, n: Operand):
        return self._apply(n, self, np.floor_divide)

    def __mod__(self, n: Operand):
        return self._apply(self, n, np.mod)

    def __rmod__(self, n: Operand):
        return self._apply(n, self, np.mod)

    def __lt__(self, n: Operand):
        return self._apply(self, n, np.less)

    def __gt__(self, n: Operand):
        return self._apply(self, n, np.greater)

    __rlt__ = __gt__

    __rgt__ = __lt__

    def __le__(self, n: Operand):
        return self._apply(self, n, np.less_equal)

    def __ge__(self, n: Operand):
        return self._apply(self, n, np.greater_equal)

    __rle__ = __ge__

    __rge__ = __le__

    def __eq__(self, n: Operand):
        return self._apply(self, n, np.equal)

    __req__ = __eq__

    def __ne__(self, n: Operand):
        return self._apply(self, n, np.not_equal)

    __rne__ = __ne__

    def __and__(self, n: Operand):
        return self._apply(self, n, np.bitwise_and)

    __rand__ = __and__

    def __or__(self, n: Operand):
        return self._apply(self, n, np.bitwise_or)

    __ror__ = __or__

    def __xor__(self, n: Operand):
        return self._apply(self, n, np.bitwise_xor)

    def __rxor__(self, n: Operand):
        return self._apply(n, self, np.bitwise_xor)

    def __rshift__(self, n: Operand):
        return self._apply(self, n, np.right_shift)

    def __lshift__(self, n: Operand):
        return self._apply(self, n, np.left_shift)

    __rrshift__ = __lshift__

    __rlshift__ = __rshift__

    def __neg__(self):
        return self._create(-1 * self.data)

    def __pos__(self):
        return self._create(1 * self.data)

    def __invert__(self):
        return con(self, False, True)

    # Instance methods

    def _create(self, data: ndarray):
        return Grid(data, self.crs, self.transform)

    def _data(self, n: Operand):
        if isinstance(n, Grid):
            return n.data
        return n

    def _apply(self, left: Operand, right: Operand, op: Callable):
        if not isinstance(left, Grid) or not isinstance(right, Grid):
            return self._create(op(self._data(left), self._data(right)))

        if left.cell_size == right.cell_size and left.extent == right.extent:
            return self._create(op(left.data, right.data))

        l_adjusted, r_adjusted = standardize(True, left, right)

        return self._create(op(l_adjusted.data, r_adjusted.data))

    def is_nan(self):
        return self.local(np.isnan)

    def local(self, func: Callable[[ndarray], ndarray]):
        return self._create(func(self.data))

    def _get_blocks(self, buffer: int):
        row = np.zeros((buffer, self.width)) * np.nan
        col = np.zeros((self.height + 2 * buffer, buffer)) * np.nan
        array = np.hstack([col, np.vstack([row, self.data, row]), col])
        window = (2 * buffer + 1, 2 * buffer + 1)
        shape = tuple(np.subtract(array.shape, window) + 1) + window
        return as_strided(array, shape, array.strides * 2)

    def focal(self, func: Callable[[ndarray], Union[float, int]], buffer: int = 1):
        blocks = self._get_blocks(buffer)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            return self._create(np.array([list(map(func, block)) for block in blocks]))

    def _focal(self, func: Callable, buffer: int = 1):
        blocks = self._get_blocks(buffer)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            with futures.ProcessPoolExecutor() as executor:
                return self._create(np.array(list(executor.map(func, blocks))))

    def focal_mean(self, buffer=1, ignore_nan: bool = False):
        return self._focal(_nanmean if ignore_nan else _mean, buffer)

    def focal_std(self, buffer=1, ignore_nan: bool = False):
        return self._focal(_nanstd if ignore_nan else _std, buffer)

    def focal_min(self, buffer=1, ignore_nan: bool = False):
        return self.focal(np.nanmin if ignore_nan else np.min, buffer)

    def focal_max(self, buffer=1, ignore_nan: bool = False):
        return self.focal(np.nanmax if ignore_nan else np.max, buffer)

    def focal_sum(self, buffer=1, ignore_nan: bool = False):
        return self.focal(np.nansum if ignore_nan else np.sum, buffer)

    def _reproject(self, transform, crs, width, height, resampling: Resampling):
        grid = self.type("float64")
        destination = np.ones((round(height), round(width)), grid.dtype) * np.nan
        reproject(
            source=grid.data,
            destination=destination,
            src_transform=grid.transform,
            src_crs=grid.crs,
            src_nodata=grid.nodata,
            dst_transform=transform,
            dst_crs=crs,
            dst_nodata=grid.nodata,
            resampling=resampling,
        )
        result = Grid(destination, crs, transform)
        return con(result == result.nodata, np.nan, result)

    def project(
        self, epsg: Union[int, CRS], resampling: Resampling = Resampling.nearest
    ):
        crs = CRS.from_epsg(epsg) if isinstance(epsg, int) else epsg
        transform, width, height = calculate_default_transform(
            self.crs, crs, self.width, self.height, *self.extent
        )
        return self._reproject(transform, crs, width, height, resampling)

    def _resample(
        self,
        extent: Tuple[float, float, float, float],
        cell_size: float,
        resampling: Resampling,
    ):
        (xmin, ymin, xmax, ymax) = extent
        xoff = (xmin - self.xmin) / self.transform.a
        yoff = (ymax - self.ymax) / self.transform.e
        scaling = cell_size / self.cell_size
        transform = (
            self.transform * Affine.translation(xoff, yoff) * Affine.scale(scaling)
        )
        width = (xmax - xmin) / abs(self.transform.a) / scaling
        height = (ymax - ymin) / abs(self.transform.e) / scaling
        return self._reproject(transform, self.crs, width, height, resampling)

    def clip(self, extent: Tuple[float, float, float, float]):
        return self._resample(extent, self.cell_size, Resampling.nearest)

    def resample(self, cell_size: float, resampling: Resampling = Resampling.nearest):
        return self._resample(self.extent, cell_size, resampling)

    def abs(self):
        return self.local(np.abs)

    def zeros(self):
        return self.local(np.zeros_like)

    def ones(self):
        return self.local(np.ones_like)

    def random(self):
        return self._create(np.random.rand(self.height, self.width))

    def round(self, decimals: int = 0):
        return self.local(lambda data: np.round(data, decimals))

    def aspect(self):
        x, y = gradient(self.data)
        return self._create(arctan2(-x, y))

    def slope(self):
        x, y = gradient(self.data)
        return self._create(pi / 2.0 - arctan(sqrt(x * x + y * y)))

    def hillshade(self, azimuth: float = 315, altitude: float = 45):
        azimuth = np.deg2rad(azimuth)
        altitude = np.deg2rad(altitude)
        aspect = self.aspect().data
        slope = self.slope().data
        shaded = sin(altitude) * sin(slope) + cos(altitude) * cos(slope) * cos(
            azimuth - aspect
        )
        return self._create((255 * (shaded + 1) / 2))

    def fill_nan(self):
        grid = self
        n = 0
        while grid.has_nan:
            grid = con(grid.is_nan(), grid.focal_mean(2**n, ignore_nan=True), grid)
            n += 1
        return grid

    def replace(self, value: Operand, replacement: Operand):
        return con(
            value if isinstance(value, Grid) else self == value, replacement, self
        )

    def set_nan(self, value: Operand):
        return self.replace(value, np.nan)

    def value(self, x: float, y: float) -> Union[None, float, int]:
        xoff = (x - self.xmin) / self.transform.a
        yoff = (y - self.ymax) / self.transform.e
        if xoff < 0 or xoff >= self.width or yoff < 0 or yoff >= self.height:
            return None
        return self.data[int(yoff), int(xoff)]

    def plot(self, cmap: ColorMap):
        return dataclasses.replace(self, cmap=cmap)

    def type(self, dtype: DataType):
        return self.local(lambda data: np.asanyarray(data, dtype=dtype))

    def save(self, file: str):
        with rasterio.open(
            file,
            "w",
            driver=driver_from_extension(file),
            height=self.height,
            width=self.width,
            count=1,
            crs=self.crs,
            transform=self.transform,
            dtype=self.data.dtype,
            nodata=self.nodata,
        ) as dataset:
            dataset.write(self.data, 1)


# Grid functions


def grid(file: str, band: int = 1):
    with rasterio.open(file) as dataset:
        return Grid(dataset.read(band), dataset.crs, dataset.transform)


def _nanmean(data):
    return list(map(np.nanmean, data))


def _mean(data):
    return list(map(np.mean, data))


def _nanstd(data):
    return list(map(np.nanstd, data))


def _std(data):
    return list(map(np.std, data))


def con(grid: Grid, trueValue: Operand, falseValue: Operand):
    return grid.local(
        lambda data: np.where(data, grid._data(trueValue), grid._data(falseValue))
    )


def standardize(intersect: bool, *grids: Grid) -> List[Grid]:
    crs_set = set(grid.crs for grid in grids)

    if len(crs_set) > 1:
        raise ValueError("Input grids must have the same CRS.")

    cell_size = 0
    extent = None

    for grid in grids:
        cell_size = grid.cell_size if grid.cell_size > cell_size else cell_size
        extent = (
            grid.extent
            if extent is None
            else extent & grid.extent
            if intersect
            else extent | grid.extent
        )

    results = []

    for grid in grids:
        if grid.cell_size != cell_size:
            grid = grid.resample(cell_size)
        if grid.extent != extent:
            grid = grid.clip(extent)  # type: ignore
        results.append(grid)

    return results


def aggregate(func: Callable, *grids: Grid) -> Grid:
    grids_adjusted = standardize(True, *grids)
    data = func(np.array([grid.data for grid in grids_adjusted]), axis=0)
    return grids_adjusted[0]._create(data)


def mean(*grids: Grid) -> Grid:
    return aggregate(np.mean, *grids)


def std(*grids: Grid) -> Grid:
    return aggregate(np.std, *grids)


def minimum(*grids: Grid) -> Grid:
    return aggregate(np.min, *grids)


def maximum(*grids: Grid) -> Grid:
    return aggregate(np.max, *grids)


def sum(*grids: Grid) -> Grid:
    return aggregate(np.sum, *grids)


def mosaic(*grids: Grid) -> Grid:
    grids_adjusted = standardize(False, *grids)
    result = grids_adjusted[0]
    for grid in grids_adjusted[1:]:
        result = con(result.is_nan(), grid, result)
    return result


@dataclass(frozen=True)
class Stack:
    grids: Tuple[Grid, ...]
    rgb: Tuple[int, int, int] = (1, 2, 3)

    def __repr__(self):
        g = self.grids[0]
        return f"image: {g.width}x{g.height} {g.dtype} | crs: {g.crs} | cell: {g.cell_size} | count: {len(self.grids)}"

    def plot(self, *rgb: int):
        return dataclasses.replace(self, rgb=rgb)

    def map(self, func: Callable[[Grid], Grid]):
        return stack(*map(func, self.grids))

    def values(self, x: float, y: float):
        return tuple(grid.value(x, y) for grid in self.grids)

    def save(self, file: str):
        g = self.grids[0]
        with rasterio.open(
            file,
            "w",
            driver=driver_from_extension(file),
            height=g.height,
            width=g.width,
            count=len(self.grids),
            crs=g.crs,
            transform=g.transform,
            dtype=g.data.dtype,
            nodata=g.nodata,
        ) as dataset:
            for index, grid in enumerate(self.grids):
                dataset.write(grid.data, index + 1)


# Stack functions


@overload
def stack(*grids: str) -> Stack:
    ...


@overload
def stack(*grids: Grid) -> Stack:
    ...


def stack(*grids) -> Stack:
    bands: List[Grid] = []

    for grid in grids:
        if isinstance(grid, str):
            with rasterio.open(grid) as dataset:
                for index in dataset.indexes:
                    band = Grid(dataset.read(index), dataset.crs, dataset.transform)
                    bands.append(band)
        else:
            bands.append(grid)

    return Stack(tuple(standardize(True, *bands)))


# IPython support

ipython = IPython.get_ipython()  # type: ignore

if ipython:

    def html(obj: Union[Grid, Stack]):
        with BytesIO() as buffer:
            figure = pyplot.figure(frameon=False)
            axes = figure.add_axes((0, 0, 1, 1))
            axes.axis("off")
            if isinstance(obj, Grid):
                pyplot.imshow(obj.data, cmap=obj.cmap)
                extent = obj.extent
            elif isinstance(obj, Stack):
                pyplot.imshow(
                    np.dstack([obj.grids[i - 1].type("uint8").data for i in obj.rgb])
                )
                extent = obj.grids[0].extent
            pyplot.savefig(buffer)
            pyplot.close(figure)
            description = str(obj).replace("|", "<br />")
            image = b64encode(buffer.getvalue()).decode()
            return f'<div>{description}</div><img src="data:image/png;base64, {image}" /><div>{extent}</div>'

    formatter = ipython.display_formatter.formatters["text/html"]  # type: ignore
    formatter.for_type(Grid, html)
    formatter.for_type(Stack, html)
    formatter.for_type(
        tuple,
        lambda items: f"""
            <table>
                <tr style="text-align: left">
                    {"".join(f"<td>{html(item)}</td>" for item in items)}
                </tr>
            </table>
        """
        if all(isinstance(item, Grid) or isinstance(item, Stack) for item in items)
        else f"{items}",
    )
