from PIL import Image
import glob,os,time

def resize(thePicture):
        global sizedPicture
        width = thePicture.size[0]
        height = thePicture.size[1]
        ratioWidth = 500 / (border[2]-border[0])
        if border[2] - border[0]>500:
                midPicture = thePicture.resize((int(width*ratioWidth),int(height*ratioWidth)),Image.ANTIALIAS)
                if (border[3] - border[1])*ratioWidth>400:
                        ratioHeight = 400 / ((border[3] - border[1])*ratioWidth)
                        sizedPicture = midPicture.resize((int(width*ratioWidth*ratioHeight),int(height*ratioWidth*ratioHeight)),Image.ANTIALIAS)
                else:
                        sizedPicture =midPicture
        else:
                midPicture = thePicture
                if (border[3] - border[1])>400:
                        ratioHeight = 400 / (border[3]-border[1])
                        sizedPicture = midPicture.resize((int(width*ratioHeight),int(height*ratioHeight)),Image.ANTIALIAS)
                else:
                        sizedPicture = midPicture
        return sizedPicture
                
def getBorder(thePicture):
	global border
	if thePicture.mode == "RGB":
		pix = thePicture.load()
		ptMtxNormal = [[9 for col in range(thePicture.size[0])] for row in range(thePicture.size[1])]
		for i in range(thePicture.size[1]):
			for j in range(thePicture.size[0]):
				if pix[j,i][0]>225 and pix[j,i][1]>225 and pix[j,i][2]>225:
					ptMtxNormal[i][j] = 0
				else:
					ptMtxNormal[i][j] = 1
		vertical = [9 for i in range(len(ptMtxNormal))]
		ptMtxTransposed = list(map(list, zip(*ptMtxNormal)))
		horizontal = [9 for i in range(len(ptMtxTransposed))]
		for i in range(len(ptMtxNormal)):
			if 1 in ptMtxNormal[i]:
				vertical[i] = 1
			else:
				vertical[i] = 0
		for i in range(len(ptMtxTransposed)):
			if 1 in ptMtxTransposed[i]:
				horizontal[i] = 1
			else:
				horizontal[i] = 0
		border = [horizontal.index(1),vertical.index(1),thePicture.size[0] - horizontal[::-1].index(1),thePicture.size[1] - vertical[::-1].index(1)]
	else:
		border = thePicture.getbbox()
	return border

def pictureCut(thePicture, left = 20, up = 20, right = 20, bottom = 20):
        global cutPicture
        getBorder(thePicture)
        region = [border[0] - left, border[1] - up, border[2] + right, border[3] + bottom]
        rawPicture = thePicture.crop(region)
        if rawPicture.mode == "RGB":
                if border[0] - left < 0:
                        rawPicture.paste((255,255,255),(0,0,20,rawPicture.size[1]))
                if border[1] - up < 0:
                        rawPicture.paste((255,255,255),(0,0,rawPicture.size[0],20))
                if border[2] - thePicture.size[0] < 20:
                        rawPicture.paste((255,255,255),(rawPicture.size[0]-20,0,rawPicture.size[0],rawPicture.size[1]))
                if border[3] - thePicture.size[1] < 20:
                        rawPicture.paste((255,255,255),(0,rawPicture.size[1]-20,rawPicture.size[0],rawPicture.size[1]))
                cutPicture = rawPicture
        else:
                cutPicture = rawPicture
        cutPicture = rawPicture
        return cutPicture

def autoPicProcessor(inputPath):
	i = 1
	totalTime = 0
	for files in glob.glob(inputPath+"/*.[jp][pn]g"):
		filePath, fileName = os.path.split(files)
		filterAme, exts = os.path.splitext(fileName)
		outputPath = filePath+"/copy/"
		if os.path.isdir(outputPath) == False:
			os.mkdir(outputPath)
		im = Image.open(files)
		startTime = time.clock()
		getBorder(im)
		resize(im)
		pictureCut(sizedPicture)	
		cutPicture.save(outputPath+filterAme+exts)
		endTime = time.clock()
		secondConsumed = round((endTime - startTime),3)
		print(i,fileName,im.mode,im.size,"->",cutPicture.size,secondConsumed)
		i += 1
		totalTime = totalTime + secondConsumed
	print(i-1,"Pictures have been resized and cut within",totalTime,"seconds")
