import subprocess
import random
import sys

PUSH_SWAP_EXECUTABLE = "./push_swap"

INT_MIN = -2147483648
INT_MAX = 2147483647

def validate_input(input_sequence):
    seen = set()
    for num in input_sequence:
        if not isinstance(num, int):
            return False, "Error: Non-numeric parameter"
        if num in seen:
            return False, "Error: Duplicate parameter"
        if num < INT_MIN or num > INT_MAX:
            return False, "Error: Parameter out of bounds"
        seen.add(num)
    return True, ""

def is_sorted(sequence):
    return sequence == sorted(sequence)

def run_push_swap(input_sequence):

    is_valid, error_message = validate_input(input_sequence)
    if not is_valid:
        return error_message, ""

    try:
        
        arg_str = " ".join(map(str, input_sequence))

        push_swap_result = subprocess.run([PUSH_SWAP_EXECUTABLE] + list(map(str, input_sequence)),
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=4)

        push_swap_output = push_swap_result.stdout.decode('utf-8').strip()

        stack_a = input_sequence[:]
        stack_b = []
        for operation in push_swap_output.splitlines():
            if operation == "sa":
                if len(stack_a) > 1:
                    stack_a[0], stack_a[1] = stack_a[1], stack_a[0]
            elif operation == "sb":
                if len(stack_b) > 1:
                    stack_b[0], stack_b[1] = stack_b[1], stack_b[0]
            elif operation == "ss":
                if len(stack_a) > 1:
                    stack_a[0], stack_a[1] = stack_a[1], stack_a[0]
                if len(stack_b) > 1:
                    stack_b[0], stack_b[1] = stack_b[1], stack_b[0]
            elif operation == "pa":
                if stack_b:
                    stack_a.insert(0, stack_b.pop(0))
            elif operation == "pb":
                if stack_a:
                    stack_b.insert(0, stack_a.pop(0))
            elif operation == "ra":
                if stack_a:
                    stack_a.append(stack_a.pop(0))
            elif operation == "rb":
                if stack_b:
                    stack_b.append(stack_b.pop(0))
            elif operation == "rr":
                if stack_a:
                    stack_a.append(stack_a.pop(0))
                if stack_b:
                    stack_b.append(stack_b.pop(0))
            elif operation == "rra":
                if stack_a:
                    stack_a.insert(0, stack_a.pop())
            elif operation == "rrb":
                if stack_b:
                    stack_b.insert(0, stack_b.pop())
            elif operation == "rrr":
                if stack_a:
                    stack_a.insert(0, stack_a.pop())
                if stack_b:
                    stack_b.insert(0, stack_b.pop())
            else:
                return "Error: Invalid operation", push_swap_output

        if is_sorted(stack_a) and not stack_b:
            return "OK", push_swap_output
        else:
            return "KO", push_swap_output

    except subprocess.TimeoutExpired:
        return "Timeout expired, process took too long!", ""

def simple_tests():
    print("Running simple tests...")

    test_cases = [
        ([INT_MAX], 0),  
        ([INT_MIN, INT_MAX], 0),  
        ([INT_MIN, 0, INT_MAX], 0),  
        ([INT_MIN, -1, 0, 1, INT_MAX], 0),  
        ([42], 0),  
        ([2, 3], 0), 
        ([0, 1, 2, 3], 0),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 0)  
    ]
    
    for seq, expected_moves in test_cases:
        print(f"Testing sequence: {seq}")
        checker_output, push_swap_output = run_push_swap(seq)
        if checker_output == "OK" and len(push_swap_output.splitlines()) == expected_moves:
            print(f"\033[92mOK\033[0m (No instructions expected)")
        else:
            print(f"\033[91mKO\033[0m (Unexpected output)")

def test_3_elements():
    print("\nRunning 3 elements test...")
    seq = [INT_MAX, 0, INT_MIN]
    checker_output, push_swap_output = run_push_swap(seq)
    if checker_output == "OK" and 2 <= len(push_swap_output.splitlines()) <= 3:
        print(f"\033[92mOK\033[0m with 2 or 3 instructions")
    else:
        print(f"\033[91mKO\033[0m (Incorrect output)")

def test_5_random_elements():
    print("\nRunning 5 random elements test ...")
    seq = [random.randint(INT_MIN, INT_MAX) for _ in range(5)]
    print(f"Sequence: {seq}")
    checker_output, push_swap_output = run_push_swap(seq)
    if checker_output == "OK" and len(push_swap_output.splitlines()) <= 12:
        print(f"\033[92mOK\033[0m with 12 or fewer instructions")
    else:
        print(f"\033[91mKO\033[0m (Incorrect output)")

def test_100_random_elements():
    print("\nRunning 100 random elements test...")
    for i in range(500): 
        seq = [random.randint(INT_MIN, INT_MAX) for _ in range(100)]
        checker_output, push_swap_output = run_push_swap(seq)

        num_instructions = len(push_swap_output.splitlines())
        if checker_output == "OK":
            if num_instructions < 700:
                score = 5
            elif num_instructions < 900:
                score = 4
            elif num_instructions < 1100:
                score = 3
            elif num_instructions < 1300:
                score = 2
            elif num_instructions < 1500:
                score = 1
            else:
                score = 0
            sys.stdout.write(f"\rTest {i + 1}: \033[92mOK\033[0m with score {score} (Instructions: {num_instructions})   ")
        else:
            sys.stdout.write(f"\rTest {i + 1}: \033[91mKO\033[0m (Incorrect output)   ")
        sys.stdout.flush()

    print()

def test_500_random_elements():
    print("\nRunning 500 random elements test...")
    for i in range(500): 
        seq = [random.randint(INT_MIN, INT_MAX) for _ in range(500)]
        checker_output, push_swap_output = run_push_swap(seq)

        num_instructions = len(push_swap_output.splitlines())
        if checker_output == "OK":
            if num_instructions < 5500:
                score = 5
            elif num_instructions < 7000:
                score = 4
            elif num_instructions < 8500:
                score = 3
            elif num_instructions < 10000:
                score = 2
            elif num_instructions < 11500:
                score = 1
            else:
                score = 0
            sys.stdout.write(f"\rTest {i + 1}: \033[92mOK\033[0m with score {score} (Instructions: {num_instructions})   ")
        else:
            sys.stdout.write(f"\rTest {i + 1}: \033[91mKO\033[0m (Incorrect output)   ")
        sys.stdout.flush()

    print() 

def main():
    print("Starting push_swap tests...\n")

    simple_tests()

    test_3_elements()
    test_5_random_elements()

    test_100_random_elements()
    test_500_random_elements()

if __name__ == "__main__":
    main()
