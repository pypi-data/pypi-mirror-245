# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import annotations

import collections
import functools
import itertools
import pathlib
import re
import typing

from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from typing import Final, Generic, Literal, Optional, Protocol, TypeVar, Union, overload

from no_vtf._typing import mypyc_attr
from no_vtf.image import Image, ImageDataTypes, ImageDynamicRange, ImageWithRawData
from no_vtf.image.channel_separator import ChannelSeparator
from no_vtf.image.io import IO
from no_vtf.image.io.image import ImageIO
from no_vtf.image.io.raw import RawIO
from no_vtf.image.modifier import ImageModifier
from no_vtf.image.modifier.hdr_to_ldr_modifier import HdrToLdrModifier
from no_vtf.texture.decoder import TextureDecoder
from no_vtf.texture.extractor import TextureExtractor
from no_vtf.texture.filter import TextureFilter
from no_vtf.texture.namer import TextureNamer

Quantity = Literal["single", "multi"]

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_T2_co = TypeVar("_T2_co", covariant=True)


@mypyc_attr(allow_interpreted_subclasses=True)
class Receipt:
    def __init__(
        self,
        *,
        io_ready: bool = False,
        io_done: bool = False,
        output_written: Mapping[pathlib.Path, int] = {},
    ) -> None:
        self.io_ready: Final = io_ready
        self.io_done: Final = io_done
        self.output_written: Final = output_written


@mypyc_attr(allow_interpreted_subclasses=True)
class Pipeline(Generic[_T]):
    FORMAT_SKIP: Final[Literal["skip"]] = "skip"

    @classmethod
    def initialize(cls, formats: Optional[Sequence[str]] = None) -> None:
        if formats:
            formats = list(filter(lambda format: format not in (cls.FORMAT_SKIP), formats))

        ImageIO.initialize(formats)

    def __init__(
        self,
        *,
        input_extension_pattern: Optional[re.Pattern[str]] = None,
        ldr_format: str,
        hdr_format: str,
        animate: bool = False,
        fps: Optional[int] = None,
        separate_channels: bool = False,
        hdr_to_ldr: bool = False,
        compress: Optional[bool] = None,
        raw: bool = False,
        write: Optional[bool] = None,
        readback: bool = False,
        extractor: TextureExtractor[_T],
        filter: Optional[TextureFilter[_T]],  # noqa: A002
        decoder: TextureDecoder[_T, ImageDataTypes],
        namer: TextureNamer[_T],
    ) -> None:
        self._input_extension_pattern: Final = input_extension_pattern

        self._animate: Final = animate
        self._separate_channels: Final = separate_channels

        self._raw: Final = raw

        self._write: Final = write
        self._readback: Final = readback

        self._compress: Final = compress
        self._fps: Final = fps

        self._extractor: Final = extractor
        self._filter: Final = filter
        self._decoder: Final = decoder
        self._namer: Final = namer

        ldr_format_split = ldr_format.split("|")
        hdr_format_split = hdr_format.split("|")

        ldr_format_single: Final = ldr_format_split[0]
        hdr_format_single: Final = hdr_format_split[0]

        ldr_format_multi: Final = (ldr_format_split[1:2] or ldr_format_split[0:1])[0]
        hdr_format_multi: Final = (hdr_format_split[1:2] or hdr_format_split[0:1])[0]

        self.image_io: Final[Mapping[tuple[Quantity, ImageDynamicRange], Optional[ImageIO]]] = {}
        self.image_io["single", "ldr"] = self._create_image_io(ldr_format_single)
        self.image_io["single", "hdr"] = self._create_image_io(hdr_format_single)
        self.image_io["multi", "ldr"] = self._create_image_io(ldr_format_multi)
        self.image_io["multi", "hdr"] = self._create_image_io(hdr_format_multi)

        self._raw_io: Final = RawIO()

        modifiers: list[ImageModifier[ImageDataTypes]] = []
        if hdr_to_ldr:
            modifiers.append(HdrToLdrModifier())

        self._apply_modifiers: Final = (
            functools.partial(_apply_modifiers, modifiers=modifiers) if modifiers else None
        )

    def _create_image_io(self, output_format: str) -> Optional[ImageIO]:
        if output_format != self.FORMAT_SKIP:
            return ImageIO(format=output_format, compress=self._compress, fps=self._fps)

        return None

    @overload
    def __call__(self, input_file: pathlib.Path, *, output_file: pathlib.Path) -> Receipt:
        ...

    @overload
    def __call__(self, input_file: pathlib.Path, *, output_directory: pathlib.Path) -> Receipt:
        ...

    def __call__(
        self,
        input_file: pathlib.Path,
        *,
        output_file: Optional[pathlib.Path] = None,
        output_directory: Optional[pathlib.Path] = None,
    ) -> Receipt:
        items = self._get_items(input_file)

        do_io: Union[_DoImageIO, _DoIO[object]]
        if not self._raw:
            do_io = self._process_items_image(
                items, output_file=output_file, output_directory=output_directory
            )
        else:
            do_io = self._process_items_raw(
                items, output_file=output_file, output_directory=output_directory
            )

        return Receipt(
            io_ready=do_io.stats.io_ready,
            io_done=do_io.stats.io_done,
            output_written=do_io.stats.output_written,
        )

    def _get_items(
        self, input_file: pathlib.Path
    ) -> Sequence[_PipelineItem[ImageWithRawData[ImageDataTypes]]]:
        textures = self._extractor(input_file)

        if self._filter:
            textures = self._filter(textures)

        items: list[_PipelineItem[ImageWithRawData[ImageDataTypes]]] = []
        for texture in textures:
            image: ImageWithRawData[ImageDataTypes] = self._decoder(texture)

            input_name = input_file.name
            if self._input_extension_pattern:
                input_name = re.sub(self._input_extension_pattern, "", input_name)

            output_stem = self._namer(input_name, texture)

            item = _PipelineItem(sequence=[image], output_stem=output_stem)
            items.append(item)

        return items

    def _process_items_image(
        self,
        items: Sequence[_PipelineItem[Image[ImageDataTypes]]],
        *,
        output_file: Optional[pathlib.Path] = None,
        output_directory: Optional[pathlib.Path] = None,
    ) -> _DoImageIO:
        do_io = self._do_image_io(output_file=output_file, output_directory=output_directory)
        steps = [
            self._apply_modifiers,
            _separate_channels if self._separate_channels else None,
            _group_by_output_stem if self._animate else None,
            do_io,
        ]

        for step in steps:
            if step:
                items = step(items)

        return do_io

    def _process_items_raw(
        self,
        items: Sequence[_PipelineItem[ImageWithRawData[ImageDataTypes]]],
        *,
        output_file: Optional[pathlib.Path] = None,
        output_directory: Optional[pathlib.Path] = None,
    ) -> _DoIO[ImageWithRawData[ImageDataTypes]]:
        do_io = self._do_raw_io(output_file=output_file, output_directory=output_directory)
        steps = [
            _group_by_output_stem if self._animate else None,
            do_io,
        ]

        for step in steps:
            if step:
                items = step(items)

        return do_io

    def _do_image_io(
        self, *, output_file: Optional[pathlib.Path], output_directory: Optional[pathlib.Path]
    ) -> _DoImageIO:
        return _DoImageIO(
            animate=self._animate,
            image_io=self.image_io,
            output_file=output_file,
            output_directory=output_directory,
            write=self._write,
            readback=self._readback,
        )

    def _do_raw_io(
        self, *, output_file: Optional[pathlib.Path], output_directory: Optional[pathlib.Path]
    ) -> _DoIO[ImageWithRawData[ImageDataTypes]]:
        return _DoIO(
            io=self._raw_io,
            extension="raw",
            output_file=output_file,
            output_directory=output_directory,
            write=self._write,
            readback=self._readback,
        )


