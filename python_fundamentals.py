
class Basics:  # (s)
    
    def read_file(self):  # (s)
        """
            Read in the text file and save the paragraph to a single string

            :return: A text file paragraph as a string
        """
        
        f = open("text.txt", 'r+')
        text=f.readline()
        f.close()
        return text
        pass

   
    def length_of_file(self):  # (s)
        """
            Reports the length of the paragraph including numbers and whitespace

            :input_text: The text file paragraph as a string
            :return: An integer length of the file
        """
        input_text = self.read_file()  # (s)
      
        return len(input_text)


  
    def if_apple(self):  # (s)
        """
            Reports a boolean True/False if the paragraph contains the entire word "apple"

            :input_text: The text file paragraph as a string
            :return: A boolean True/false
        """
        input_text = self.read_file()  # (s)
        
        words = input_text.replace(".","")
        words = words.split(" ")[1::]
        for i in words:
            if i=="apple":
                return True
        return False


    def if_upper_case_exists(self):  # (s)
        """
            Reports a boolean True/False if the paragraph contains any number of upper case letters

            :input_text: The text file paragraph as a string
            :return: A boolean True/false
        """
        input_text = self.read_file()  # (s)

        words = input_text.replace(".","")
        words = words.split(" ")[1::]
        for i in words:
            if i.lower()!=i:
                return True
        return False
    

   
    def if_numbers_exist(self):  # (s)
        """
            Reports a boolean True/False if the paragraph contains any number of integers

            :input_text: The text file paragraph as a string
            :return: A boolean True/false
        """
        input_text = self.read_file()  # (s)
        
        words = input_text.replace(".","")
        words = words.split(" ")[1::]
        for i in words:
            try:
                n = int(i)
                return True
            except:pass
        return False

    def if_spaces_exist(self):  # (s)
        """
            Reports a boolean True/False if the paragraph contains any number of blank spaces

            :input_text: The text file paragraph as a string
            :return: A boolean True/false
        """
        input_text = self.read_file()  # (s)
     
        for i in input_text:
            if i == " ":
                return True
        return False

   
    def if_first_letter_t(self):  # (s)
        """
            Reports a boolean True/False if the first letter of the paragraph is a t

            :input_text: The text file paragraph as a string
            :return: A boolean True/false
        """
        input_text = self.read_file() 
  
        words = input_text.replace(".","")
        words = words.split(" ")[1::]
        return True if words[0][0]=="t" else False
        


    def fourth_letter_seventh_word(self):  # (s)
        """
            Reports the fourth letter in the seventh word of the paragraph as a string

            :input_text: The text file paragraph as a string
            :return: A string letter
        """
        input_text = self.read_file()  # (s)
       
        words = input_text.replace(".","")
        words = words.split(" ")[1::]
        
        try:
            word=words[6]
            character = word[3]
            return character
        except:
            return ""


    def convert_to_lower_case(self):  # (s)
        """
            Converts the paragraph to entirely lowercase with no other changes

            :input_text: The text file paragraph as a string
            :return: A string paragraph
        """
        input_text = self.read_file()  # (s)
     
        newText = ""
        for i in range(len(input_text)):
            n=int(ord(input_text[i]))
            
            if n<=ord("Z") and n>=ord("A"):
                newText+=chr(n+32)
            else:
                newText+=chr(n)
                
        return newText
       

   
    def reverse_paragraph(self):  # (s)
        """
            Reverses the paragraph such that it can be read backwards with no other changes

            :input_text: The text file paragraph as a string
            :return: A string paragraph
        """
        input_text = self.read_file()  # (s)
     
        return input_text[::-1]
        
 
    def duplicate_and_concatenate_paragraph(self):  # (s)
        """
            Duplicate the paragraph and combine them such that they can be read twice in order with
            no other changes

            :input_text: The text file paragraph as a string
            :return: A string paragraph
        """
        input_text = self.read_file()  # (s)

        return input_text+input_text



    def remove_whitespace_from_paragraph(self):  # (s)
        """
            Remove any whitespace from the paragraph except spaces between words and numbers with no
            other changes

            :input_text: The text file paragraph as a string
            :return: A string paragraph
        """
        input_text = self.read_file()  # (s)
 
        return input_text.strip()





