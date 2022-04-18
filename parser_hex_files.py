import random

import parser_data_hex_line

# Record type hex line
TYPE_DATA = 0
TYPE_END_OF_FILE = 1
TYPE_EXTENDED_SEGMENT_ADDRESS = 2
TYPE_START_SEGMENT_ADDRESS = 3
TYPE_EXTENDED_LINEAR_ADDRESS = 4
TYPE_STARTING_LINEAR_ADDRESS = 5


def processing_file_line_by_line(data_file, reg_hex_file, current_reg=None) -> bool:
    """
    Function hex data processing line by line
    :param data_file: data hex file
    :param reg_hex_file: data hex file
    :param current_reg: current region
    :return: True - successful file processing,
             False - file corrupted
    """
    if isinstance(data_file, str):
        data_file = data_file.split()

    for line_hex in data_file:
        is_good, type_rec, address, data, amount_data = parser_data_hex_line.ProcessingHexLine(line_hex[1:]).parsing()
        if is_good:
            if TYPE_EXTENDED_LINEAR_ADDRESS == type_rec:
                if current_reg:
                    current_reg.current_seg.current_mem.complete()
                current_reg = reg_hex_file.create_new_reg(data)
            elif TYPE_DATA == type_rec:
                current_reg.add_data(address, data, amount_data)
            elif TYPE_STARTING_LINEAR_ADDRESS == type_rec:
                reg_hex_file.create_start_liner_adr_data(data)
            elif TYPE_END_OF_FILE == type_rec:
                if current_reg:
                    current_reg.current_seg.current_mem.complete()
                return True
        else:
            return False


class ParserHex:
    """
    Class processing accepted hex files
    """

    data_hex_list = {}

    def __init__(self):
        self.data_hex_list = {}

    def processing(self, list_name_hex_files: list):
        """
        Function processing of hex files for availability and
        corruption or upon successful opening parsing data
        """
        self.data_hex_list.clear()

        for name_hex_file in list_name_hex_files:
            print('Processing file ' + name_hex_file + '.hex')
            try:
                data_hex_file = open(name_hex_file + '.hex', 'r')
                print('File has been successfully opened for processing.')
                regions_hex_file = parser_data_hex_line.RegionsList()
                if processing_file_line_by_line(data_hex_file, regions_hex_file):
                    self.data_hex_list[name_hex_file] = regions_hex_file
                    print('File has been processed successfully.\n')
                else:
                    print('Further processing of the file is impossible - the file is damaged!')
                data_hex_file.close()
            except FileNotFoundError:
                print('File not found!\n')
                continue

    def save_file(self, name_file: str = 'merge', merge_file: bool = False):
        """
        Написать описание
        """
        hex_file_text = ''
        if name_file in self.data_hex_list.keys():
            hex_file_text = self.data_hex_list[name_file].gen_hex(is_end=True)
        elif merge_file:
            name_file += str(random.randrange(10000))
            for item_name in self.data_hex_list.keys():
                flag_end = False
                if item_name == list(self.data_hex_list)[-1]:
                    flag_end = True
                hex_file_text += self.data_hex_list[item_name].gen_hex(is_end=flag_end)

        hex_file = open(name_file + '.hex', 'w')
        hex_file.write(hex_file_text)
        hex_file.close()

    def merge(self, empty=0xFF):
        """
        Function merge all or part of the hex files data
        :param empty: what data to fill the void with
        :return: True, False
        """
        pass
