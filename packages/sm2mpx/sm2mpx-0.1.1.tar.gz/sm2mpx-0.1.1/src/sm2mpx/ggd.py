"""
module:: sm2mpx.ggd
:platform: Any
:synopsis: ggd format file object
moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
license:: GPL v3

::

    The file format is:
    *****************************
    HEADER
    *****************************
    PAYLOAD / obscured graphics file
    *****************************

    The header format is:

    *****************************
    UINT32LE @ 0x0
    FILE_SIGNATURE
    *****************************
    UINT16LE @ 0x4
    GRAPHICS WIDTH
    *****************************
    UINT16LE @ 0x8
    GRAPHICS HEIGHT
    *****************************

    the payload format is:
    *****************************
    depending on signature,
    typically
    lzss compressed
    which is obscured by XOR-ring
    with 8 byte key
    Standard Key b"M981113M"
    *****************************

"""
import logging
import traceback
from enum import IntEnum
from io import BytesIO
from pathlib import Path
from typing import Tuple

from PIL import Image

LOGGER = logging.getLogger(__name__)


def parse_ggd(filepath: Path,
              output_filepath: Path = Path("debug.png")
              ):
    with filepath.open("rb") as src:
        color_mode = bytes(x ^ 0xFF for x in src.read(4)).decode()
        print("color mode {0}".format(color_mode))

        # TRUE, FULL = 24 bit per pixel
        # HIGH = 16 bit per pixel
        # 256G = 8 bit per pixel
        assert color_mode in ["TRUE", "FULL"]
        dimensions = tuple(int.from_bytes(src.read(2), "little") for i in range(2))
        src.seek(8)
        payload = bytearray(src.read())
        print("length of payload {0}".format(len(payload)))

    data = decode_ggd(payload, dimensions)
    # int stride = ((int)info.Width * info.BPP / 8 + 3) & ~3;
    # stride = int(dimensions[0] * 24 / 8 + 3)
    # data.extend(bytes((dimensions[0]*dimensions[1]*3) - len(data)))
    # print(len(data), dimensions[0]*dimensions[1]*3)
    image = Image.frombytes(
        "RGB",
        dimensions,
        data,
        "raw",
        "BGR",
        # stride,
    )
    image.save(output_filepath, format="png", lossless=True)


class GGDCtrlByte(IntEnum):
    RepeatPixelForCount = 0
    RepeatPixelSequenceFrom8bitOffset = 1
    RepeatPixelSequenceFrom16bitOffset = 2
    CopyPixelFrom8BitOffset = 3
    CopyPixelFrom16BitOffset = 4


def repeat_pixel(buffer: bytearray,
                 pixel_count: int,
                 bytes_per_pixel: int = 3) -> None:
    """
    Procedure that repeats a pixel on a given buffer bytearray
    :param buffer: The bytearray
    :param pixel_count: The number of repeats
    :param bytes_per_pixel: The bytes per pixel, usually 24bit color, 3 bytes
    :return: Nothing. Works on the buffer.
    """
    assert len(buffer) >= bytes_per_pixel
    for index in range(pixel_count):
        buffer.extend(buffer[-bytes_per_pixel:])
    # assumed to be correct


# def repeat_pixel_from_offset(buffer: bytearray,
#                              pixel_count: int,
#                              pixel_offset: int,
#                              bytes_per_pixel: int = 3) -> None:
#     assert len(buffer) >= bytes_per_pixel
#     pixel_bytes = buffer[-bytes_per_pixel*pixel_offset: -bytes_per_pixel*(pixel_offset-1)]
#     for index in range(pixel_count):
#         buffer.extend(pixel_bytes)

def repeat_sequence(buffer: bytearray,
                    pixel_count: int,
                    pixel_offset: int,
                    bytes_per_pixel: int = 3) -> None:
    """
    Procedure that repeats a sequence of pixels on a given buffer bytearray
    :param buffer: The bytearray
    :param pixel_count: The number pixels to copy from offset.
    :param pixel_offset: The offset from the end of the buffer.
    :param bytes_per_pixel: The bytes per pixel, usually 24bit color, 3 bytes
    :return: Nothing. Works on the buffer.
    """
    # assert len(buffer) >= (bytes_per_pixel * pixel_count)

    # if pixel_count > pixel_offset:
    #     print(pixel_count, pixel_offset)
    #     raise ValueError
    buffer.extend(buffer[-bytes_per_pixel * pixel_offset: -(pixel_offset - pixel_count) * bytes_per_pixel])


