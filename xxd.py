#!/usr/bin/env python

################################################################################
# Imports   <Package Import>
################################################################################
import os
import sys
import subprocess

try:
    import progressbar
except ImportError as e:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "progressbar"])
    import progressbar


################################################################################
# Private global variables and functions
################################################################################

# Number of bytes per line
BYTES_PER_LINE = 12

# Check the version of the python used
PYTHON_VER = sys.version_info > (3,)


def byte_conv(array, path):
    """
    @param array        : contains read file output
    @param path         : contains path of the file
    @return  status     : returns True if conversion is success
                          False if file is empty
             output     : Returns converted string
    """

    # output stores the byte converted lines
    output = []

    # Variable to count the byte length
    byte_length = 0

    # Progress indication bar
    bar = progressbar.ProgressBar(maxval=1, widgets=[progressbar.Bar(
        '=', '[', ']'), ' ', progressbar.Percentage(), '\n'])
    output.append("unsigned char %s[] = {\n" % path)
    print("Length of data bytes : ", len(array))

    # Check file is empty
    if len(array) == 0:
        print("FILE ERROR...! File doesn't contain anything, Please select \
        the valid file..!")
        return False, output

    # Start the progress bar
    bar.start()

    # loop over the data of tflite file
    for byte_index in range(len(array)):
        if PYTHON_VER:
            byte = array[byte_index]
        else:
            byte = ord(array[byte_index])

        byte_length += 1
        if byte_length == BYTES_PER_LINE:
            byte_length = 0
            output.append(' 0x' + '{:02x},\n'.format(byte))
        elif byte_length == 1:
            output.append('  0x' + '{:02x},'.format(byte))
        else:
            output.append(' 0x' + '{:02x},'.format(byte))

        # Update the progress bar
        bar.update(byte_index/len(array))

    output = output[:-1] + list(output[-1].replace(', ', '').replace(',', '').
                                replace('\n', ''))
    output.append("\n")
    output.append("};\n")
    output += "unsigned int %s_len = %d;" % (path, byte_index + 1)
    bar.finish()
    print('Conversion is done, Writing it to a file.')
    return True, ''.join(output)


# Main starts from here
if __name__ == '__main__':
    """
    Function Name       : __main__ 
    Description         : Main function.
    Arguments           : None
    Return Value        : None
    """
    
    if os.path.exists(sys.argv[1]):
        path = sys.argv[1].replace('.', '_')
        if sys.argv[1].split('.')[-1] != 'tflite':
            print("FILE FORMAT ERROR...!, Please select valid tflite file")
        else:
            output = sys.argv[1].replace('.tflite', '.cc')
            with open(sys.argv[1], 'rb') as f:
                file = f.read()
                status, data = byte_conv(file, path)
            if status:
                f = open('%s'%output, 'w+')
                f.writelines(data)
                f.close()
                print('File processing Finished...!')

    else:
        print("FILE NOT FOUND...! Please select valid file")

