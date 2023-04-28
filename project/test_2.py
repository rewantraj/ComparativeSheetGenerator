from implementation import CSG;

import pandas as pd
import pytest;
from sys import platform
slash = "/";
if (platform == "win32"):
	slash = "\\";
input_path = "input" + slash;
output_path = "output" + slash;

def testcase_1(): # checks correctness of debug error thrown in case files don't match
	input_path = "testcases" + slash + "testcase2" + slash + "input" + slash;
	output_path = "testcases" + slash + "testcase2" + slash + "output" + slash;
	print(input_path);
	print(output_path);
	csg = CSG.CSG(input_dir = input_path, output_dir = output_path);
	with pytest.raises(SystemExit):
		csg.run();
