
def toBinary(decimal):
    binary = []
    for bit in bin(decimal).replace("0b", "").zfill(3):
        binary.append(eval(bit))
    return binary
      
generate_number =0;  
def btn_increase_pressed():
  
    generate_number = generate_number + 1

btn_increase_pressed()
print(generate_number)