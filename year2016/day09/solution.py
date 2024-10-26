"""
--- Day 9: Explosives in Cyberspace ---
Wandering around a secure area, you come across a datalink port to a new part of the network.
After briefly scanning it for interesting files, you find one file in particular that catches your attention.
It's compressed with an experimental format, but fortunately, the documentation for the format is nearby.

The format compresses a sequence of characters. Whitespace is ignored.
To indicate that some sequence should be repeated, a marker is added to the file, like `(10x2)`.
To decompress this marker, take the subsequent 10 characters and repeat them 2 times.
Then, continue reading the file after the repeated data.
The marker itself is not included in the decompressed output.

If parentheses or other characters appear within the data referenced by a marker, that's okay
- treat it like normal data, not a marker, and then resume looking for markers after the decompressed section.

For example:
- `ADVENT` contains no markers and decompresses to itself with no changes, resulting in a decompressed length of 6.
- `A(1x5)BC` repeats only the `B` a total of 5 times, becoming `ABBBBBC` for a decompressed length of 7.
- `(3x3)XYZ` becomes `XYZXYZXYZ` for a decompressed length of 9.
- `A(2x2)BCD(2x2)EFG` doubles the `BC` and `EF`, becoming `ABCBCDEFEFG` for a decompressed length of 11.
- `(6x1)(1x3)A` simply becomes `(1x3)A` - the `(1x3)` looks like a marker, but because it's within a data section of another marker,
    it is not treated any differently from the `A` that comes after it. It has a decompressed length of 6.
- `X(8x2)(3x3)ABCY` becomes `X(3x3)ABC(3x3)ABCY` (for a decompressed length of 18),
    because the decompressed data from the `(8x2)` marker (the `(3x3)ABC`) is skipped and not processed further.

What is the decompressed length of the file (your puzzle input)? Don't count whitespace.

--- Part Two ---
Apparently, the file actually uses version two of the format.

In version two, the only difference is that markers within decompressed data are decompressed.
This, the documentation explains, provides much more substantial compression capabilities,
allowing many-gigabyte files to be stored in only a few kilobytes.

For example:
- `(3x3)XYZ` still becomes `XYZXYZXYZ`, as the decompressed section contains no markers.
- `X(8x2)(3x3)ABCY` becomes `XABCABCABCABCABCABCY`, because the decompressed data from the `(8x2)` marker is then further decompressed, thus triggering the `(3x3)` marker twice for a total of six `ABC` sequences.
- `(27x12)(20x12)(13x14)(7x10)(1x12)A` decompresses into a string of `A` repeated 241920 times.
- `(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN` becomes 445 characters long.

Unfortunately, the computer you brought probably doesn't have enough memory to actually decompress the file;
you'll have to come up with another way to get its decompressed length.

What is the decompressed length of the file using this improved format?

--- Notes ---

https://en.wikipedia.org/wiki/Zip_bomb

"""

from pathlib import Path
from dataclasses import dataclass
import re


@dataclass
class Marker:
    start: int
    end: int
    n_chars: int
    n_reps: int

    def __post_init__(self):
        self.length = self.end - self.start


def get_markers(compressed_sequence: str) -> list[Marker]:
    markers = []
    marker_pattern = re.compile(r"\((\d+)x(\d+)\)")

    match = marker_pattern.search(compressed_sequence)
    while match is not None:
        marker = Marker(
            start=match.start(),
            end=match.end(),
            n_chars=int(match.group(1)),
            n_reps=int(match.group(2)),
        )
        match = marker_pattern.search(compressed_sequence, marker.end + marker.n_chars)
        markers.append(marker)

    return markers


def get_length_decompressed_marker(marker: Marker) -> int:
    # Compute the number of characters that are substituted for the marker.
    return marker.n_chars * marker.n_reps - marker.n_chars - marker.length


def get_length_decompressed_sequence_part1(compressed_sequence: str) -> int:
    markers = get_markers(compressed_sequence)

    return sum(get_length_decompressed_marker(marker) for marker in markers) + len(
        compressed_sequence
    )


def get_length_decompressed_sequence_part2(compressed_sequence: str) -> int:
    length_decompressed_sequence = len(compressed_sequence)

    for marker in get_markers(compressed_sequence):
        length_decompressed_sequence += (
            marker.n_reps
            * get_length_decompressed_sequence_part2(
                compressed_sequence[marker.end : marker.end + marker.n_chars]
            )
        )
        length_decompressed_sequence -= marker.n_chars + marker.length

    return length_decompressed_sequence


def solve_part1(input_path: str):
    compressed_sequence = Path(input_path).read_text()
    length_decompressed_sequence = get_length_decompressed_sequence_part1(
        compressed_sequence
    )
    print(
        f"Part 1:\nThe length of the decompressed sequence is {length_decompressed_sequence}\n"
    )


def solve_part2(input_path: str):
    compressed_sequence = Path(input_path).read_text()
    length_decompressed_sequence = get_length_decompressed_sequence_part2(
        compressed_sequence
    )
    print(
        f"Part 2:\nThe length of the decompressed sequence is {length_decompressed_sequence}\n"
    )


if __name__ == "__main__":
    solve_part1(f"{Path(__file__).parent}/input.txt")
    solve_part2(f"{Path(__file__).parent}/input.txt")
