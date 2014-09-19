# *
# *  Copyright (C) 2012-2013 Garrett Brown
# *  Copyright (C) 2010      j48antialias
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  Based on code by j48antialias:
# *  https://anarchintosh-projects.googlecode.com/files/addons_xml_generator.py
 
""" addons.xml generator """
 
import os
import sys
import hashlib
 
# Compatibility with 3.0, 3.1 and 3.2 not supporting u"" literals
if sys.version < '3':
	import codecs
	def u(x):
		return codecs.unicode_escape_decode(x)[0]
else:
	def u(x):
		return x
 
class Generator:
	"""
		Generates a new addons.xml file from each addons addon.xml file
		and a new addons.xml.md5 hash file. Must be run from the root of
		the checked-out repo. Only handles single depth folder structure.
	"""

	def __init__( self ):
		# generate files
		self._generate_md5_file()
		# notify user
		print("Finished updating addons xml and md5 files")

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
		except Exception as e:
			# oops
			print("An error occurred creating addons.xml.md5 file!\n%s" % e)

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