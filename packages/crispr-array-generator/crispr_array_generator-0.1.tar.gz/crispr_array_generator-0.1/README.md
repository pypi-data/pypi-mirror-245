# crispr_array_generator
A python package for verifying and generating CRISPR Cas12 Arrays

CRISPR arrays that encode for multiple CRISPR guide (g)RNAs allow for multiplexed gene editing. Cas12 systems are best suited for this multiplexed targeting, since they possess the power to process gRNAs from an RNA transcript with no additional inputs. While this makes CRISPR Cas12 arrays a great tool for research labs to implement multiplexed gene targeting, designing these arrays can be tedious, as each gRNA within the array should be accompanied by separator, repeat, and annealing overhang sequences to optimize processing. With this, it is time-intensive and easy to make mistakes when designing these arrays by hand.

This tool can be used to check existing gRNAs or CRISPR arrays for common errors. It can also be used to identify and choose gRNAs from DNA sequences and auto-process gRNAs into ready-to-order array oligonucleotides, simplifying the array generation process to save the user time and effort.

# Set up
`pip install -U openpyxl ; pip install git+https://github.com/wachern/crispr_array_generator.git ; from crispr_array_generator.crisprarraygenerator import Array`

# Check gRNAs for common errors
gRNAs can be inputted as an array or within an excel file. You may check as many gRNAs at a time as you'd like.

The function will output an excel file "grnacheck.xlsx" with all processed gRNAs and errors if present listed on the first sheet "gRNAcheck." If using google colaboratory, this will show up under the left "Files" tab. You may need to refresh the files in order to see the output file.

### Inputting an excel file
Upload the file to your python environment of choice. For example, if using google colaboratory, you can call:
`from google.colab import files ; uploaded = files.upload()`

Input the name of your excel file (exclusing the ".xlsx") into the check_grna function:
`Array.check_grna('excelfile')`

### Inputting an array
create an array or input it directly into the get_array function:
`grnas = ['grna1', 'grna2', ..., 'graN'] ; Array.check_grna(grnas)`

# Generate array from gRNAs
gRNAs can be inputted as an array or within an excel file. You may add up to nine gRNAs to an array and only one array can be processed at a time. You do not need to check these gRNAs for errors separately, get_array does this for you.

The function will output an excel file "grnacheck.xlsx" with all processed gRNAs and errors if present listed on the first sheet "gRNAcheck." Array oligonucleotides and the full array sequence will be listed on the second sheet "Array." If using google colaboratory, this will show up under the left "Files" tab. You may need to refresh the files in order to see the output file.

### Inputting an excel file
Upload the file to your python environment of choice. For example, if using google colaboratory, you can call:
`from google.colab import files ; uploaded = files.upload()`

Input the name of your excel file (exclusing the ".xlsx") into the check_grna function:
`Array.get_array('excelfile')`

### Inputting an array
create an array or input it directly into the get_array function:
`grnas = ['grna1', 'grna2', ..., 'graN'] ; Array.get_array(grnas)`

# Common errors
- Not all gRNAs showing up in output file? Check that your guides only include nucleotide bases (ATCG or atcg). The program automatically removes non-valid DNA inputs.
- Input file not loading? Check that it is a .xlsx file. This is the only file type currently accepted.

Run into a problem that's not addressed here? Add an issue to the repository or email the author at wachern@uw.edu.