@mypyc_attr(allow_interpreted_subclasses=True)
class _PipelineItem(Generic[_T_co]):
    def __init__(self, *, sequence: Sequence[_T_co], output_stem: str) -> None:
        self.sequence: Final = sequence
        self.output_stem: Final = output_stem

    def map(self, func: Callable[[_T_co], _T2_co]) -> _PipelineItem[_T2_co]:
        new_sequence = list(map(func, self.sequence))
        return _PipelineItem(sequence=new_sequence, output_stem=self.output_stem)

    @staticmethod
    def map_items(
        func: Callable[[_T_co], _T2_co], items: Sequence[_PipelineItem[_T_co]]
    ) -> Sequence[_PipelineItem[_T2_co]]:
        return [item.map(func) for item in items]


class _PipelineStep(Protocol[_T]):
    def __call__(self, items: Sequence[_PipelineItem[_T]]) -> Sequence[_PipelineItem[_T]]:
        ...


def _apply_modifiers(
    items: Sequence[_PipelineItem[Image[ImageDataTypes]]],
    *,
    modifiers: Sequence[ImageModifier[ImageDataTypes]],
) -> Sequence[_PipelineItem[Image[ImageDataTypes]]]:
    new_items: list[_PipelineItem[Image[ImageDataTypes]]] = []
    for item in items:
        new_sequence: list[Image[ImageDataTypes]] = []
        for image in item.sequence:
            for modifier in modifiers:
                image = modifier(image)

            new_sequence.append(image)

        new_item = _PipelineItem(sequence=new_sequence, output_stem=item.output_stem)
        new_items.append(new_item)

    return new_items


