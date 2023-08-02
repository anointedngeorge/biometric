from pyfingerprint.pyfingerprint import PyFingerprint
import time

try:
    f = PyFingerprint('COM1', 57600, 0xFFFFFFFF, 0x00000000)
    if f.verifyPassword() == False:
        raise ValueError('The given fingerprint sensor password is wrong!')
except Exception as e:
    print('Error: ' + str(e))
    exit(1)


try:
    print('Waiting for finger...')
    while f.readImage() == False:
        pass
    f.convertImage(0x01)
    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber >= 0:
        print('Fingerprint already exists at position #' + str(positionNumber))
        exit(0)

    print('Remove finger...')
    time.sleep(2)

    print('Place the same finger again...')
    while f.readImage() == False:
        pass
    f.convertImage(0x02)

    if f.compareCharacteristics() == 0:
        raise Exception('Fingers do not match')

    f.createTemplate()
    positionNumber = f.storeTemplate()
    print('Fingerprint enrolled successfully at position #' + str(positionNumber))
except Exception as e:
    print('Error: ' + str(e))
    exit(1)