def copy_pixel_from_offset(buffer: bytearray,
                           pixel_offset: int,
                           bytes_per_pixel: int = 3) -> None:
    """
    Copy a single pixel from some offset position
    :param buffer: The bytearray
    :param pixel_offset: The offset / number of pixels
    :param bytes_per_pixel: The bytes per pixel, usually 24bit color, 3 bytes
    :return: Nothing. Works on the buffer.
    """
    pixel_start_offset = bytes_per_pixel * pixel_offset
    # print(len(buffer), pixel_offset, pixel_start_offset)
    # assert len(buffer) >= pixel_start_offset > 0
    buffer.extend(buffer[-pixel_start_offset: -pixel_start_offset + bytes_per_pixel])


# def copy_pixel_from_start(buffer: bytearray,
#                            pixel_offset: int,
#                            bytes_per_pixel: int = 3) -> None:
#     """
#     Copy a single pixel from some offset position
#     :param buffer: The bytearray
#     :param pixel_offset: The offset / number of pixels
#     :param bytes_per_pixel: The bytes per pixel, usually 24bit color, 3 bytes
#     :return: Nothing. Works on the buffer.
#     """
#     pixel_start_offset = bytes_per_pixel * pixel_offset
#     # print(len(buffer), pixel_offset, pixel_start_offset)
#     # assert len(buffer) >= pixel_start_offset > 0
#     buffer.extend(buffer[pixel_start_offset: pixel_start_offset + bytes_per_pixel])


def copy_pixel_from_input_buffer_at_byte_offset(input_buffer: BytesIO,
                                                output_buffer: bytearray,
                                                position: int,
                                                bytes_per_pixel: int = 3) -> None:
    old_position = input_buffer.tell()
    input_buffer.seek(position)
    output_buffer.extend(input_buffer.read(bytes_per_pixel))
    input_buffer.seek(old_position)


def decode_ggd(data: bytes, dimensions: Tuple[int, int], bytes_per_pixel: int = 3) -> bytes:
    """
    GGD decode / decompression
    Proprietary algo of IKURA
    Implemented for 24 bit only
    :param data: The input data bytes.
    :param dimensions: The dimensions of the picture.
    :return: The output data bytes.
    """
    expected_pixel_count = dimensions[0] * dimensions[1]
    input_buffer = BytesIO(data)
    output_buffer = bytearray()
    # print(data[:0x2B*3].hex())
    ctrl_stats = list()
    previous_line_count = 0
    print_stats = False
    try:
        while input_buffer.tell() < len(data):
            line_count = int(len(output_buffer) / (dimensions[0] * 3))

            if print_stats and (line_count > previous_line_count):
                stats = [ctrl_stats.count(x) for x in GGDCtrlByte]
                stats.append(len(ctrl_stats) - sum(stats))
                print("Line {0} Opcode Stats {1}".format(line_count, stats))
                print("Line Ended with {0} - Line Starts with {1}".format(ctrl_stats[-2], ctrl_stats[-1]))
                ctrl_stats.clear()
                previous_line_count = line_count

            ctrl_byte = int.from_bytes(input_buffer.read(1), "little", signed=False)
            ctrl_stats.append(ctrl_byte)

            if ctrl_byte == GGDCtrlByte.RepeatPixelForCount:
                """
                This has been verified working by checking the WHITE.GGD / BLACK.GGD single color pictures
                Pattern
                - Read Single Pixel Code 05 FF FF FF <-- BLACK Pixel 24bit
                - Repeat Last Written Pixel 00 FF <-- 255 Times, reoccurring command until picture is full
                """
                assert input_buffer.tell() <= (len(data) - 1)
                number_of_pixels = int.from_bytes(input_buffer.read(1), "little", signed=False)
                repeat_pixel(buffer=output_buffer,
                             pixel_count=number_of_pixels)

            elif ctrl_byte == GGDCtrlByte.RepeatPixelSequenceFrom8bitOffset:
                assert input_buffer.tell() <= (len(data) - 2)
                number_of_pixels = int.from_bytes(input_buffer.read(1), "little", signed=False)
                offset = int.from_bytes(input_buffer.read(1), "little") * bytes_per_pixel
                # repeat_pixel_from_offset(buffer=output_buffer,
                #                          pixel_count=number_of_pixels,
                #                          pixel_offset=offset)
                repeat_sequence(buffer=output_buffer,
                                pixel_count=number_of_pixels,
                                pixel_offset=offset)

            elif ctrl_byte == GGDCtrlByte.RepeatPixelSequenceFrom16bitOffset:  # NAME may be wrong
                assert input_buffer.tell() <= (len(data) - 3)
                number_of_pixels = int.from_bytes(input_buffer.read(1), "little", signed=False)
                offset = int.from_bytes(input_buffer.read(2), "little") * bytes_per_pixel
                # repeat_pixel_from_offset(buffer=output_buffer,
                #                          pixel_count=number_of_pixels,
                #                          pixel_offset=offset)
                repeat_sequence(buffer=output_buffer,
                                pixel_count=number_of_pixels,
                                pixel_offset=offset)

            elif ctrl_byte == GGDCtrlByte.CopyPixelFrom8BitOffset:
                # copy a pixel from somewhere in the output buffer
                # if a pixel is already part of the palette used
                assert input_buffer.tell() <= (len(data) - 1)
                print("Ctrl 3 at pixel {0}".format(len(output_buffer) / 3))
                pixel_offset = int.from_bytes(input_buffer.read(1), "little", signed=False)
                copy_pixel_from_offset(buffer=output_buffer,
                                       pixel_offset=pixel_offset)

            elif ctrl_byte == GGDCtrlByte.CopyPixelFrom16BitOffset:
                # copy a pixel from somewhere in the output buffer
                # if a pixel is already part of the palette used
                assert input_buffer.tell() <= (len(data) - 2)

                pixel_offset = int.from_bytes(input_buffer.read(2), "little", signed=False)
                copy_pixel_from_offset(buffer=output_buffer,
                                       pixel_offset=pixel_offset)
            else:
                # direct copy from input to output
                # used if pixels were not already part of the palette used, e.g. not yet in output buffer
                # likely correct - do not change!
                number_of_pixels = ctrl_byte - 4
                pixel_sequence = input_buffer.read(bytes_per_pixel * number_of_pixels)
                output_buffer.extend(pixel_sequence)
    except AssertionError:
        current_position = input_buffer.tell()
        print(data[current_position - 20:current_position].hex(), data[current_position:current_position + 20].hex())
        print(traceback.format_exc())

    # assert input_buffer.tell() == len(data)
    if len(output_buffer) < expected_pixel_count * 3:
        print("BUG - need to extend output {0} --> {1} missing {2} pixels".format(len(output_buffer),
                                                                                  expected_pixel_count * 3,
                                                                                  (expected_pixel_count - len(
                                                                                      output_buffer) / 3)
                                                                                  ))
        lfill = False
        # lfill = True
        if lfill:
            incomplete = bytearray()
            incomplete.extend(bytes(expected_pixel_count * 3 - len(output_buffer)))
            incomplete.extend(output_buffer)
            output_buffer = incomplete
        else:
            output_buffer.extend(bytes(expected_pixel_count * 3 - len(output_buffer)))

    return bytes(output_buffer)


