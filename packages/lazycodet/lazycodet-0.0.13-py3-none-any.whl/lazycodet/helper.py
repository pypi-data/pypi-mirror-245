import os
class Helper:

    @staticmethod
    def mergeTextFiles(folder_path, output_file):
        """
        ### mergeTextFiles
        This method will merge all the text files in the folder after save all text files to a text file
        #### folder_path:
        path to folder contains files
        #### output_file:
        path of file after merge
        """
        with open(output_file, 'w', encoding='utf-8') as output:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf8') as input_file:
                            content = input_file.read()
                            output.write(content)
                            output.write('\n')  # Add a newline between file contents
        print('Merge complete !')