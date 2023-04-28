# Author: Rewant Raj

import os
import glob
from sys import platform
from sys import stderr
from sys import exit
import pandas as pd
import numpy as np
import math
from itertools import filterfalse

path = os.getcwd();
slash = "/";
if (platform == "win32"):
	slash = "\\";
input_path = "input" + slash;
output_path = "output" + slash;


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

def fill_missing_values(df):
	df['List Price of the Book (Single Copy)'].fillna("NA", inplace = True);
	df['Conversion Rate'].fillna("NA", inplace = True);
	df['Discount'].fillna("NA", inplace = True);
	df['QTY'].fillna("NA", inplace = True);
	df['Total Price (INR)'].fillna(math.inf, inplace = True);

def get_min_total(row, currency_rate):
	listprice = row['List Price of the Book (Single Copy)'];
	conversion_rate = row['Conversion Rate'];
	discount = row['Discount'];
	quantity = row['QTY'];
	total = row['Total Price (INR)'];
	currency = '₹';
	cost = 0;
	
	if(listprice == "NA"):
		return total;
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
	return total;

class CSG:
	def __init__(self, input_dir = input_path, output_dir = output_path, output_file = "comparative_sheet.xlsx"):
		self.input_files = glob.glob(os.path.join(path, input_dir + "*.xlsx"));
		self.output_path = os.path.join(path, output_dir + output_file);
		self.comparative_df = pd.DataFrame();
		self.needs_assignment = True;
		self.currency_rate = {'$': 1, '€': 1, '£': 1, '₹': 1};
		self.non_vendor_columns = 0;

	def prepare_comparative_sheet(self):
		for f in self.input_files:
			vendor = get_vendor_name(f);
			df = pd.read_excel(f, skiprows = 4);
			update_conversion_rate(df, self.currency_rate);
			df = df[df[df.columns[0]].notna()];

			if(self.needs_assignment):
				assingment_columns = [df.columns[i] for i in range(6)];
				for col in assingment_columns:
					self.comparative_df[col] = df[col];
				self.non_vendor_columns = len(self.comparative_df.columns);
				self.needs_assignment = False;
			else:
				if(not self.comparative_df[df.columns[:self.non_vendor_columns]].equals(df[df.columns[:self.non_vendor_columns]])):
					print(self.comparative_df[df.columns[:self.non_vendor_columns]].compare(df[df.columns[:self.non_vendor_columns]], align_axis = 0, result_names = ('current', 'previous')));
					print(f"{f} doesn't match with the previous entries", stderr);
					raise SystemExit(1);
				self.needs_assignment = False;
		
			total_values = []
			fill_missing_values(df);
			for i, r in df.iterrows():
				total = get_min_total(r, self.currency_rate);
				total_values.append(total);
				
			self.comparative_df[vendor] = total_values;
			print(df);

	def compute_l1_vendor(self):
		min_total = self.comparative_df.loc[:, self.comparative_df.columns[self.non_vendor_columns:]].idxmin(axis = 1)
		self.comparative_df['L1 Vendor'] = min_total.to_numpy();

	def generate_sheet(self):
		print(self.comparative_df);
		self.comparative_df.to_excel(self.output_path, index = False);

	def run(self):
		self.prepare_comparative_sheet();
		self.compute_l1_vendor();
		self.generate_sheet();

def main():
	csg = CSG();
	csg.run();

if __name__ == "__main__":
	main();