from ctParser import parse_db 
if __name__ == '__main__':
    df = parse_db("Aligners/parser/test/db_file.db")
    print(df)