def _separate_channels(
    items: Sequence[_PipelineItem[Image[ImageDataTypes]]],
    *,
    channel_separator: ChannelSeparator = ChannelSeparator(),
) -> Sequence[_PipelineItem[Image[ImageDataTypes]]]:
    new_items: list[_PipelineItem[Image[ImageDataTypes]]] = []
    for item in items:
        new_sequence_by_channels: defaultdict[str, list[Image[ImageDataTypes]]] = defaultdict(list)
        for image in item.sequence:
            for image_seperated in channel_separator(image):
                new_sequence_by_channels[image_seperated.channels].append(image_seperated)

        for channels, new_sequence in new_sequence_by_channels.items():
            new_output_stem = f"{item.output_stem}_{channels}"
            new_item = _PipelineItem(sequence=new_sequence, output_stem=new_output_stem)
            new_items.append(new_item)

    return new_items


def _group_by_output_stem(items: Sequence[_PipelineItem[_T]]) -> Sequence[_PipelineItem[_T]]:
    item_by_output_stem: dict[str, _PipelineItem[_T]] = {}
    for item in items:
        output_stem = item.output_stem
        if output_stem not in item_by_output_stem:
            item_by_output_stem[output_stem] = item
        else:
            old_item = item_by_output_stem[output_stem]
            new_sequence = list(old_item.sequence) + list(item.sequence)
            new_item = _PipelineItem(sequence=new_sequence, output_stem=output_stem)
            item_by_output_stem[output_stem] = new_item

    return list(item_by_output_stem.values())


@mypyc_attr(allow_interpreted_subclasses=True)
class _DoImageIO(_PipelineStep[Image[ImageDataTypes]]):
    def __init__(
        self,
        *,
        animate: bool,
        image_io: Mapping[tuple[Quantity, ImageDynamicRange], Optional[ImageIO]],
        output_file: Optional[pathlib.Path],
        output_directory: Optional[pathlib.Path],
        write: Optional[bool],
        readback: bool,
        stats: Optional[_Stats] = None,
    ):
        self.stats: Final = stats or _Stats()

        self._do_io: Final[
            Mapping[tuple[Quantity, ImageDynamicRange], _DoIO[Image[ImageDataTypes]]]
        ] = {}
        for quantity, dynamic_range in itertools.product(
            typing.get_args(Quantity), typing.get_args(ImageDynamicRange)
        ):
            if image_io_instance := image_io[quantity, dynamic_range]:
                self._do_io[quantity, dynamic_range] = _DoIO(
                    io=image_io_instance,
                    extension=image_io_instance.format,
                    output_file=output_file,
                    output_directory=output_directory,
                    write=write,
                    readback=readback,
                    stats=self.stats,
                )

    def __call__(
        self, items: Sequence[_PipelineItem[Image[ImageDataTypes]]]
    ) -> Sequence[_PipelineItem[Image[ImageDataTypes]]]:
        for item in items:
            if not item.sequence:
                continue

            quantity: Quantity = "multi" if len(item.sequence) > 1 else "single"
            dynamic_range = item.sequence[0].dynamic_range

            for image in item.sequence:
                assert (
                    image.dynamic_range == dynamic_range
                ), "Dynamic range must be the same for all images"

            if do_io_instance := self._do_io.get((quantity, dynamic_range)):
                do_io_instance([item])

        return items


@mypyc_attr(allow_interpreted_subclasses=True)
class _DoIO(Generic[_T_co]):
    def __init__(
        self,
        *,
        io: IO[_T_co],
        extension: str,
        output_file: Optional[pathlib.Path],
        output_directory: Optional[pathlib.Path],
        write: Optional[bool],
        readback: bool,
        stats: Optional[_Stats] = None,
    ) -> None:
        self.io: Final = io
        self.extension: Final = extension
        self.output_file: Final = output_file
        self.output_directory: Final = output_directory
        self.write: Final = write
        self.readback: Final = readback
        self.stats: Final = stats or _Stats()

    def __call__(self, items: Sequence[_PipelineItem[_T_co]]) -> Sequence[_PipelineItem[_T_co]]:
        for item in items:
            item_output_path = self.output_file
            if not item_output_path:
                assert self.output_directory is not None, "output path must be set"
                output_name = f"{item.output_stem}.{self.extension}"
                item_output_path = self.output_directory / output_name

            self.stats.io_ready = True

            if self.write is not False:
                if (
                    self.write is True
                    or not item_output_path.is_file()
                    or self.stats.output_written[item_output_path]
                ):
                    item_output_path.parent.mkdir(parents=True, exist_ok=True)
                    self.io.write_sequence(item_output_path, item.sequence)
                    self.stats.io_done = True
                    self.stats.output_written[item_output_path] += 1

            if self.readback:
                self.io.readback_sequence(item_output_path, item.sequence)
                self.stats.io_done = True

        return items


@mypyc_attr(allow_interpreted_subclasses=True)
class _Stats:
    def __init__(self) -> None:
        self.io_ready = False
        self.io_done = False
        self.output_written: collections.Counter[pathlib.Path] = collections.Counter()
