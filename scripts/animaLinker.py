#python
import lx
import modo
import os
'''
This script links MDD files in a location to matching mesh names (of a fashion) in a scene.
This was developed with Anima exports in mind.

Thanks to Simon Lundberg for guidance with the TD SDK.
'''

def main():
	scene = modo.Scene()
	graph = lx.object.ItemGraph(scene.GraphLookup('deformers'))
	items = scene.items('mesh')
	if (len(items) == 0):
		sys.exit()
	targetFile = customfile('fileOpen', 'Choose any MDD file', 'mdd', 'MDD', '*.mdd', None)
	if (targetFile != None):
		targetLocation = os.path.dirname(targetFile)
		lx.out('targetLocation: {%s}' % targetLocation)
		monitor = lx.Monitor( len(items) )     
		for item in items:
			monitor.step()
			lx.eval('select.drop item')
			meshName = item.UniqueName()
			# Take out character naming off the end. Only for Anima 1.x
			tempArray = meshName.split('--')
			if len(tempArray) > 1:
				# Add back a trailing dash to match naming convention for MDD files
				meshName = tempArray[0] + "-"
			lx.out('meshName: {%s}' % meshName)
			filepath = targetLocation + os.sep
			lx.out('filepath: {%s}' % filepath)
			filepath = filepath + meshName + ".mdd"
			''' mesh = item.Ident()'''
			deformer = scene.addItem('deformMDD2')
			graph.AddLink(deformer, item)
			deformer.channel('file').set(filepath)
			lx.eval('select.drop item')
			lx.eval('select.item {%s}' % deformer.Ident())
			lx.eval('deform.mddReload')
	else:
		sys.exit()

# From Gwynne Reddick
def customfile(type, title, format, uname, ext, save_ext=None, path=None):
	'''
		Open a file requester for a custom file type and return result
		type - open or save dialog (fileOpen or fileSave)
		title - dialog title
		format - file format
		uname - format username
		ext - file extension in the form '*.ext'
		save_ext - (optional)
		path - (optional) Default path to open dialog with
		
		examples:
			file = customfile('fileOpen', 'Open JPEG file', 'JPG', 'JPEG File', '*.jpg;*.jpeg')
			file = customfile('fileSave', 'Save Text file', 'TXT', 'Text File', '*.txt', 'txt')
	
	'''
	lx.eval('dialog.setup %s' % type)
	lx.eval('dialog.title {%s}' % (title))
	lx.eval('dialog.fileTypeCustom {%s} {%s} {%s} {%s}' % (format, uname, ext, save_ext))
	if type == 'fileSave' and save_ext != None:
		lx.eval('dialog.fileSaveFormat %s' % save_ext)
	if path != None:
		lx.eval('dialog.result {%s}' % (path + 'Scenes'))
	try:
		lx.eval('dialog.open')
		return lx.eval('dialog.result ?')
	except:
		return None

	#stlfile = customfile('fileOpen', 'Load STL file', 'stl', 'STL', '*.stl')

main()