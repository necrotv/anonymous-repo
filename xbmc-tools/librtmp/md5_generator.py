import os
import sys
import hashlib
 
if sys.version < '3':
	import codecs
	def u(x):
		return codecs.unicode_escape_decode(x)[0]
else:
	def u(x):
		return x
 
class Generator:

	def __init__( self ):
		# generate files
		self._generate_md5_file()
		# notify user
		print("Finished md5 files")

	def _md5sum_verified( self, path):
		BLOCK_SIZE = 65536
		hasher = hashlib.md5()
		f = open(path,'rb')
		done = 0
		size = os.path.getsize(path)
		while done < size:
			data = f.read(BLOCK_SIZE)
			done += len(data)
			hasher.update(data)
			if not data: break		
		md5sum = hasher.hexdigest()
		return md5sum

	def _generate_md5_file( self ):
		# save file
		try:
			self._save_file(self._md5sum_verified("Windows/librtmp.dll"), file="md5/windows.xml.md5" )
			self._save_file(self._md5sum_verified("Android/librtmp.so"), file="md5/android.xml.md5" )
			self._save_file(self._md5sum_verified("RaspberryPI/librtmp.so.0"), file="md5/raspberry.xml.md5" )
			self._save_file(self._md5sum_verified("iOS/librtmp.0.dylib"), file="md5/ios.xml.md5" )
			self._save_file(self._md5sum_verified("Linux/x64/librtmp.so.0"), file="md5/linux_x64.xml.md5" )
			self._save_file(self._md5sum_verified("Linux/x86&ATV1/librtmp.so.0"), file="md5/linux_x86.xml.md5" )
			self._save_file(self._md5sum_verified("macOS/x64/librtmp.0.dylib"), file="md5/macos_x64.xml.md5" )
			self._save_file(self._md5sum_verified("macOS/x86/librtmp.0.dylib"), file="md5/macos_x86.xml.md5" )
		except Exception as e:
			# oops
			print("An error occurred creating ...xml.md5 file!\n%s" % e)

	def _save_file( self, data, file ):
		try:
			# write data to the file (use b for Python 3)
			open( file, "w" ).write( data )
		except Exception as e:
			# oops
			print("An error occurred saving %s file!\n%s" % ( file, e ))

if ( __name__ == "__main__" ):
	# start
	Generator()