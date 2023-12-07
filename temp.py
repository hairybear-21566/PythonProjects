"""
This is a stub for the comp16321 midterm.
Do not edit or delete any lines given in this file that are marked with a "(s)".
(you can move them to different lines as long as you do not change the overall structure)

Place your code below the comments marked "#Your code here".

Each method is documented to explain what work is to be placed within it.

NOTE: You can create as many more methods as you need. However, you need to add 
self as a parameter of the new method and to call it with the prefix self.name 

EXAMPLE:

def class_table_result(self, boat_type, race_results):#(s)
    strings_value = "0601-0501-0702-0803-0904-0405-0306-0207-1008-0609-0110"
    single_boat = self.remove_highest_value(strings_value)
    return(single_boat)

def remove_highest_value(self, strings_value):
    strings_value.pop(10)
    return strings_value

"""


class Races:#(s)

    def read_results(self):#(s)
        """
        Read in the text file and save the races_results into a python list

        :return: A list of strings denoting each race_result
        """

        # Your code here

        lines = []  # result strings
        with open("input.txt", "r") as f:
            line = f.readline().rstrip()
            while line != "":
                lines.append(line)
                line = f.readline().strip()

        return lines
        pass#(s)

    def race_result(self, boat_type, race_number, results_string):#(s)
        """
        Query results_string which is read form the input.txt and  get the  result
        for the given params

        :param: boat_type: An integer denoting which type of boat 
        :param: race_number: An integer denoting which race
        :return: A string with the race result for the given boat_type and race_number
        """

        # Your code here

        race_code = "0"+str(boat_type) if boat_type < 10 else str(boat_type)
        for r in results_string:
            if r[0:2] == race_code:
                if race_number == 1: return r[5:]
                else: race_number -= 1
        return ""

        pass#(s)

    def class_table_result(self, boat_type, results_string):#(s)
        """
        Output the results for a given boat_type

        :param: boat_type: An integer denoting which type of boat 
        :return: A string in the specified format as shown in the pdf
        """

        # Your code here

        races_arr = []
        race_code = "0"+str(boat_type) if boat_type < 10 else str(boat_type)
        for r in results_string:
            if r[0:2] == race_code : races_arr.append(r)

        last_race = races_arr[-1][5:].split("-")
        country_results = [["0"+str(x) if x < 10 else str(x), 1, 0]for x in range(1, 11)]
        for race in races_arr:
            mult = 2 if int(race[2:4]) == 2 else 1
            outcome = race[5:].split("-")
            points_added = 1
            for place in outcome:
                if place[2:4] != "xx":
                    country_results[int(place[0:2]) -1][2] += points_added * mult
                    points_added += 1
                else: country_results[int(place[0:2])-1][2] += 11 * mult
        country_results = sorted(country_results, key=lambda x: x[2])

        ########################
        # handling tie breakers
        ########################

        corrected_country_results = []
        i = 1
        prob_start = 0
        prob_end = 0

        def resolve_ties(x_count, prob_start, prob_end):
            if prob_end == prob_start:
                arr = [country_results[prob_start]]

            else:
                section_in_question = country_results[prob_start:prob_end+1]
                countries_in_question = [
                    c for c, _, _ in country_results[prob_start:prob_end+1]]
                priority_of_section = [
                    0 for rand in range(len(section_in_question))]

                x_count = 0
                priotity_index = 1

                for pos in last_race:
                    if pos[2:] != "xx" and pos[0:2] in [country for country, _, _ in section_in_question]:
                        priority_of_section[countries_in_question.index(
                            pos[0:2])] = 11 + x_count
                        x_count += 1

                    elif pos[0:2] in [country for country, _, _ in section_in_question]:
                        priority_of_section[countries_in_question.index(
                            pos[0:2])] = priotity_index
                        priotity_index += 1

                    arr = [x for x, y in
                           sorted(zip(section_in_question, priority_of_section), key=lambda u: u[1])]

            return x_count, arr

        xx_count = 0
        for i in range(10):

            if country_results[prob_start][2] == country_results[i][2]: 
                
                prob_end += 1
            else:
                xx_count, sec_sorted = resolve_ties(
                    xx_count, prob_start, prob_end)
                corrected_country_results += sec_sorted
                prob_start = i
                prob_end = i

        xx_count, sec_sorted = resolve_ties(xx_count, prob_start, prob_end)
        corrected_country_results += sec_sorted

        for wr in range(len(corrected_country_results)):
            corrected_country_results[wr][1] = "0"+str(wr+1) if wr+1 < 10 else str(wr+1)
            corrected_country_results[wr][2] = "0"+str(
                corrected_country_results[wr][2]) if corrected_country_results[wr][2] < 10 else str(
                corrected_country_results[wr][2])
            
        
        output = ""
        for final_word in corrected_country_results:
            output += final_word[0]+"-"+final_word[1]+"-"+final_word[2]+", "

        return output[:-2]

        pass#(s)

    def class_table_discard_result(self, boat_type, results_string):#(s)
        """
        Output the class table discard string

        :param: boat_type: An integer denoting which type of boat 
        :return: A string in the specified format as shown in the pdf
        """

        # Your code here
        def format_output(to_format):
            for wr in range(len(to_format)):
                to_format[wr][1] = "0"+str(wr+1) if wr+1 < 10 else str(wr+1)
                to_format[wr][2] = "0"+str(to_format[wr][2]) if to_format[wr][2] < 10 else str(to_format[wr][2])
            output = ""
            for final_word in to_format:
                output += final_word[0]+"-"+final_word[1]+"-"+final_word[2]+", "
            return output[:-2]

        def resolve_ties(x_count, prob_start, prob_end):

            if prob_end == prob_start:
                arr = [country_results[prob_start]]

            else: 
                section_in_question = country_results[prob_start:prob_end+1]
                countries_in_question = [
                    c for c, _, _ in country_results[prob_start:prob_end+1]]
                priority_of_section = [0 for rand in range(len(section_in_question))]

                x_count = 0
                priotity_index = 1

                for pos in last_race:
                    if pos[2:] != "xx" and pos[0:2] in [country for country, _, _ in section_in_question]:
                        priority_of_section[countries_in_question.index(
                            pos[0:2])] = 11 + x_count
                        x_count += 1

                    elif pos[0:2] in [country for country, _, _ in section_in_question]:
                        priority_of_section[countries_in_question.index(
                            pos[0:2])] = priotity_index
                        priotity_index += 1

                    arr = [x for x, y in
                           sorted(zip(section_in_question, priority_of_section), key=lambda u: u[1])]

            return x_count, arr


        max_double, max_single=[0 for i in range(10)]

        races_arr = []
        race_code = "0"+str(boat_type) if boat_type < 10 else str(boat_type)
        for r in results_string:
            if r[0:2] == race_code:
                races_arr.append(r)
        last_race = races_arr[-1][5:].split("-")

        double_count, single_count = 0

        country_results = [["0"+str(x) if x < 10 else str(x), 1, 0]
                           for x in range(1, 11)]
        
        for race in races_arr:
            mult = 2 if int(race[2:4]) == 2 else 1
            single_count += 0 if mult==2 else 1
            double_count += 1 if mult==2 else 0
            outcome = race[5:].split("-")
            points_added = 1
            for place in outcome:
                if place[2:4] != "xx":
                    points = points_added * mult
                    country_results[int(place[0:2]) - 1][2] += points_added * mult
                    points_added += 1
                else:
                    points=11 * mult
                    country_results[int(place[0:2])-1][2] += 11 * mult
                if mult==2:
                    max_double[int(place[0:2])-1] = max(max_double[int(place[0:2])-1], points )
                else:
                    max_single[int(place[0:2])-1] = max(max_single[int(place[0:2])-1], points )

        if single_count > 2:
            for temp1 in range(10):
                country_results[temp1][2]-=max_single[temp1]

        if double_count > 2:
            for temp2 in range(10):
                country_results[temp2][2]-=max_double[temp2]

        country_results = sorted(country_results, key=lambda x: x[2])

        i = 1
        prob_start, prob_end = 0

        corrected_country_results=[]

        xx_count = 0
        for i in range(10):
            
            if country_results[prob_start][2] == country_results[i][2]:
                prob_end += 1
            else:
                xx_count, sec_sorted = resolve_ties(xx_count, prob_start, prob_end)
                corrected_country_results += sec_sorted
                prob_start, prob_end = i
  

        xx_count, sec_sorted = resolve_ties(xx_count, prob_start, prob_end)
        corrected_country_results += sec_sorted

        return format_output(corrected_country_results)

        pass#(s)

    def medal_table_result(self, results_string):#(s)
        """
        Output the class table discard string

        :param: boat_type: An integer denoting which type of boat 
        :return: A string in the specified format as shown in the pdf 
        """

        # Your code here

        arr = [[i+1,0,0,0,0] for i in range(10)]

        def format(arr):
            return ", ".join(["-".join( ["0"+str(arr[i][j]) if arr[i][j]<10 else str(arr[i][j]) for j in range(len(arr[i]))]) for i in range(len(arr))])
        
        for i in range(10):
            r_string = self.class_table_discard_result(i+1,results_string).split(", ")
            for j in range(3):
                arr[int(r_string[j][:2])-1][j+1]+=1
                arr[int(r_string[j][:2])-1][4]+= 3-j
            

        return format(sorted(arr,key = lambda x : (x[4],x[1],x[2],x[3]), reverse=True))
    
        pass#(s)


if __name__ == '__main__':  # (s)
    # You can place any ad-hoc testing here
    # e.g. my_instance = Races()
    # e.g. section_1 = my_instance.read_results()
    # e.g. print(section_1)

    
    pass#(s)
