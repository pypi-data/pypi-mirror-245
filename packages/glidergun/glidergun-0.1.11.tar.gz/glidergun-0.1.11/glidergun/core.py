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
from rasterio.io import MemoryFile
from rasterio.transform import Affine
from rasterio.warp import calculate_default_transform, reproject, Resampling
from typing import Any, Callable, Iterable, List, Tuple, Union, overload
from glidergun.constants import ColorMap, DataType


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


Value = Union[float, int]

Operand = Union["Grid", float, int]


@dataclass(frozen=True)
class Grid:
    data: ndarray
    crs: CRS
    transform: Affine
    _cmap: ColorMap = "gray"

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

    # Methods

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

        l_adjusted, r_adjusted = _standardize(True, left, right)

        return self._create(op(l_adjusted.data, r_adjusted.data))

    def is_nan(self):
        return self.local(np.isnan)

    def local(self, func: Callable[[ndarray], ndarray]):
        return self._create(func(self.data))

    def _focal(self, func: Callable, buffer: int = 1):
        blocks = _generate_blocks(self, buffer)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            with futures.ProcessPoolExecutor() as executor:
                return self._create(np.array(list(executor.map(func, blocks))))

    def focal(
        self, func: Callable[[ndarray], Any], buffer: int = 1, max_workers: int = 1
    ) -> "Grid":
        return focal(lambda data: func(data[0]), buffer, max_workers, self)[0]

    def focal_mean(self, buffer=1, ignore_nan: bool = False) -> "Grid":
        return self._focal(_nanmean if ignore_nan else _mean, buffer)

    def focal_std(self, buffer=1, ignore_nan: bool = False) -> "Grid":
        return self._focal(_nanstd if ignore_nan else _std, buffer)

    def focal_min(self, buffer=1, ignore_nan: bool = False) -> "Grid":
        return self.focal(np.nanmin if ignore_nan else np.min, buffer)

    def focal_max(self, buffer=1, ignore_nan: bool = False) -> "Grid":
        return self.focal(np.nanmax if ignore_nan else np.max, buffer)

    def focal_sum(self, buffer=1, ignore_nan: bool = False) -> "Grid":
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

    def value(self, x: float, y: float) -> Value:
        xoff = (x - self.xmin) / self.transform.a
        yoff = (y - self.ymax) / self.transform.e
        if xoff < 0 or xoff >= self.width or yoff < 0 or yoff >= self.height:
            return np.nan
        return self.data[int(yoff), int(xoff)]

    def data_extent(self):
        xmin, ymin, xmax, ymax = None, None, None, None
        for x, y, _ in self.to_points():
            if not xmin or x < xmin:
                xmin = x
            if not ymin or y < ymin:
                ymin = y
            if not xmax or x > xmax:
                xmax = x
            if not ymax or y > ymax:
                ymax = y
        if xmin is None or ymin is None or xmax is None or ymax is None:
            raise ValueError("None of the cells has a value.")
        n = self.cell_size / 2
        return Extent(xmin - n, ymin - n, xmax + n, ymax + n)

    def shrink(self):
        return self.clip(self.data_extent())

    def to_points(self) -> Iterable[Tuple[float, float, Value]]:
        n = self.cell_size / 2
        for y, row in enumerate(self.data):
            for x, value in enumerate(row):
                if np.isfinite(value):
                    yield self.xmin + x * self.cell_size + n, self.ymax - y * self.cell_size - n, value

    def plot(self, cmap: ColorMap):
        return dataclasses.replace(self, _cmap=cmap)

    def type(self, dtype: DataType):
        return self.local(lambda data: np.asanyarray(data, dtype=dtype))

    @overload
    def save(self, file: str, driver: str = ""):
        ...

    @overload
    def save(self, file: MemoryFile, driver: str = ""):
        ...

    def save(self, file, driver: str = ""):
        if isinstance(file, str):
            with rasterio.open(
                file,
                "w",
                driver=driver if driver else driver_from_extension(file),
                count=1,
                **_metadata(self),
            ) as dataset:
                dataset.write(self.data, 1)
        elif isinstance(file, MemoryFile):
            with file.open(
                driver=driver if driver else "GTiff",
                count=1,
                **_metadata(self),
            ) as dataset:
                dataset.write(self.data, 1)


# Grid functions


@overload
def grid(file: str, index: int = 1) -> Grid:
    ...


@overload
def grid(file: MemoryFile, index: int = 1) -> Grid:
    ...


def grid(file, index: int = 1) -> Grid:
    if isinstance(file, str):
        with rasterio.open(file) as dataset:
            return _read(dataset, index)
    elif isinstance(file, MemoryFile):
        with file.open() as dataset:
            return _read(dataset, index)
    raise ValueError()


def _read(dataset, index):
    grid = Grid(dataset.read(index), dataset.crs, dataset.transform)
    return grid


def _metadata(grid: Grid):
    return {
        "height": grid.height,
        "width": grid.width,
        "crs": grid.crs,
        "transform": grid.transform,
        "dtype": grid.data.dtype,
        "nodata": grid.nodata,
    }


