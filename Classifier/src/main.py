# Adicionando caminho do modulo Leap (em tempo de execucao) para que seja possivel importa-lo. 
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

from collections import OrderedDict
import csv, Leap
from sklearn.externals import joblib
import socket
from time import sleep

def getFrameSnapshot(*args):
	args = list(args)
	controller = args[0]
	frame = controller.frame()

	# Armazenando os vetores direcionais da ponta de cada osso, para cada dedo.
	fingers = frame.fingers
	fingerBones = []
	for finger in fingers:
		fingerBones.append(finger.bone(Leap.Bone.TYPE_METACARPAL).next_joint)
		fingerBones.append(finger.bone(Leap.Bone.TYPE_PROXIMAL).next_joint)
		fingerBones.append(finger.bone(Leap.Bone.TYPE_INTERMEDIATE).next_joint)
		fingerBones.append(finger.bone(Leap.Bone.TYPE_DISTAL).next_joint)

	# Obtendo o vetor que corresponde ao centro da mao.
	''' Aqui se assume que apenas UMA mao e detectada. '''
	hands = frame.hands
	handCenter = Leap.Vector(0, 0, 0)
	for hand in hands:
		handCenter = hand.palm_position

	# Subtraindo o vetor dos ossos dos dedos pela posicao da mao (normalizacao).
	translatedFingerBones = OrderedDict()
	for i in range(len(fingerBones)):
		translatedJoint = (fingerBones[i] - handCenter).to_tuple()
		for j in range(3):
			translatedFingerBones["feat" + str(i*3+j)] = translatedJoint[j]

	if (len(args) == 2):
		target = args[1]
		translatedFingerBones['target'] = target

		# Convertendo dicionario em uma linha de arquivo csv.
		with open('../data/libras.csv', 'a') as csvFile:
			fieldNames = translatedFingerBones.keys()
			writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
			# writer.writeheader()
			writer.writerow(translatedFingerBones)

	return translatedFingerBones

def main():
	controller = Leap.Controller()

	key = raw_input("Digite 1 para treinar ou 2 para classificar e 'q' para sair\n")
	if key == '1':
		while True:
			key = raw_input('Enter -> Capturar o quadro.\n')
			if key == '':
				target = raw_input('Codigo da letra/numero/palavra: ')
				print getFrameSnapshot(controller, target)
			elif key == 'q':
				break
	if key == '2':
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		host = ''
		port = 3000

		try:
			address = (host,port)
			s.bind(address)
		except socket.error as e:
			print(e)
			exit(0)

		s.listen(1)

		conn, addr = s.accept()
		print "conexão aceita"
		print "ctrl + c para sair"

		# load the model from disk
		trained_model = open("trained_model.sav", 'r')
		loaded_model = joblib.load(trained_model)

		try:
			while(True):
				new_value = getFrameSnapshot(controller)
				result = loaded_model.predict(new_value)
				conn.send((result + "\n").encode())
				print(result)
				sleep(1)
		except(KeyboardInterrupt, socket.error) as e:
			conn.close()
			s.close()

if __name__ == '__main__':
	main()