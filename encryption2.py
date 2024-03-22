plaintext = input("Plaintext: ")
cipherText = ""

plaintextPosition = 0

while (plaintextPosition < len(plaintext)):
    plaintextChar = plaintext[plaintextPosition]
    ASCIIValue = ord(plaintext[plaintextPosition]) - 3
    if plaintext[plaintextPosition] in ['a', 'b', 'c', 'A', 'B', 'C']:
        ASCIIValue += 27
    cipherText = cipherText+chr(ASCIIValue)
    plaintextPosition += 1

print(cipherText)
