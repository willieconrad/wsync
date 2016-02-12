import os
import argparse

class WSync:

	def __init__(self, src, dst):
		self.src = src 
		self.dst = dst

	def sync(self):
		for root, dirs, files in os.walk(self.src):
			for f in files:
				src_path = os.path.join(root, f)
				relative_path = os.path.relpath(src_path, self.src)
				dst_path = os.path.join(self.dst, relative_path)
				print src_path + " --> " + dst_path	
				if not os.path.exists(dst_path):
					print "\tNo destination file ... copying"
				elif os.path.islink(dst_path):
					print "\tDestination is symlink ... bailing"
				elif os.path.isdir(dst_path):
					print "\tSource is file, destination is directory ... bailing"
				elif os.path.getsize(src_path) != os.path.getsize(dst_path):
					print "\tSource and destination are different sizes ... which one do we keep?"
				elif os.path.getmtime(src_path) < os.path.getmtime(dst_path):
					print "\tFiles match in size, but source is older ... touching dst file"
				else:
					print "\tFiles are identical in size and mtime."
				

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Copy stuff awesome.')
	parser.add_argument('src', help='Source directory')
	parser.add_argument('dst', help='Destiation directory')
	args = parser.parse_args()

	wsync = WSync(args.src, args.dst)
	wsync.sync()
