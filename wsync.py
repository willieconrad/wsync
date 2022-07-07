#!/usr/bin/python
import os
import shutil
import argparse

class WSync:

	def __init__(self, src, dst, dry_run, verbose):
		self.src = src 
		self.dst = dst
		self.dry_run = dry_run
		self.verbose = verbose

	def sync(self):
		for root, dirs, files in os.walk(self.src):
			for f in files:
				src_path = os.path.join(root, f)
				relative_path = os.path.relpath(src_path, self.src)
				dst_path = os.path.join(self.dst, relative_path)
				if not os.path.exists(dst_path):
					#TODO: also check reverse case
					try:
						unicode(dst_path).encode('utf-8')
					except UnicodeDecodeError:
						dst_path_utf8 = dst_path.decode('iso-8859-1').encode('utf-8')
						if os.path.exists(dst_path_utf8):
							#print src_path + " Exists int utf-8 form!"
							dst_path = dst_path_utf8
					
				paths = src_path + " --> " + dst_path	
				
				if not os.path.exists(dst_path):
					print src_path + " No destination file ... copying"
					if not self.dry_run:
						dst_dir = os.path.dirname(dst_path)
						# Could possibly do this before the for loop
						if not os.path.isdir(dst_dir):
							os.makedirs(dst_dir)
						shutil.copy2(src_path, dst_path)
				elif os.path.islink(dst_path):
					print src_path + " Destination is symlink ... bailing"
				elif os.path.isdir(dst_path):
					print src_path + " Source is file, destination is directory ... bailing"
				elif os.path.getsize(src_path) != os.path.getsize(dst_path):
					print src_path + " Source and destination are different sizes ... which one do we keep?"
				elif os.path.getmtime(src_path) - os.path.getmtime(dst_path) > 1:
					if self.verbose:
						print src_path + " Files match in size, but source has newer mtime.  Ignoring."
				elif os.path.getmtime(dst_path) - os.path.getmtime(src_path) > 1:
					print src_path + " Files match in size, but source has older mtime.  Touching destination."
					if not self.dry_run:
						src_mtime = os.path.getmtime(src_path)
						dst_atime = os.path.getatime(dst_path)
						os.utime(dst_path, (dst_atime, src_mtime))
				else:
					if self.verbose:
						print src_path + " Files are identical in size and mtime."
				

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Copy stuff awesome.')
	parser.add_argument('--dry-run', '-n', dest="dry_run", action='store_true', default=False)
	parser.add_argument('--verbose', '-v', dest="verbose", action='store_true', default=False)
	parser.add_argument('src', help='Source directory')
	parser.add_argument('dst', help='Destiation directory')
	args = parser.parse_args()

	wsync = WSync(args.src, args.dst, args.dry_run, args.verbose)
	wsync.sync()
