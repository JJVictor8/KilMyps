from register import register as reg
from memory_register import memory_register as mem_reg
arquivo = 'assembly.txt'
read = 'r'
jump_instruction = []


def addi(load_reg, reg_add, immediate):
    add_reg = reg[reg_add] + int(immediate)
    reg[load_reg] = add_reg


def add(load_reg, reg_add_one, reg_add_two):
    add_reg = reg[reg_add_one] + reg[reg_add_two]
    reg[load_reg] = add_reg


def lw(load_reg, reg_memory, address):
    local_address = mem_reg['memory'][(reg[reg_memory[0]] + int(int(address)/4)) - 1] 
    reg[load_reg] = local_address 


def sw(store_reg, reg_memory, address):
    local_address = (reg[reg_memory[0]] + int(int(address)/4)) - 1
    mem_reg['memory'][local_address] = reg[store_reg] 


def j(jump_instruction, cmd):
    if len(jump_instruction) != 0:
        for each in cmd:
            if each.split(' ')[0].strip() == jump_instruction[-1]:
                command = each.split(' ')[1].strip()
                instruction_line = each.split(' ')[2].strip()
                instruction = instruction_line.split(',')
                for each in instruction:
                    if 'j' in each: # If for a Jump instruction # j Exit
                        command = (each[:1]).strip()
                        instruction = (each[1:]).strip()
                        jump_instruction.append(instruction)
                        j(jump_instruction, cmd)
                        break
                    elif command == 'beq': # If for a Branch if Equals instructinon # beq s3,s4,L1
                        command = (each[:3]).strip() 
                        instruction = (each[3:]).strip().split(',')
                        first_reg = instruction[0].strip()
                        second_reg = instruction[1].strip()
                        if reg[first_reg] == reg[second_reg]:
                            branch = instruction[2].strip()
                            jump_instruction.append(branch)
                            j(jump_instruction, cmd)
                            break
                        else:
                            pass
                    elif command == 'lw': # If for a Load word instruction # lw t0,0(t1)
                        load_reg = instruction[0].strip() # Getting the register to load in a memory
                        try_memory = instruction[1].split('(') # print(memory) = [' 0', 't0)']
                        reg_memory = try_memory[1].split(')') # Getting the register to add in the address to specify where will it load. Use memory[0]
                        address = try_memory[0].strip() # Getting the address to add with the register
                        lw(load_reg, reg_memory, address)
                    elif command == 'sw': # If for a Store word instruction # sw t0, 0(t1)
                        store_reg = instruction[0].strip() # Getting the register to load in a memory
                        try_memory = instruction[1].split('(') # print(memory) = [' 0', 't0)']
                        reg_memory = try_memory[1].split(')') # Getting the register to add in the address to specify where will it load. Use memory[0]
                        address = try_memory[0].strip() # Getting the address to add with the register
                        sw(store_reg, reg_memory, address)
                    elif command == 'addi': # If for a addi instruction # addi t0, t1, 1
                        load_reg = instruction[0].strip() # Getting the register to load the result
                        reg_add = instruction[1].strip() # Getting the first register to the add operation
                        immediate = instruction[2].strip() # Getting the immediate constant to the add operation
                        addi(load_reg, reg_add, immediate)
                    elif each[:3] == 'add': # If for a add instruction # add t0,t1,t2
                        load_reg = instruction[0].strip() # Getting the register to load the result
                        reg_add_one = instruction[1].strip() # Getting the first register to the add operation
                        reg_add_two = instruction[2].strip() # Getting the second register to the add operation
                        add(load_reg, reg_add_one, reg_add_two)
                        

