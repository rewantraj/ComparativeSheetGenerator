# ComparativeSheetGenerator

## Build and Run
* Make sure the terminal is opened in ```project/implementation/``` directory. 

* Place all the input files in the ```input/``` directory.

* Create an ```output/``` directory for output.

* To generate the comparative sheet for the input files, run the following command.
```
python3 CSG.py
```

## Test
* Make sure the terminal is opened in ```project/``` directory. 
* To test the correctness of code, run the following code.
```
pytest
```

## Points to note

<ul>
    <li>All the quotation responses in the input directory, should correspond to the same indentation numbers and metadata, otherwise the software throws an error </li>
    <li>The format of the quotation files remain consistent</li>
    <li>Only 'NA' and blank space are considered as valid null space occupiers</li>
    <li>The expected format of various fields is as follows:
    <ul>
        <li>'List Price' is {currency symbol}{amount}, for example ₹100</li>
        <li>'Conversion Rate' is {equivalent amount in ₹}, for example 100</li>
        <li>'Discount' is {discount expressed as %}, for example 10</li>
        <li>'Total Price' is {total price in ₹}, for example 1000</li>
    </ul>
    </li>
</ul>
