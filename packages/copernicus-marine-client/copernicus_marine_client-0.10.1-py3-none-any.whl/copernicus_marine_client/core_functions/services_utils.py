import logging
from dataclasses import dataclass
from enum import Enum
from itertools import chain
from typing import List, Literal, Optional, Tuple

import xarray

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    CopernicusMarineCatalogue,
    CopernicusMarineDatasetServiceType,
    CopernicusMarineService,
    CopernicusMarineVersionPart,
    get_dataset_and_suffix_path_from_url,
    get_dataset_and_version_part_from_id,
)
from copernicus_marine_client.catalogue_parser.request_structure import (
    DatasetTimeAndGeographicalSubset,
)
from copernicus_marine_client.core_functions.utils import (
    construct_query_params_for_marine_data_store_monitoring,
    next_or_raise_exception,
)
from copernicus_marine_client.download_functions.subset_xarray import (
    get_size_of_coordinate_subset,
)

logger = logging.getLogger("copernicus_marine_root_logger")


class _Command(Enum):
    GET = "get"
    SUBSET = "subset"
    LOAD = "load"


@dataclass(frozen=True)
class Command:
    command_name: _Command
    service_types_by_priority: List[CopernicusMarineDatasetServiceType]

    def service_names(self) -> List[str]:
        return list(
            map(
                lambda service_type: service_type.service_name.value,
                self.service_types_by_priority,
            )
        )

    def service_short_names(self) -> List[str]:
        return list(
            map(
                lambda service_type: service_type.short_name.value,
                self.service_types_by_priority,
            )
        )

    def service_aliases(self) -> List[str]:
        return list(
            chain(
                *map(
                    lambda service_type: service_type.aliases(),
                    self.service_types_by_priority,
                )
            )
        )


class CommandType(Command, Enum):
    SUBSET = _Command.SUBSET, [
        CopernicusMarineDatasetServiceType.GEOSERIES,
        CopernicusMarineDatasetServiceType.TIMESERIES,
        CopernicusMarineDatasetServiceType.OPENDAP,
        CopernicusMarineDatasetServiceType.MOTU,
    ]
    GET = _Command.GET, [
        CopernicusMarineDatasetServiceType.FILES,
        CopernicusMarineDatasetServiceType.FTP,
    ]
    LOAD = _Command.LOAD, [
        CopernicusMarineDatasetServiceType.GEOSERIES,
        CopernicusMarineDatasetServiceType.TIMESERIES,
        CopernicusMarineDatasetServiceType.OPENDAP,
    ]


def assert_service_type_for_command(
    service_type: CopernicusMarineDatasetServiceType, command_type: CommandType
) -> CopernicusMarineDatasetServiceType:
    return next_or_raise_exception(
        (
            service_type
            for service_type in command_type.service_types_by_priority
        ),
        service_type_does_not_exist_for_command(service_type, command_type),
    )


class ServiceDoesNotExistForCommand(Exception):
    def __init__(self, service_name, command_name, available_services):
        super().__init__()
        self.__setattr__(
            "custom_exception_message",
            f"Service {service_name} "
            f"does not exist for command {command_name}. "
            f"Possible service{'s' if len(available_services) > 1 else ''}: "
            f"{available_services}",
        )


def service_type_does_not_exist_for_command(
    service_type: CopernicusMarineDatasetServiceType, command_type: CommandType
) -> ServiceDoesNotExistForCommand:
    return service_does_not_exist_for_command(
        service_type.service_name.value, command_type
    )


def service_does_not_exist_for_command(
    service_name: str, command_type: CommandType
) -> ServiceDoesNotExistForCommand:
    return ServiceDoesNotExistForCommand(
        service_name,
        command_type.command_name.value,
        command_type.service_aliases(),
    )


def _select_forced_service(
    dataset_version_part: CopernicusMarineVersionPart,
    force_service_type: CopernicusMarineDatasetServiceType,
    command_type: CommandType,
) -> CopernicusMarineService:
    logger.info(
        f"You forced selection of service: "
        f"{force_service_type.service_name.value}"
    )
    return next_or_raise_exception(
        (
            service
            for service in dataset_version_part.services
            if service.service_type == force_service_type
        ),
        service_not_available_error(dataset_version_part, command_type),
    )