with open(arquivo, read) as code:
    cmd = code.readlines() # cmd correspond to command of the file complete orded in List
    # print(cmd) = ['addi t0, t0, 5\n', 'addi t1, t0, 4']
    for each in cmd:
        # print(each) = addi t0, t0, 5 or addi t1, t0, 4 # Each represents lines of code in assembly.txt
        if 'j' in each: # If for a Jump instruction # j Exit
            command = (each[:1]).strip()
            instruction = (each[1:]).strip()
            jump_instruction.append(instruction)
            j(jump_instruction, cmd)
            break
        elif each[:3] == 'beq': # If for a Branch if Equals instructinon # beq s3,s4,L1
            command = (each[:3]).strip() 
            instruction = (each[3:]).strip().split(',')
            first_reg = instruction[0].strip()
            second_reg = instruction[1].strip()
            if reg[first_reg] == reg[second_reg]:
                branch = instruction[2].strip()
                jump_instruction.append(branch)
                j(jump_instruction, cmd)
                break
            else:
                pass
        elif each[:2] == 'lw': # If for a Load word instruction # lw t0,0(t1)
            command = (each[:2]).strip()
            instruction = (each[2:]).strip().split(',') # print(instruction) = [' t2', ' 0(t0)']
            load_reg = instruction[0].strip() # Getting the register to load in a memory
            try_memory = instruction[1].split('(') # print(memory) = [' 0', 't0)']
            reg_memory = try_memory[1].split(')') # Getting the register to add in the address to specify where will it load. Use memory[0]
            address = try_memory[0].strip() # Getting the address to add with the register
            lw(load_reg, reg_memory, address)
        elif each[:2] == 'sw': # If for a Store word instruction # sw t0, 0(t1)
            command = (each[:2].strip())
            instruction = (each[2:]).strip().split(',')
            store_reg = instruction[0].strip() # Getting the register to load in a memory
            try_memory = instruction[1].split('(') # print(memory) = [' 0', 't0)']
            reg_memory = try_memory[1].split(')') # Getting the register to add in the address to specify where will it load. Use memory[0]
            address = try_memory[0].strip() # Getting the address to add with the register
            sw(store_reg, reg_memory, address)
        elif each[:4] == 'addi': # If for a addi instruction # addi t0, t1, 1
            command = (each[:4]).strip() 
            instruction = (each[4:]).strip().split(',')
            load_reg = instruction[0].strip() # Getting the register to load the result
            reg_add = instruction[1].strip() # Getting the first register to the add operation
            immediate = instruction[2].strip() # Getting the immediate constant to the add operation
            addi(load_reg, reg_add, immediate)
        elif each[:3] == 'add': # If for a add instruction # add t0,t1,t2
            command = (each[:3]).strip() 
            instruction = (each[3:]).strip().split(',')
            load_reg = instruction[0].strip() # Getting the register to load the result
            reg_add_one = instruction[1].strip() # Getting the first register to the add operation
            reg_add_two = instruction[2].strip() # Getting the second register to the add operation
            add(load_reg, reg_add_one, reg_add_two)
        else:
            line = each.split(' ')
            command = line[1].strip()
            instruction = line[2].strip()
            if command == 'beq': # If for a Branch if Equals instructinon # beq s3,s4,L1
                command = (each[:3]).strip() 
                instruction = (each[3:]).strip().split(',')
                first_reg = instruction[0].strip()
                second_reg = instruction[1].strip()
                if reg[first_reg] == reg[second_reg]:
                    branch = instruction[2].strip()
                    jump_instruction.append(branch)
                    j(jump_instruction, cmd)
                    break
                else:
                    break
            elif command == 'lw': # If for a Load word instruction # lw t0,0(t1)
                load_reg = instruction[0].strip() # Getting the register to load in a memory
                try_memory = instruction[1].split('(') # print(memory) = [' 0', 't0)']
                reg_memory = try_memory[1].split(')') # Getting the register to add in the address to specify where will it load. Use memory[0]
                address = try_memory[0].strip() # Getting the address to add with the register
                lw(load_reg, reg_memory, address)
            elif command == 'sw': # If for a Store word instruction # sw t0, 0(t1)
                store_reg = instruction[0].strip() # Getting the register to load in a memory
                try_memory = instruction[1].split('(') # print(memory) = [' 0', 't0)']
                reg_memory = try_memory[1].split(')') # Getting the register to add in the address to specify where will it load. Use memory[0]
                address = try_memory[0].strip() # Getting the address to add with the register
                sw(store_reg, reg_memory, address)
            elif command == 'addi': # If for a addi instruction # addi t0, t1, 1
                load_reg = instruction[0].strip() # Getting the register to load the result
                reg_add = instruction[1].strip() # Getting the first register to the add operation
                immediate = instruction[2].strip() # Getting the immediate constant to the add operation
                addi(load_reg, reg_add, immediate)
            elif command == 'add': # If for a add instruction # add t0,t1,t2
                load_reg = instruction[0].strip() # Getting the register to load the result
                reg_add_one = instruction[1].strip() # Getting the first register to the add operation
                reg_add_two = instruction[2].strip() # Getting the second register to the add operation
                add(load_reg, reg_add_one, reg_add_two)
        print(reg)
        # print(command) = addi or addi or j
        # print(instruction) = [' t0', ' t0', ' 5\n'] or [' t1', ' t0', ' 4']
print(mem_reg)
code.close()