# function Decode_GGD;
# var TmpPosition, i : longword;
#     ctrlbyte : byte;
#     buf : array[0..7] of byte;
# begin
#   while iStream.Position < iStream.Size do begin
#    iStream.Read(ctrlbyte,1);
#    case ctrlbyte of
#    0 : begin
#         iStream.Read(buf[0],1);
#         oStream.Position := oStream.Position - 3;
#         oStream.Read(buf[1],3);
#         for i:= 1 to buf[0] do begin
#          oStream.Write(buf[1],3);
#         end;
#        end;
#    1 : begin
#         iStream.Read(buf[0],2);
#         TmpPosition := oStream.Position - buf[1]*3;
#         for i:= 1 to buf[0] do begin
#          oStream.Position := TmpPosition;
#          oStream.Read(buf[2],3);
#          oStream.Position := oStream.Size;
#          oStream.Write(buf[2],3);
#          Inc(TmpPosition,3);
#         end;
#        end;
#    2 : begin
#         iStream.Read(buf[0],3);
#         TmpPosition := oStream.Position - ((Word(buf[2]) shl 8) or buf[1])*3;
#         for i:= 1 to buf[0] do begin
#          oStream.Position := TmpPosition;
#          oStream.Read(buf[3],3);
#          oStream.Position := oStream.Size;
#          oStream.Write(buf[3],3);
#          Inc(TmpPosition,3);
#         end;
#        end;
#    3 : begin
#         iStream.Read(buf[0],1);
#         oStream.Position := oStream.Position - buf[0]*3;
#         oStream.Read(buf[1],3);
#         oStream.Position := oStream.Size;
#         oStream.Write(buf[1],3);
#        end;
#    4 : begin
#         iStream.Read(buf[0],2);
#         oStream.Position := oStream.Position - ((Word(buf[1]) shl 8) or buf[0])*3;
#         oStream.Read(buf[2],3);
#         oStream.Position := oStream.Size;
#         oStream.Write(buf[2],3);
#        end;
#   else begin
#         for i:= 0 to ctrlbyte-5 do begin
#          iStream.Read(buf[0],3);
#          oStream.Write(buf[0],3);
#         end;
#        end;
#   end;
#  end;
# end;