def _get_best_arco_service_type(
    dataset_subset: DatasetTimeAndGeographicalSubset,
    dataset_url: str,
) -> Literal[
    CopernicusMarineDatasetServiceType.TIMESERIES,
    CopernicusMarineDatasetServiceType.GEOSERIES,
]:
    dataset = xarray.open_zarr(
        dataset_url,
        # Pass custom query parameters for MDS's Monitoring
        # (note that here we don't have 'username', shall we pass it?)
        storage_options={
            "params": construct_query_params_for_marine_data_store_monitoring(),
        },
    )

    latitude_size = get_size_of_coordinate_subset(
        dataset,
        "latitude",
        dataset_subset.minimum_latitude,
        dataset_subset.maximum_latitude,
    )
    longitude_size = get_size_of_coordinate_subset(
        dataset,
        "longitude",
        dataset_subset.minimum_longitude,
        dataset_subset.maximum_longitude,
    )
    time_size = get_size_of_coordinate_subset(
        dataset,
        "time",
        dataset_subset.start_datetime,
        dataset_subset.end_datetime,
    )
    dataset_coordinates = dataset.coords

    geographical_dimensions = (
        dataset_coordinates["latitude"].size
        * dataset_coordinates["longitude"].size
    )
    subset_geographical_dimensions = latitude_size * longitude_size
    temporal_dimensions = dataset_coordinates["time"].size
    subset_temporal_dimensions = time_size

    geographical_coverage = (
        subset_geographical_dimensions / geographical_dimensions
    )
    temporal_coverage = subset_temporal_dimensions / temporal_dimensions

    if geographical_coverage >= temporal_coverage:
        return CopernicusMarineDatasetServiceType.GEOSERIES
    return CopernicusMarineDatasetServiceType.TIMESERIES


def _get_first_available_service_type(
    dataset_version_part: CopernicusMarineVersionPart,
    command_type: CommandType,
    dataset_available_service_types: list[CopernicusMarineDatasetServiceType],
) -> CopernicusMarineDatasetServiceType:
    return next_or_raise_exception(
        (
            service_type
            for service_type in command_type.service_types_by_priority
            if service_type in dataset_available_service_types
        ),
        no_service_available_for_command(command_type),
    )


def _select_service_by_priority(
    dataset_version_part: CopernicusMarineVersionPart,
    command_type: CommandType,
    dataset_subset: Optional[DatasetTimeAndGeographicalSubset],
) -> CopernicusMarineService:
    dataset_available_service_types = [
        service.service_type for service in dataset_version_part.services
    ]
    first_available_service_type = _get_first_available_service_type(
        dataset_version_part, command_type, dataset_available_service_types
    )
    first_available_service = dataset_version_part.get_service_by_service_type(
        first_available_service_type
    )
    if (
        CopernicusMarineDatasetServiceType.GEOSERIES
        in dataset_available_service_types
        and CopernicusMarineDatasetServiceType.TIMESERIES
        in dataset_available_service_types
        and command_type in [CommandType.SUBSET, CommandType.LOAD]
        and dataset_subset is not None
    ):
        best_arco_service_type: CopernicusMarineDatasetServiceType = (
            _get_best_arco_service_type(
                dataset_subset, first_available_service.uri
            )
        )
        return dataset_version_part.get_service_by_service_type(
            best_arco_service_type
        )
    else:
        return first_available_service


def _select_service_from_url(
    dataset_version_part: CopernicusMarineVersionPart,
    dataset_url: str,
    command_type: CommandType,
) -> CopernicusMarineService:
    url_service_type: CopernicusMarineDatasetServiceType = (
        _get_service_type_from_url(dataset_url)
    )
    assert_service_type_for_command(url_service_type, command_type)
    return dataset_version_part.get_service_by_service_type(url_service_type)


def _select_dataset_service(
    dataset_version_part: CopernicusMarineVersionPart,
    dataset_url: Optional[str],
    force_service: Optional[str],
    command_type: CommandType,
    dataset_subset: Optional[DatasetTimeAndGeographicalSubset] = None,
) -> CopernicusMarineService:
    if force_service:
        force_service_type = service_type_from_string(
            force_service, command_type
        )
        return _select_forced_service(
            dataset_version_part, force_service_type, command_type
        )
    if dataset_url:
        return _select_service_from_url(
            dataset_version_part, dataset_url, command_type
        )
    return _select_service_by_priority(
        dataset_version_part, command_type, dataset_subset
    )


