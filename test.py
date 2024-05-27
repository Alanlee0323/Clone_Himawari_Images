for i in range(0, len(values), (end_column - start_column)):
            line = ' '.join(str(value) for value in values[i:i+(end_column - start_column)])
            file.write(line + '\n')