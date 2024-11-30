from nksc2c.s3_client import S3Client

def read_data(filename: str, parser=str, sep='\n') -> list:
    sections = open(filename).read().rstrip().split(sep)
    return [parser(section) for section in sections]


def parser(line: list):
    nbname, rest = line.split("->")
    return nbname.rstrip().replace('"',"")

def upload(filename_data):
    with open("nks_nb_template.nb", "rb") as fd:
        notebook_content = fd.read()

    s3 = S3Client()
    for filename in filename_data:
        print(f"Uploading -> {filename}.nb")
        s3.s3_put_object(f"{filename}.nb", notebook_content)
        print(f"Done uploading -> {filename}.nb")
        print()
    print("Process complete!")

if __name__ == "__main__":
    data = read_data("notebooks.txt", parser=parser)
    upload(data)