def _generate_blocks(grid: Grid, buffer: int):
    row = np.zeros((buffer, grid.width)) * np.nan
    col = np.zeros((grid.height + 2 * buffer, buffer)) * np.nan
    array = np.hstack([col, np.vstack([row, grid.data, row]), col])
    window = (2 * buffer + 1, 2 * buffer + 1)
    shape = tuple(np.subtract(array.shape, window) + 1) + window
    return as_strided(array, shape, array.strides * 2)


def focal(
    func: Callable[[np.ndarray], Union[Value, Tuple[Value, ...]]],
    buffer: int,
    max_workers: int,
    *grids: Grid,
) -> Tuple[Grid, ...]:
    grids_adjusted = _standardize(True, *grids)
    stacks = np.stack([_generate_blocks(g, buffer) for g in grids_adjusted], axis=2)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        if max_workers > 1:
            with futures.ProcessPoolExecutor() as executor:
                rows = [list(executor.map(func, stack)) for stack in stacks]
        else:
            rows = [list(map(func, block_stack)) for block_stack in stacks]

        count = len(rows[0][0]) if isinstance(rows[0][0], tuple) else 1

        arrays = [
            [[n[i] if isinstance(n, tuple) else n for n in row] for row in rows]
            for i in range(count)
        ]

        return tuple([grids_adjusted[0]._create(np.array(array)) for array in arrays])


def con(grid: Grid, trueValue: Operand, falseValue: Operand):
    return grid.local(
        lambda data: np.where(data, grid._data(trueValue), grid._data(falseValue))
    )


def aggregate(func: Callable, *grids: Grid) -> Grid:
    grids_adjusted = _standardize(True, *grids)
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


def mosaic(*grids: Grid) -> Grid:
    grids_adjusted = _standardize(False, *grids)
    result = grids_adjusted[0]
    for grid in grids_adjusted[1:]:
        result = con(result.is_nan(), grid, result)
    return result


def _nanmean(data):
    return list(map(np.nanmean, data))


def _mean(data):
    return list(map(np.mean, data))


def _nanstd(data):
    return list(map(np.nanstd, data[0]))


def _std(data):
    return list(map(np.std, data))


def _standardize(intersect: bool, *grids: Grid) -> List[Grid]:
    if len(grids) == 1:
        return list(grids)

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


@dataclass(frozen=True)
class Stack:
    grids: Tuple[Grid, ...]
    _rgb: Tuple[int, int, int] = (1, 2, 3)

    def __repr__(self):
        g = self.grids[0]
        return f"image: {g.width}x{g.height} {g.dtype} | crs: {g.crs} | cell: {g.cell_size} | count: {len(self.grids)}"

    # Methods

    def plot(self, *rgb: int):
        return dataclasses.replace(self, _rgb=rgb)

    def map(self, func: Callable[[Grid], Grid]):
        return stack(*map(func, self.grids))

    def zip_with(self, other_stack: "Stack", func: Callable[[Grid, Grid], Grid]):
        grids = []
        for grid1, grid2 in zip(self.grids, other_stack.grids):
            grid1, grid2 = _standardize(True, grid1, grid2)
            grids.append(func(grid1, grid2))
        return stack(*grids)

    def values(self, x: float, y: float):
        return tuple(grid.value(x, y) for grid in self.grids)

    @overload
    def save(self, file: str, driver: str = ""):
        ...

    @overload
    def save(self, file: MemoryFile, driver: str = ""):
        ...

    def save(self, file, driver: str = ""):
        g = self.grids[0]
        if isinstance(file, str):
            with rasterio.open(
                file,
                "w",
                driver=driver if driver else driver_from_extension(file),
                count=len(self.grids),
                **_metadata(g),
            ) as dataset:
                for index, grid in enumerate(self.grids):
                    dataset.write(grid.data, index + 1)
        elif isinstance(file, MemoryFile):
            with file.open(
                driver=driver if driver else "GTiff",
                count=len(self.grids),
                **_metadata(g),
            ) as dataset:
                for index, grid in enumerate(self.grids):
                    dataset.write(grid.data, index + 1)


# Stack functions


@overload
def stack(*grids: str) -> Stack:
    ...


@overload
def stack(*grids: MemoryFile) -> Stack:
    ...


@overload
def stack(*grids: Grid) -> Stack:
    ...


def stack(*grids) -> Stack:
    bands: List[Grid] = []

    for grid in grids:
        if isinstance(grid, Grid):
            bands.append(grid)
        else:
            with rasterio.open(grid) if isinstance(
                grid, str
            ) else grid.open() as dataset:
                for index in dataset.indexes:
                    band = _read(dataset, index)
                    bands.append(band)

    return Stack(tuple(_standardize(True, *bands)))


# IPython support

ipython = IPython.get_ipython()  # type: ignore

if ipython:

    def html(obj: Union[Grid, Stack]):
        with BytesIO() as buffer:
            figure = pyplot.figure(frameon=False)
            axes = figure.add_axes((0, 0, 1, 1))
            axes.axis("off")
            if isinstance(obj, Grid):
                pyplot.imshow(obj.data, cmap=obj._cmap)
                extent = obj.extent
            elif isinstance(obj, Stack):
                pyplot.imshow(
                    np.dstack([obj.grids[i - 1].type("uint8").data for i in obj._rgb])
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
