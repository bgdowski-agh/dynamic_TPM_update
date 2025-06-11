# dynamic_TPM_update
Source codes and results of tests covered in "Enhancing Security of Error Correction in Quantum Key Distribution Using Tree Parity Machine Update Rule Randomization" article

# How to run
Prerequisites:
- python3
- numpy
1. Download all files from [source_codes](./source_codes) folder
2. Set the parameters in [paramsK.py](./source_codes/paramsK.py), [paramsN.py](./source_codes/paramsN.py) or other file with the same format as one of the mentioned.
3. Set correct parameters file in the beginning of [test.py](./source_codes/test.py) (currently: `from paramsK import params` - replace `paramsK` with selected file name)
4. Run the program in command line with following command: `python3 test.py <number of iteration per parameters set>`

[Original code by Fariz Rahman](https://github.com/farizrahman4u/neuralkey)
