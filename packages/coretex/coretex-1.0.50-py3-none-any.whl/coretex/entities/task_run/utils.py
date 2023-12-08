#     Copyright (C) 2023  Coretex LLC

#     This file is part of Coretex.ai

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Type, Any, Optional, List
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import logging

import git

from ..dataset import *
from ..project import ProjectType
from ... import folder_manager
from ...networking import FileData


def getDatasetType(type_: ProjectType, isLocal: bool) -> Type[Dataset]:
    if type_ == ProjectType.other:
        if isLocal:
            return LocalCustomDataset

        return CustomDataset

    if type_ == ProjectType.imageSegmentation:
        if isLocal:
            return LocalImageSegmentationDataset

        return ImageSegmentationDataset

    if type_ == ProjectType.computerVision:
        if isLocal:
            return LocalComputerVisionDataset

        return ComputerVisionDataset

    logging.getLogger("coretexpylib").debug(f">> [Coretex] ProjectType ({type_}) does not have a dataset type using CustomDataset")

    # Returning CustomDataset in case the type_ doesn't have it's dataset type
    if isLocal:
        return LocalCustomDataset

    return CustomDataset


def fetchDataset(datasetType: Type[Dataset], value: Any) -> Optional[Dataset]:
    if issubclass(datasetType, LocalDataset):
        return datasetType(value)  # type: ignore

    if issubclass(datasetType, NetworkDataset):
        return datasetType.fetchById(value)

    return None


def getSnapshotFiles(dirPath: Path, ignoredFiles: List[str]) -> List[Path]:
    snapshotFiles: List[Path] = []

    if dirPath.joinpath(".coretexignore").exists():
        return []

    for path in dirPath.iterdir():
        if path.is_dir():
            snapshotFiles.extend(getSnapshotFiles(path, ignoredFiles))
        elif str(path) not in ignoredFiles:
            snapshotFiles.append(path)

    return snapshotFiles


def getDefaultEntryPoint() -> Optional[str]:
    for defaultEntryPoint in [Path(".", "main.py"), Path(".", "main.r"), Path(".", "main.R")]:
        if defaultEntryPoint.exists():
            return defaultEntryPoint.name

    return None


def createSnapshot() -> Path:
    entryPoint = getDefaultEntryPoint()
    if entryPoint is None or not Path(".", entryPoint).exists():
        raise FileNotFoundError(">> [Coretex] Entry point file not found")

    snapshotPath = folder_manager.temp / "snapshot.zip"
    with ZipFile(snapshotPath, "w", ZIP_DEFLATED) as snapshotArchive:
        repo = git.Repo(Path.cwd(), search_parent_directories = True)
        ignoredFiles = repo.ignored(*list(Path.cwd().rglob("*")))

        if not Path(entryPoint).exists() or not Path("requirements.txt").exists():
            raise FileNotFoundError(f">> [Coretex] Required files \"{entryPoint}\" and \"requirements.txt\"")

        for path in getSnapshotFiles(Path.cwd(), ignoredFiles):
            snapshotArchive.write(path)

    return snapshotPath
