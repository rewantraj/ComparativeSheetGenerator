# Author: Rewant Raj

import openpyxl
import os
import glob
from sys import platform
import pandas as pd
import numpy as np
import math
from itertools import filterfalse

def get_vendor_name(f):
	vendor_row = pd.read_excel(f, nrows = 1);
	vendor_attr = vendor_row.columns[0];
	vendor = vendor_attr[vendor_attr.index(':')+1:];
	vendor = vendor.strip();
	return vendor;

def update_conversion_rate(df, currency_rate):
	conv_rate_row = np.where(df[df.columns[0]].notna().to_numpy() == False)[0];
	i = conv_rate_row[0];
	while(True):
		currency = df.loc[i][2];
		rate = df.loc[i][3];
		i+=1;
		if(currency in currency_rate.keys()):
			currency_rate[currency] = float(rate);
		else:
			break;

path = os.getcwd();
slash = "/";
if (platform == "win32"):
	slash = "\\";
input_files = glob.glob(os.path.join(path, "input" + slash + "*.xlsx"))
# pd.set_option('display.max_columns', None);
comparative_df = pd.DataFrame();
print(comparative_df);
needs_assignment = True;
currency_rate = {'$': 1, '€': 1, '£': 1, '₹': 1};
non_vendor_columns = 0;
for f in input_files:
	# f contains the path to all csv that have to considered input
	vendor = get_vendor_name(f);
	print(vendor)
	df = pd.read_excel(f, skiprows = 4);
	print(df.columns);
	# ['SL.No', 'Indent. NO', 'Author', 'Title', 'Ed/Year', 'Publisher', 'List Price of the Book (Single Copy)', 'Conversion Rate', 'Discount', 'QTY', 'Total Price (INR)']
	update_conversion_rate(df, currency_rate);
	print(currency_rate);
	df = df[df[df.columns[0]].notna()];

	if(needs_assignment):
		assingment_columns = [df.columns[i] for i in range(6)];
		print(assingment_columns)
		for col in assingment_columns:
			comparative_df[col] = df[col];
		non_vendor_columns = len(comparative_df.columns);
		needs_assignment = False;
	else:
		needs_assignment = False;
		# check quotation response validity
	total_values = []
	df['List Price of the Book (Single Copy)'].fillna("NA", inplace = True);
	df['Conversion Rate'].fillna("NA", inplace = True);
	df['Discount'].fillna("NA", inplace = True);
	df['QTY'].fillna("NA", inplace = True);
	df['Total Price (INR)'].fillna(math.inf, inplace = True);
	for i, r in df.iterrows():
		listprice = r['List Price of the Book (Single Copy)'];
		conversion_rate = r['Conversion Rate'];
		discount = r['Discount'];
		quantity = r['QTY'];
		total = r['Total Price (INR)'];
		currency = '₹';
		cost = 0;
		if(listprice == "NA"):
			total_values.append(total);
			continue;
		else:
			currency = listprice[0];
			cost = float(listprice[1:]);

		if(conversion_rate == "NA"):
			conversion_rate = currency_rate[currency];

		if(discount == "NA"):
			discount = 0.0;

		if(quantity == "NA"):
			quantity = 1;

		new_total = quantity * (cost * conversion_rate) * (100 - discount) / 100;
		total = min(total, new_total);
		total_values.append(total);
		
	# df['currency'] = df['List Price of the Book (Single Copy)'].apply(lambda x: not x.isdigit());
	comparative_df[vendor] = total_values;
	print(df);



# Add L1 Vendor
min_total = comparative_df.loc[:, comparative_df.columns[non_vendor_columns:]].idxmin(axis = 1)
comparative_df['L1 Vendor'] = min_total.to_numpy();


print(comparative_df)

outputfile = "comparative_sheet.xlsx";
comparative_df.to_excel("output" + slash + outputfile, index = False);