# byte[] DecodeStream (Stream input, int pixel_count)
#         {
#             byte[] output = new byte[pixel_count];
#             for (int out_pos = 0; out_pos < output.Length; )
#             {
#                 int opcode = input.ReadByte();
#                 if (-1 == opcode)
#                     break;
#                 int count, src_offset;
#                 int remaining = output.Length - out_pos;
#                 switch (opcode)
#                 {
#                 case 0:
#                     count = Math.Min (3 * input.ReadByte(), remaining);
#                     src_offset = out_pos - 3;
#                     if (count < 0 || src_offset < 0)
#                         return null;
#                     Binary.CopyOverlapped (output, src_offset, out_pos, count);
#                     break;
#                 case 1:
#                     count = Math.Min (3 * input.ReadByte(), remaining);
#                     src_offset = out_pos - 3 * input.ReadByte();
#                     if (count < 0 || src_offset < 0 || src_offset == out_pos)
#                         return null;
#                     Binary.CopyOverlapped (output, src_offset, out_pos, count);
#                     break;
#                 case 2:
#                     {
#                         count = Math.Min (3 * input.ReadByte(), remaining);
#                         int off_lo = input.ReadByte();
#                         int off_hi = input.ReadByte();
#                         src_offset = out_pos - 3 * (off_hi << 8 | off_lo);
#                         if (count < 0 || src_offset < 0 || src_offset == out_pos)
#                             return null;
#                         Binary.CopyOverlapped (output, src_offset, out_pos, count);
#                         break;
#                     }
#                 case 3:
#                     count = Math.Min (3, remaining);
#                     src_offset = out_pos - 3 * input.ReadByte();
#                     if (src_offset < 0 || src_offset == out_pos)
#                         return null;
#                     Buffer.BlockCopy (output, src_offset, output, out_pos, count);
#                     break;
#                 case 4:
#                     {
#                         count = Math.Min (3, remaining);
#                         int off_lo = input.ReadByte();
#                         int off_hi = input.ReadByte();
#                         src_offset = out_pos - 3 * (off_hi << 8 | off_lo);
#                         if (src_offset < 0 || src_offset == out_pos)
#                             return null;
#                         Buffer.BlockCopy (output, src_offset, output, out_pos, count);
#                         break;
#                     }
#                 default:
#                     count = Math.Min (3*(opcode - 4), remaining);
#                     input.Read (output, out_pos, count);
#                     break;
#                 }
#                 out_pos += count;
#             }
#             return output;
#         }

#         /// <summary>
#         /// Copy potentially overlapping sequence of <paramref name="count"/> bytes in array
#         /// <paramref name="data"/> from <paramref name="src"/> to <paramref name="dst"/>.
#         /// If destination offset resides within source region then sequence will repeat itself.  Widely used
#         /// in various compression techniques.
#         /// </summary>
#         public static void CopyOverlapped (byte[] data, int src, int dst, int count)
#         {
#             if (dst > src)
#             {
#                 while (count > 0)
#                 {
#                     int preceding = System.Math.Min (dst - src, count);
#                     System.Buffer.BlockCopy (data, src, data, dst, preceding);
#                     dst += preceding;
#                     count -= preceding;
#                 }
#             }
#             else
#             {
#                 System.Buffer.BlockCopy (data, src, data, dst, count);
#             }
#         }

if __name__ == "__main__":
    parse_ggd(Path(r"GGD/BG41DS.GGD"))  # ROOM with multiplication in front

    # parse_ggd(Path(r"GGD/BLACK.GGD")) # full black
    # parse_ggd(Path(r"GGD/WHITE.GGD"))

    # parse_ggd(Path(r"GGD/C39.GGD"))  # Wives club SM scene

    # parse_ggd(Path(r"GGD/BACK.GGD"))

    # parse_ggd(Path(r"GGD/YU06.GGD"))  # many multiplication on top

    # parse_ggd(Path(r"GGD/SEL_SVL.GGD")) # 256G

    # parse_ggd(Path(r"GGD/T_BG01.GGD")) # Wives club main menu

    # for ggd in Path("GGD").glob("BG*.GGD"):
    #     print(ggd.name)
    #     parse_ggd(filepath=ggd, output_filepath=Path("{0}.png".format(str(ggd)[:-4])))
