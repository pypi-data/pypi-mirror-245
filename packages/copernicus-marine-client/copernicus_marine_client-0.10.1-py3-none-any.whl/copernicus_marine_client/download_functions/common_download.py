import logging
import pathlib

import xarray
import zarr
from dask.delayed import Delayed
from tqdm.dask import TqdmCallback

logger = logging.getLogger("copernicus_marine_root_logger")


def get_delayed_download(dataset: xarray.Dataset, output_path: pathlib.Path):
    if output_path.suffix == ".nc":
        delayed = _prepare_download_dataset_as_netcdf(dataset, output_path)
    elif output_path.suffix == ".zarr":
        delayed = _prepare_download_dataset_as_zarr(dataset, output_path)
    else:
        delayed = _prepare_download_dataset_as_netcdf(dataset, output_path)
    return delayed


def download_delayed_dataset(
    delayed: Delayed, disable_progress_bar: bool
) -> None:
    if disable_progress_bar:
        delayed.compute()
    else:
        with TqdmCallback():
            delayed.compute()


def _prepare_download_dataset_as_netcdf(
    dataset: xarray.Dataset, output_path: pathlib.Path
):
    logger.debug("Writing dataset to NetCDF")
    return dataset.to_netcdf(output_path, mode="w", compute=False)


def _prepare_download_dataset_as_zarr(
    dataset: xarray.Dataset, output_path: pathlib.Path
):
    logger.debug("Writing dataset to Zarr")
    store = zarr.DirectoryStore(output_path)
    return dataset.to_zarr(store=store, mode="w", compute=False)
