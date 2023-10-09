plaintext = input("Plaintext: ")
cipherText = ""
alphabet = "XYZABCDEFGHIJKLMNOPQRSTUVWXYZABC"
plaintextPosition = 0

while (plaintextPosition < len(plaintext)):
    plaintextChar = plaintext[plaintextPosition]
    alphabetPosition = 3

    while plaintextChar != alphabet[alphabetPosition]:
        alphabetPosition += 1

    alphabetPosition -= 3
    cipherText = cipherText+alphabet[alphabetPosition]
    plaintextPosition += 1

print(cipherText)


# 2a) ILSBMVQELK
# 2b) ILSBRLJ
# 2c) FULLOFLOVE
