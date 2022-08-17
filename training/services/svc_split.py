
def split_and_code():
    """Split a number and give it as dollars based on county level splits for voaww training"""
    print("This program splits a decimal number across all three VOAWW counties.")
    number = float(input("What number are we splitting?\n"))

    ska = round((number * 0.3),2)
    sno = round((number * 0.45),2)
    king = round((number * 0.25),2)

    print ("-*-*-*-*-*-*-*-*-*-*-*-*-\n")
    print(f"Skagit: ${ska}")
    print(f"Snohmish: ${sno}")
    print(f"King: ${king}")
    print ("-*-*-*-*-*-*-*-*-*-*-*-*-\n")

if __name__ == "__main__":
    split_and_code()
