from implementation import CSG;

import pandas as pd
import pytest;
from sys import platform
slash = "/";
if (platform == "win32"):
	slash = "\\";
input_path = "input" + slash;
output_path = "output" + slash;

def testcase_1(): # checks correctness of output incase files match
	input_path = "testcases" + slash + "testcase1" + slash + "input" + slash;
	output_path = "testcases" + slash + "testcase1" + slash + "output" + slash;
	print(input_path);
	print(output_path);
	csg = CSG.CSG(input_dir = input_path, output_dir = output_path);
	csg.run();
	cdf_correct = pd.read_excel(output_path +"comparative_sheet_correct.xlsx");
	cdf = pd.read_excel(output_path + "comparative_sheet.xlsx");
	assert cdf.equals(cdf_correct);