def get_dataset_service_and_suffix_path(
    catalogue: CopernicusMarineCatalogue,
    dataset_id: Optional[str],
    dataset_url: Optional[str],
    force_dataset_version_label: Optional[str],
    force_service_type: Optional[str],
    command_type: CommandType,
    dataset_subset: Optional[DatasetTimeAndGeographicalSubset] = None,
) -> Tuple[CopernicusMarineService, str, Optional[str]]:
    if dataset_id is None and dataset_url is None:
        syntax_error = SyntaxError(
            "Must specify at least one of "
            "'dataset_url' or 'dataset_id' options"
        )
        raise syntax_error
    if dataset_id is not None and dataset_url is not None:
        syntax_error = SyntaxError(
            "Must specify only one of 'dataset_url' or 'dataset_id' options"
        )
        raise syntax_error
    if dataset_id:
        dataset, dataset_version_part = get_dataset_and_version_part_from_id(
            catalogue=catalogue,
            dataset_id=dataset_id,
            force_dataset_version_label=force_dataset_version_label,
        )
        return (
            _select_dataset_service(
                dataset_version_part,
                None,
                force_service_type,
                command_type,
                dataset_subset,
            ),
            dataset_id,
            None,
        )
    if dataset_url:
        dataset, suffix_path = get_dataset_and_suffix_path_from_url(
            catalogue=catalogue,
            dataset_url=dataset_url,
        )
        dataset, dataset_version_part = get_dataset_and_version_part_from_id(
            catalogue=catalogue,
            dataset_id=dataset.dataset_id,
            force_dataset_version_label=force_dataset_version_label,
        )
        return (
            _select_dataset_service(
                dataset_version_part,
                dataset_url,
                force_service_type,
                command_type,
            ),
            dataset.dataset_id,
            suffix_path,
        )
    raise NotPossibleError()


class NotPossibleError(Exception):
    ...


def _get_service_type_from_url(
    dataset_url,
) -> CopernicusMarineDatasetServiceType:
    if dataset_url.startswith("ftp://"):
        service_type = CopernicusMarineDatasetServiceType.FTP
    elif "/motu-web/Motu" in dataset_url:
        service_type = CopernicusMarineDatasetServiceType.MOTU
    elif "/thredds/dodsC/" in dataset_url:
        service_type = CopernicusMarineDatasetServiceType.OPENDAP
    elif "/mdl-arco-time" in dataset_url:
        service_type = CopernicusMarineDatasetServiceType.TIMESERIES
    elif "/mdl-arco-geo" in dataset_url:
        service_type = CopernicusMarineDatasetServiceType.GEOSERIES
    elif "/mdl-native" in dataset_url:
        service_type = CopernicusMarineDatasetServiceType.FILES
    else:
        exception = ValueError(f"No service matching url: {dataset_url}")
        raise exception
    return service_type


class ServiceNotAvailable(Exception):
    ...


def service_not_available_error(
    dataset_version_part: CopernicusMarineVersionPart,
    command_type: CommandType,
) -> ServiceNotAvailable:
    dataset_available_service_types = [
        service.service_type.short_name.value
        for service in dataset_version_part.services
        if service.service_type in command_type.service_types_by_priority
    ]
    return ServiceNotAvailable(
        f"Available services for dataset: "
        f"{dataset_available_service_types}"
    )


class NoServiceAvailable(Exception):
    ...


def no_service_available_for_command(
    command_type: CommandType,
) -> NoServiceAvailable:
    return NoServiceAvailable(
        f"No service available for dataset "
        f"with command {command_type.command_name.value}"
    )


def service_type_from_string(
    string: str, command_type: CommandType
) -> CopernicusMarineDatasetServiceType:
    return next_or_raise_exception(
        (
            service_type
            for service_type in command_type.service_types_by_priority
            if string in service_type.aliases()
        ),
        service_does_not_exist_for_command(string, command_type),
    )
