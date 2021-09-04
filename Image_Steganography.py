from PIL import Image
from os import system
import cv2
import numpy as np
import time


genData = lambda data : [(format(ord(i), '08b')) for i in data]
getPix = lambda imgdata : imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]


def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		pix = [value for value in getPix(imdata)]	
		
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j] % 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
					
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]


def encode_enc(newimg, data):
	w = newimg.size[0]

	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1


def open(enordec):
	while True:
		try:
			if enordec == "encode":
				choice = int(input("1. Select an Image\n2. Capture an Image\n"))
				if choice == 1:
					name = input("Enter image name (with extension) : ")
				
				elif choice == 2:
					name = input("Enter the name to save the image as (with extension) : ")
					print("Press Space to Capture.")
					cam = cv2.VideoCapture(0)
					time.sleep(1)
					while True:
							_, imag = cam.read()
							cv2.imshow("Camera",imag)
							key = cv2.waitKey(1)
							if key == 32:
								cv2.imwrite(name,imag)
								break
					cam.release()
					cv2.destroyAllWindows()

			elif enordec == "decode":
				name = input("Enter image name (with extension) : ")

			image = Image.open(name, 'r')	
			cv2.imshow("Image", cv2.imread(name))
			print("The size of the selected image is : ", image.size)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

			inp = int(input("Is the displayed image correct?\n1. Yes\t2. No\n"))
			if inp == 1:
				break
			
		except:
			print("File Not Found. Please try again.")
	return [name, image]


def encode():
	[imgname, image] = open("encode")

	data = input("Enter data to be encoded : ")
	if (len(data) == 0):
		raise ValueError('Data is empty.')

	newimg = image.copy()
	encode_enc(newimg, data)

	new_img_name = input("Enter the name of new image(with extension) : ")
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
	print("The new image with the specified name is saved.")

	img1 = cv2.imread(imgname)
	img2 = cv2.imread(new_img_name)
	imgjoin = np.concatenate((img1, img2), axis = 1)
	imgjoin = cv2.line(imgjoin, (image.size[0],0), (image.size[0],image.size[1]), (0,0,0), 2)
	cv2.imshow("Original V/S Encoded Image", imgjoin)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def decode():
	[_, image] = open("decode")
	data = ''
	imgdata = iter(image.getdata())
		
	while (True):
		pixels = [value for value in getPix(imgdata)]
		binstr = ''
		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data


while True:
	a = int(input("Image Steganography\n1. Encode\n2. Decode\n3. Exit\n"))

	if a == 1:
		encode()

	elif a == 2:
		data = decode()
		print("Decoded Word : ", data)

	elif a == 3:
		print('Exiting.')
		_=system('cls')
		break

	else:
		print("Enter correct input")

	input("Press any key.")
	system('cls')
